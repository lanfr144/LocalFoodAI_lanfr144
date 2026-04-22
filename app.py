import streamlit as st
import pymysql
import myloginpath
import ollama
import bcrypt
import requests
import json

def local_web_search(query: str) -> str:
    """Search the internet anonymously for nutritional information not found in the database. Returns markdown."""
    try:
        req = requests.get(f'http://127.0.0.1:8080/search', params={'q': query, 'format': 'json'})
        if req.status_code == 200:
            data = req.json()
            results = data.get('results', [])
            if not results:
                return f"No results found on the web for '{query}'."
            # Extract top 3 results
            snippets = [f"Source: {r.get('url')}\nContent: {r.get('content')}" for r in results[:3]]
            return "\n\n".join(snippets)
        return "Search engine returned an error."
    except Exception as e:
        return f"Local search engine unreachable: {e}"

search_tool_schema = {
    'type': 'function',
    'function': {
        'name': 'local_web_search',
        'description': 'Search the internet anonymously for nutritional information or recent food facts not found in the database.',
        'parameters': {
            'type': 'object',
            'properties': {
                'query': {
                    'type': 'string',
                    'description': 'The detailed search query to send to the external search engine.',
                },
            },
            'required': ['query'],
        },
    },
}
# -------------------------------------------------------------------
# Database Connections (PoLP & SoD)
# -------------------------------------------------------------------
def get_db_connection(login_path):
    """Dynamically connect using myloginpath to preserve Segregation of Duties."""
    try:
        conf = myloginpath.parse(login_path)
        return pymysql.connect(
            host=conf.get('host', '127.0.0.1'),
            user=conf.get('user'),
            password=conf.get('password'),
            database='food_db',
            cursorclass=pymysql.cursors.DictCursor
        )
    except Exception as e:
        st.error(f"Failed to connect using login-path '{login_path}'. Did you run mysql_config_editor?")
        st.sidebar.error(f"Connection Error: {e}")
        return None

# -------------------------------------------------------------------
# Authentication Logic
# -------------------------------------------------------------------
def verify_login(username, password):
    conn = get_db_connection('app_auth')
    if not conn: return False
    
    with conn.cursor() as cursor:
        cursor.execute("SELECT password_hash FROM users WHERE username = %s LIMIT 1", (username,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            # Check the hash
            return bcrypt.checkpw(password.encode('utf-8'), result['password_hash'].encode('utf-8'))
    return False

def register_user(username, password):
    conn = get_db_connection('app_auth')
    if not conn: return False
    
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    try:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, hashed))
            conn.commit()
        conn.close()
        return True
    except pymysql.err.IntegrityError:
        return False  # Username exists

# -------------------------------------------------------------------
# UI Flow
# -------------------------------------------------------------------
st.set_page_config(page_title="Food AI Explorer", page_icon="🍔", layout="wide")

if "authenticated_user" not in st.session_state:
    st.session_state["authenticated_user"] = None

# Sidebar Authentication
with st.sidebar:
    st.title("User Portal 🔐")
    if st.session_state["authenticated_user"]:
        st.success(f"Logged in as: {st.session_state['authenticated_user']}")
        if st.button("Logout"):
            st.session_state["authenticated_user"] = None
            st.rerun()
    else:
        tab1, tab2 = st.tabs(["Login", "Register"])
        with tab1:
            l_user = st.text_input("Username", key="l_user")
            l_pass = st.text_input("Password", type="password", key="l_pass")
            if st.button("Login"):
                if verify_login(l_user, l_pass):
                    st.session_state["authenticated_user"] = l_user
                    st.success("Logged in successfully!")
                    st.rerun()
                else:
                    st.error("Invalid username or password.")
        with tab2:
            r_user = st.text_input("Username", key="r_user")
            r_pass = st.text_input("Password", type="password", key="r_pass")
            if st.button("Register"):
                if len(r_pass) < 6:
                    st.error("Password too short.")
                elif register_user(r_user, r_pass):
                    st.success("Registered successfully! Please log in.")
                else:
                    st.error("Username already exists.")

# Main Application Logic
if not st.session_state["authenticated_user"]:
    st.title("🍔 Food AI Local Explorer")
    st.info("Please login or register on the sidebar to interact with the LLM.")
    st.stop()  # Halt execution here, keeping it secure.

# --- Authenticated App ---
st.title("🍔 Food AI Local Explorer")
st.markdown("Interrogate your database leveraging your private secure stack.")

# Checking products via Reader Login path
conn_reader = get_db_connection('app_reader')
if conn_reader:
    with conn_reader.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) as total FROM products;")
        total_products = cursor.fetchone()['total']
        st.sidebar.info(f"Database Scope: {total_products} products.")

tab_chat, tab_explore = st.tabs(["💬 AI Chat", "🔍 Food Search & Details"])

with tab_chat:
    st.subheader("Chat with the Context")
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you analyze the food data today?"}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input("Ask about the food items..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        sys_prompt = "You are a helpful data analyst AI. Answer strictly using local data contexts. If you need external data, use the local_web_search tool!"
        
        with st.spinner("Analyzing the dataset locally..."):
            try:
                # Compile complete conversational history
                temp_messages = [{"role": "system", "content": sys_prompt}] + [m for m in st.session_state.messages if m["role"] != "tool"]
                
                # Primary AI inference
                response = ollama.chat(
                    model='mistral', 
                    messages=temp_messages,
                    tools=[search_tool_schema]
                )
                
                # Check if Mistral decided it needs to search the web
                if response.get('message', {}).get('tool_calls'):
                    for tool in response['message']['tool_calls']:
                        if tool['function']['name'] == 'local_web_search':
                            query_arg = tool['function']['arguments'].get('query')
                            st.info(f"🔍 AI is autonomously searching the web for: '{query_arg}'")
                            
                            # Execute the local web search against SearXNG
                            search_data = local_web_search(query_arg)
                            
                            # Append the tool's thought and the raw search results to the session memory
                            st.session_state.messages.append(response['message'])
                            st.session_state.messages.append({
                                'role': 'tool', 
                                'content': search_data, 
                                'name': 'local_web_search'
                            })
                            
                            # Feed the web data back into Mistral for the final summarization
                            temp_messages = [{"role": "system", "content": sys_prompt}] + st.session_state.messages
                            response = ollama.chat(
                                model='mistral',
                                messages=temp_messages
                            )
                
                ai_reply = response['message']['content']
            except Exception as e:
                ai_reply = f"Hold on! Engine execution fault: {e}"

        st.session_state.messages.append({"role": "assistant", "content": ai_reply})
        st.chat_message("assistant").write(ai_reply)

with tab_explore:
    st.subheader("Raw Data Search")
    search_query = st.text_input("Search Product Name or Ingredient (e.g. 'Nutella' or 'Sugar')")
    
    if st.button("Search Database") and search_query and conn_reader:
        with st.spinner("Querying MySQL..."):
            try:
                with conn_reader.cursor() as cursor:
                    # Leverage the FULLTEXT INDEX built in init.sql
                    query = """
                        SELECT code, product_name, generic_name, brands, ingredients_text 
                        FROM products 
                        WHERE MATCH(product_name, ingredients_text) AGAINST(%s IN NATURAL LANGUAGE MODE)
                        LIMIT 50
                    """
                    cursor.execute(query, (search_query,))
                    results = cursor.fetchall()
            except Exception as e:
                st.error(f"SQL Error: {e}")
                results = []
                
        if results:
            st.success(f"Found {len(results)} matching records!")
            st.dataframe(results, use_container_width=True)
        else:
            st.warning("No products found matching those terms.")

if conn_reader:
    conn_reader.close()
