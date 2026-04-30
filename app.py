import streamlit as st
import pymysql
import myloginpath
import ollama
import bcrypt
import requests
import string
import random
import smtplib
from email.message import EmailMessage
import pandas as pd
from unit_converter import UnitConverter
from snmp_notifier import notifier

def local_web_search(query: str) -> str:
    try:
        req = requests.get(f'http://127.0.0.1:8080/search', params={'q': query, 'format': 'json'})
        if req.status_code == 200:
            data = req.json()
            results = data.get('results', [])
            if not results: return f"No results found on the web for '{query}'."
            snippets = [f"Source: {r.get('url')}\nContent: {r.get('content')}" for r in results[:3]]
            return "\n\n".join(snippets)
        return "Search engine returned an error."
    except Exception as e: return f"Local search engine unreachable: {e}"

search_tool_schema = {
    'type': 'function',
    'function': {
        'name': 'local_web_search',
        'description': 'Search the internet for info not in DB.',
        'parameters': {'type': 'object', 'properties': {'query': {'type': 'string'}}, 'required': ['query']},
    },
}

def search_nutrition_db(query: str) -> str:
    conn = get_db_connection('app_reader')
    if not conn: return "Database connection failed."
    try:
        with conn.cursor() as cursor:
            # Query products view via natural language match on core table
            sql = """
                SELECT c.product_name, m.proteins_100g, m.fat_100g, m.carbohydrates_100g, m.sugars_100g 
                FROM food_db.products_core c
                LEFT JOIN food_db.products_macros m ON c.code = m.code
                WHERE MATCH(c.product_name, c.ingredients_text) AGAINST(%s IN BOOLEAN MODE)
                AND c.product_name IS NOT NULL AND c.product_name != '' AND c.product_name != 'None'
                LIMIT 5
            """
            bool_query = " ".join([f"+{w}" for w in query.split()])
            cursor.execute(sql, (bool_query,))
            results = cursor.fetchall()
            if not results: return f"No database records found for '{query}'."
            
            snippets = []
            for r in results:
                snippets.append(f"- {r['product_name']}: Protein {r['proteins_100g']}g, Fat {r['fat_100g']}g, Carbs {r['carbohydrates_100g']}g, Sugars {r['sugars_100g']}g (per 100g)")
            return "\n".join(snippets)
    except Exception as e:
        return f"Database query failed: {e}"
    finally:
        conn.close()

db_search_tool_schema = {
    'type': 'function',
    'function': {
        'name': 'search_nutrition_db',
        'description': 'Search the local medical nutrition database for product macros and ingredients. ALWAYS prioritize this over web search.',
        'parameters': {'type': 'object', 'properties': {'query': {'type': 'string', 'description': 'The product or food name to search for (e.g. apple, chicken, bread)'}}, 'required': ['query']},
    },
}

def get_db_connection(login_path):
    try:
        conf = myloginpath.parse(login_path)
        if not conf or not conf.get('user'):
            st.error(f"⚠️ MySQL configuration missing for `{login_path}`. If you are testing locally on Windows, this app must be run on the Ubuntu server where `mysql_config_editor` is properly configured.")
            return None
            
        return pymysql.connect(
            host=conf.get('host', '127.0.0.1'),
            user=conf.get('user'),
            password=conf.get('password'),
            database='food_db',
            cursorclass=pymysql.cursors.DictCursor
        )
    except Exception as e:
        st.error(f"Connection Failed: {e}")
        return None

def verify_login(username, password):
    conn = get_db_connection('app_auth')
    if not conn: return False
    with conn.cursor() as cursor:
        cursor.execute("SELECT password_hash FROM users WHERE username = %s LIMIT 1", (username,))
        result = cursor.fetchone()
        conn.close()
        if result: return bcrypt.checkpw(password.encode('utf-8'), result['password_hash'].encode('utf-8'))
    return False

def get_user_id(username):
    conn = get_db_connection('app_auth')
    if not conn: return None
    with conn.cursor() as cursor:
        cursor.execute("SELECT id FROM users WHERE username = %s LIMIT 1", (username,))
        result = cursor.fetchone()
        conn.close()
        return result['id'] if result else None

def get_eav_profile(username):
    uid = get_user_id(username)
    if not uid: return []
    conn = get_db_connection('app_auth')
    with conn.cursor() as cursor:
        cursor.execute("SELECT id, illness_health_condition_diet_dislikes_name as name, illness_health_condition_diet_dislikes_value as value FROM user_health_profiles WHERE user_id = %s", (uid,))
        res = cursor.fetchall()
        conn.close()
        return res

def get_user_limit(username):
    conn = get_db_connection('app_auth')
    if not conn: return "50"
    with conn.cursor() as cursor:
        cursor.execute("SELECT search_limit FROM users WHERE username = %s LIMIT 1", (username,))
        result = cursor.fetchone()
        conn.close()
        return result['search_limit'] if (result and result['search_limit']) else "50"

def register_user(username, password, email):
    conn = get_db_connection('app_auth')
    if not conn: return False
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    try:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO users (username, password_hash, email) VALUES (%s, %s, %s)", (username, hashed, email))
            conn.commit()
        conn.close()
        send_email(email, "Welcome to Local Food AI", f"Hello {username}, your account was securely created!", to_name=username.title())
        return True
    except pymysql.err.IntegrityError:
        return False

def send_email(to_email, subject, body, to_name="User"):
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = '"Clinical Food AI System" <security@localfoodai.com>'
    msg['To'] = f'"{to_name}" <{to_email}>'
    
    import time
    for attempt in range(5):
        try:
            s = smtplib.SMTP('localhost', 25)
            s.send_message(msg)
            s.quit()
            return True
        except Exception as e:
            if attempt == 4:
                return f"SMTP Delivery Failed: {str(e)}"
            time.sleep(2)
    return "Unknown Error Occurred"

def reset_password(username, email):
    conn = get_db_connection('app_auth')
    if not conn: return False
    with conn.cursor() as cursor:
        cursor.execute("SELECT id, email FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        if user and user['email'] == email:
            new_pass = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            hashed = bcrypt.hashpw(new_pass.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            cursor.execute("UPDATE users SET password_hash = %s WHERE id = %s", (hashed, user['id']))
            conn.commit()
            conn.close()
            status = send_email(email, "Password Reset", f"Your new temporary password is: {new_pass}", to_name=username.title())
            if status is True:
                return True
            return status
    return False

# UI Theming
def render_version():
    import os, datetime
    file_time = datetime.datetime.fromtimestamp(os.path.getmtime(__file__)).strftime('%Y-%m-%d %H:%M:%S')
    st.markdown("---")
    st.caption("🚀 Version: v1.3.0")
    st.caption(f"📅 Last Updated: {file_time}")

st.set_page_config(page_title="Food AI Explorer", page_icon="🍔", layout="wide")
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    html, body, [class*="css"]  { font-family: 'Inter', sans-serif; background-color: #0b192c; color: #e2e8f0; }
    h1, h2, h3 { color: #38bdf8 !important; font-weight: 600; letter-spacing: 0.5px; }
    div[data-testid="stSidebar"] { background: rgba(11, 25, 44, 0.95) !important; backdrop-filter: blur(10px); border-right: 1px solid #1e293b; }
    .stButton>button { background: linear-gradient(135deg, #0ea5e9, #0284c7); color: white; border: none; border-radius: 6px; }
    .stButton>button:hover { transform: scale(1.02); }
    .stTextInput>div>div>input, .stNumberInput>div>div>input, .stSelectbox>div>div>div { background-color: #0f172a; color: #f8fafc; border: 1px solid #38bdf8; }
</style>
""", unsafe_allow_html=True)

if "authenticated_user" not in st.session_state:
    st.session_state["authenticated_user"] = None

with st.sidebar:
    st.title("User Portal 🔐")
    render_version()
    if st.session_state["authenticated_user"]:
        st.success(f"Logged in as: {st.session_state['authenticated_user']}")
        if st.button("Logout"):
            st.session_state["authenticated_user"] = None
            st.rerun()
            
        st.markdown("---")
        st.subheader("🏥 Dynamic Health Profile")
        eav_data = get_eav_profile(st.session_state["authenticated_user"])
        uid = get_user_id(st.session_state["authenticated_user"])
        user_lim = get_user_limit(st.session_state["authenticated_user"])
        
        with st.expander("⚙️ Account Preferences"):
            opts = ["10", "20", "50", "100", "All"]
            idx = opts.index(user_lim) if user_lim in opts else 2
            new_lim = st.selectbox("Default Search Limit", opts, index=idx)
            if new_lim != user_lim:
                conn = get_db_connection('app_auth')
                with conn.cursor() as c:
                    c.execute("UPDATE users SET search_limit = %s WHERE id = %s", (new_lim, uid))
                    conn.commit()
                st.rerun()

        with st.expander("➕ Add Condition / Diet"):
            new_cat = st.selectbox("Category", ["Condition", "Illness", "Diet", "Dislike", "Allergy"])
            new_val = st.text_input("Value (e.g. 'vegan', 'diabetes', 'broccoli')").strip().lower()
            if st.button("Add to Profile") and new_val and uid:
                conn = get_db_connection('app_auth')
                with conn.cursor() as c:
                    c.execute("INSERT INTO user_health_profiles (user_id, illness_health_condition_diet_dislikes_name, illness_health_condition_diet_dislikes_value) VALUES (%s, %s, %s)", (uid, new_cat, new_val))
                    conn.commit()
                st.rerun()
                
        if eav_data:
            st.markdown("#### Active Flags")
            for e in eav_data:
                col1, col2 = st.columns([4, 1])
                col1.info(f"**{e['name']}:** {e['value'].title()}")
                if col2.button("X", key=f"del_eav_{e['id']}"):
                    conn = get_db_connection('app_auth')
                    with conn.cursor() as c:
                        c.execute("DELETE FROM user_health_profiles WHERE id = %s", (e['id'],))
                        conn.commit()
                    st.rerun()
    else:
        tab1, tab2, tab3 = st.tabs(["Login", "Register", "Reset"])
        with tab1:
            l_user = st.text_input("Username", key="l_user").strip()
            l_pass = st.text_input("Password", type="password", key="l_pass")
            if st.button("Login"):
                if verify_login(l_user, l_pass):
                    notifier.send_alert(f"User Login Success: {l_user}")
                    st.session_state["authenticated_user"] = l_user
                    st.rerun()
                else:
                    notifier.send_alert(f"User Login Failed: {l_user}")
                    st.error("Invalid login.")
        with tab2:
            r_user = st.text_input("Username", key="r_user")
            r_email = st.text_input("Email Address", key="r_email")
            r_pass = st.text_input("Password", type="password", key="r_pass")
            if st.button("Register"):
                if len(r_pass) < 6: st.error("Password too short.")
                elif register_user(r_user, r_pass, r_email): st.success("Registered safely!")
                else: st.error("Username exists.")
        with tab3:
            f_user = st.text_input("Username", key="f_user")
            f_email = st.text_input("Registered Email", key="f_email")
            if st.button("Send Reset Link"):
                status = reset_password(f_user, f_email)
                if status is True: 
                    st.success("Password reset emailed.")
                else: 
                    st.error(f"Failed: {status}")

if not st.session_state["authenticated_user"]:
    st.title("🍔 Food AI Medical Explorer")
    st.info("Please login to interrogate the Clinical Data.")
    st.stop()

st.title("🍔 Food AI Clinical Explorer")
conn_reader = get_db_connection('app_reader')

tab_chat, tab_explore, tab_plate, tab_planner = st.tabs(["💬 AI Chat", "🔬 Clinical Search", "🍽️ My Plate Builder", "🤖 AI Meal Planner"])

import re

with tab_chat:
    c1, c2 = st.columns([4, 1])
    c1.subheader("Chat with the Context")
    if c2.button("🧹 Clear Chat"):
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you analyze the food data today?"}]
        st.rerun()
    st.info("""
    ℹ️ **How to use this feature (Examples)**
    **Your active conditions (e.g. Pregnant, Diabetic) are automatically sent to the AI in the background. You do not need to type them out.**
    
    *Examples:*
    1. "I am pregnant, diabetic, and have kidney problems. Can I eat sushi?"
    2. "What is a safe snack to stabilize my blood sugar without hurting my kidneys?"
    3. "Can I drink milk? I need calcium for the baby."
    4. "Is it safe to eat a large steak for iron?"
    5. "What foods are strictly forbidden for me?"
    """)
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you analyze the food data today?"}]

        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display chat history, filtering out TOOL_CALLS
        for msg in st.session_state.messages:
            if msg["role"] == "tool": continue
            display_text = re.sub(r'\[TOOL_CALLS\]\s*\[.*?\]', '', msg["content"]).strip()
            if display_text:
                st.chat_message(msg["role"]).write(display_text)
        
        user_eav = get_eav_profile(st.session_state["authenticated_user"])
        profile_text = ", ".join([f"{p['name']}: {p['value']}" for p in user_eav]) if user_eav else "None"
        
        sys_prompt = f"""You are a helpful medical data analyst AI. 
        The user has the following health profile / conditions: {profile_text}. 
        You MUST act as a specialized clinical dietitian. Autonomously deduce what foods are recommended, forbidden, or accepted for these specific conditions and apply these rules to all your answers.
        ALWAYS query the local database using the search_nutrition_db tool to answer questions about food, macros, and nutrients before answering or searching the web! If it's not in the DB, you can use local_web_search.
        DO NOT hallucinate that a well-known food like sushi has 0 macros just because the database is missing a row. Use your medical knowledge to supplement missing database data and warn the user of biological facts (e.g. Sushi contains raw fish and carbs from rice)."""
        with st.spinner("Analyzing..."):
            try:
                temp_messages = [{"role": "system", "content": sys_prompt}] + [m for m in st.session_state.messages if m["role"] != "tool"]
                response = ollama.chat(model='llama3', messages=temp_messages, tools=[search_tool_schema, db_search_tool_schema])
                
                if response.get('message', {}).get('tool_calls'):
                    for tool in response['message']['tool_calls']:
                        if tool['function']['name'] == 'local_web_search':
                            query_arg = tool['function']['arguments'].get('query')
                            st.info(f"🔍 Web Search triggered for: '{query_arg}'")
                            search_data = local_web_search(query_arg)
                            st.session_state.messages.append(response['message'])
                            st.session_state.messages.append({'role': 'tool', 'content': search_data, 'name': 'local_web_search'})
                        elif tool['function']['name'] == 'search_nutrition_db':
                            query_arg = tool['function']['arguments'].get('query')
                            st.info(f"🗄️ Database Search triggered for: '{query_arg}'")
                            db_data = search_nutrition_db(query_arg)
                            st.session_state.messages.append(response['message'])
                            st.session_state.messages.append({'role': 'tool', 'content': db_data, 'name': 'search_nutrition_db'})
                            
                    temp_messages = [{"role": "system", "content": sys_prompt}] + st.session_state.messages
                    response = ollama.chat(model='llama3', messages=temp_messages)
                ai_reply = response['message']['content']
                ai_reply = re.sub(r'\[TOOL_CALLS\]\s*\[.*?\]', '', ai_reply).strip()
            except Exception as e: ai_reply = f"Hold on! Engine execution fault: {e}"

        st.session_state.messages.append({"role": "assistant", "content": ai_reply})
        st.chat_message("assistant").write(ai_reply)

def highlight_medical_warnings(row):
    try:
        val = str(row.get('Medical Warning', ''))
        if '⚠️' in val: return ['background-color: rgba(255, 0, 0, 0.4); color: white;'] * len(row)
        if '💚' in val: return ['background-color: rgba(0, 255, 0, 0.3); color: white;'] * len(row)
    except: pass
    return [''] * len(row)

with tab_explore:
    st.subheader("Clinical Data Search")
    st.info("""
    ℹ️ **How to use this feature (Examples)**
    **Your active conditions are automatically flagged (⚠️ or 💚) in the search results.**
    
    *Example Searches:*
    1. `Cereal` *(Checks for high sugar & hidden phosphorus)*
    2. `Cheese` *(Checks for unpasteurized pregnancy risks & high sodium)*
    3. `Fruit Juice` *(Checks for high sugar spikes)*
    4. `Deli Meat` *(Checks for Listeria risk & extreme sodium)*
    5. `White Rice` *(Safe for kidneys but flags high glycemic index)*
    """)
    sq = st.text_input("Search Product Name or Ingredient")
    cols = st.columns(5)
    min_pro = cols[0].number_input("Min Protein (g)", 0, 1000, 0)
    min_fat = cols[1].number_input("Min Fat (g)", 0, 1000, 0)
    min_carb = cols[2].number_input("Min Carbs (g)", 0, 1000, 0)
    max_sug = cols[3].number_input("Max Sugar (g)", 0, 1000, 1000)
    
    # Load dynamically fetched limit to prevent Pandas Styler crash
    pd.set_option("styler.render.max_elements", 5000000)
    opts = [10, 50, 100, 500, 1000]
    
    user_lim_str = get_user_limit(st.session_state["authenticated_user"])
    user_lim_val = 1000 if user_lim_str == "All" else int(user_lim_str)
    if user_lim_val not in opts: user_lim_val = 50
    idx = opts.index(user_lim_val)
    limit_rc = cols[4].selectbox("Limit Results", opts, index=idx)
    
    if st.button("Search Database") and sq and conn_reader:
        notifier.send_alert(f"Medical DB Search Executed: {sq}")
        with st.spinner("Processing massive clinical query..."):
            try:
                with conn_reader.cursor() as cursor:
                    l_str = "" if limit_rc == "All" else f"LIMIT {limit_rc}"
                    query = f"""
                        SELECT c.code, c.product_name, c.generic_name, c.brands, c.ingredients_text,
                               a.allergens,
                               m.`energy-kcal_100g`, m.proteins_100g, m.fat_100g, m.carbohydrates_100g, m.sugars_100g, m.fiber_100g, m.sodium_100g, m.salt_100g, m.cholesterol_100g,
                               v.`vitamin-a_100g`, v.`vitamin-b1_100g`, v.`vitamin-b2_100g`, v.`vitamin-pp_100g`, v.`vitamin-b6_100g`, v.`vitamin-b9_100g`, v.`vitamin-b12_100g`, v.`vitamin-c_100g`, v.`vitamin-d_100g`, v.`vitamin-e_100g`, v.`vitamin-k_100g`,
                               min.calcium_100g, min.iron_100g, min.magnesium_100g, min.potassium_100g, min.zinc_100g
                        FROM food_db.products_core c
                        LEFT JOIN food_db.products_allergens a ON c.code = a.code
                        LEFT JOIN food_db.products_macros m ON c.code = m.code
                        LEFT JOIN food_db.products_vitamins v ON c.code = v.code
                        LEFT JOIN food_db.products_minerals min ON c.code = min.code
                        WHERE MATCH(c.product_name, c.ingredients_text) AGAINST(%s IN BOOLEAN MODE)
                        AND c.product_name IS NOT NULL AND c.product_name != '' AND c.product_name != 'None'
                        AND (m.proteins_100g >= %s OR m.proteins_100g IS NULL)
                        AND (m.fat_100g >= %s OR m.fat_100g IS NULL)
                        AND (m.carbohydrates_100g >= %s OR m.carbohydrates_100g IS NULL)
                        AND (m.sugars_100g <= %s OR m.sugars_100g IS NULL)
                        {l_str}
                    """
                    sq_bool = " ".join([f"+{w}" for w in sq.split()])
                    cursor.execute(query, (sq_bool, min_pro, min_fat, min_carb, max_sug))
                    results = cursor.fetchall()
                    
                    if results:
                        # Fetch EAV Medical Profile
                        eav_profile = get_eav_profile(st.session_state["authenticated_user"])
                        df = pd.DataFrame(results)
                        
                        st.markdown("### 🛠️ Dynamic Column Display")
                        default_columns = [
                            'code', 'product_name', 'generic_name', 'brands', 'allergens', 'ingredients_text',
                            'proteins_100g', 'fat_100g', 'carbohydrates_100g', 'sugars_100g', 'sodium_100g', 'energy-kcal_100g',
                            'vitamin-c_100g', 'iron_100g', 'calcium_100g'
                        ]
                        all_fetched_cols = list(df.columns)
                        valid_defaults = [c for c in default_columns if c in all_fetched_cols]
                        
                        if "selected_columns" not in st.session_state or st.button("Reset Default Columns"):
                            st.session_state["selected_columns"] = valid_defaults
                            st.rerun()
                            
                        chosen_cols = st.multiselect("Customize Dataset View", all_fetched_cols, default=st.session_state["selected_columns"], key="multi_cols")
                        st.session_state["selected_columns"] = chosen_cols
                        
                        # Filter dataframe gracefully, but we retain a copy for background analytics
                        df_display = df[chosen_cols].copy()
                        warnings_col = []
                        
                        for idx, row in df.iterrows():
                            warns = []
                            ing_text = str(row['ingredients_text']).lower()
                            all_text = str(row['allergens']).lower()
                            
                            for param in eav_profile:
                                cat = param['name'].lower()
                                val = param['value']
                                
                                # Disease Analytics
                                if cat == 'illness':
                                    if val == 'diabetes' and pd.notnull(row.get('sugars_100g')) and float(row['sugars_100g']) > 10.0:
                                        warns.append("⚠️ High Sugar (Diabetes)")
                                    if (val == 'hypertension' or val == 'high bp') and pd.notnull(row.get('sodium_100g')) and float(row['sodium_100g']) > 1.5:
                                        warns.append("⚠️ High Salt (Hypertension)")
                                    if val == 'scurvy' and pd.notnull(row.get('vitamin-c_100g')) and float(row['vitamin-c_100g']) > 0.005:
                                        warns.append("💚 High Vitamin C (Scurvy Recommended)")
                                    if val == 'anemia' and pd.notnull(row.get('iron_100g')) and float(row['iron_100g']) > 0.002:
                                        warns.append("💚 High Iron (Anemia Recommended)")
                                        
                                # Condition Analytics
                                if cat == 'condition':
                                    if val == 'pregnant':
                                        if ('cru' in ing_text or 'raw' in ing_text or 'viande crue' in ing_text):
                                            warns.append("⚠️ Raw Foods (Pregnancy Toxoplasmosis)")
                                        if pd.notnull(row.get('iron_100g')) and float(row['iron_100g']) > 0.002:
                                            warns.append("💚 Med-High Iron (Pregnancy Health)")
                                    if val == 'low fat' and pd.notnull(row.get('fat_100g')) and float(row['fat_100g']) > 20.0:
                                        warns.append("⚠️ High Fat")
                                    if val == 'osteoporosis' and pd.notnull(row.get('calcium_100g')) and float(row['calcium_100g']) > 0.1:
                                        warns.append("💚 High Calcium (Bone Health)")
                                        
                            if eav_data:
                                ing_text = str(row.get('ingredients_text', '')).lower()
                                all_text = str(row.get('allergens', '')).lower()
                                product_name_text = str(row.get('product_name', '')).lower()
                                
                                for e in eav_data:
                                    cat = str(e['name']).lower()
                                    val = str(e['value']).lower()
                                    
                                    # Clinical Trace Checks...
                                    if cat == 'condition' and (val == 'pregnant' or val == 'pregnancy' or val == 'breastfeeding'):
                                        # Forbidden / High Risk (Toxoplasmosis & Listeria)
                                        if any(x in ing_text or x in product_name_text for x in ['cru', 'raw', 'viande crue', 'sushi', 'sashimi', 'poisson cru']):
                                            warns.append("⚠️ Forbidden: Raw Meat/Fish (Toxoplasmosis/Parasite Risk)")
                                        if any(x in ing_text or x in product_name_text for x in ['lait cru', 'unpasteurized', 'non pasteurisé']):
                                            warns.append("⚠️ Forbidden: Unpasteurized Dairy (Listeria Risk)")
                                        if any(x in ing_text or x in product_name_text for x in ['alcool', 'wine', 'alcohol', 'beer']):
                                            warns.append("⚠️ Forbidden: Contains Alcohol")
                                            
                                        # Recommended (Iron & Calcium)
                                        if float(row.get('iron_100g', 0) or 0) > 0.003:
                                            warns.append("💚 Recommended: High Iron (Pregnancy Health)")
                                        if float(row.get('calcium_100g', 0) or 0) > 0.120:
                                            warns.append("💚 Recommended: High Calcium (Bone Health / Breastfeeding)")
                                    
                                    if cat == 'illness' and val == 'osteoporosis':
                                        if float(row.get('calcium_100g', 0) or 0) < 0.120:
                                            warns.append("⚠️ Low Calcium (Osteoporosis Risk)")
                                        else:
                                            warns.append("💚 Recommended (High Calcium)")
                                            
                                    if cat == 'illness' and val == 'scurvy':
                                        if float(row.get('vitamin-c_100g', 0) or 0) < 0.010:
                                            warns.append("⚠️ Low Vitamin C (Scurvy Risk)")
                                        else:
                                            warns.append("💚 Recommended (High Vitamin C)")
                                            
                                    if cat == 'diet' and val in ['vegan', 'vegetarian']:
                                        if any(x in ing_text for x in ['meat', 'beef', 'chicken', 'fish', 'gelatin', 'whey', 'pork', 'porc', 'poulet']):
                                            warns.append("⚠️ Contains Animal Products")
                                    if cat == 'diet' and val == 'halal':
                                        if any(x in ing_text for x in ['pork', 'pig', 'porc', 'wine', 'alcohol', 'beer', 'vin']):
                                            warns.append("⚠️ Probable Haram Ingredients (e.g. Pork/Wine)")
                                            
                                    if cat in ['dislike', 'allergy']:
                                        if val in ing_text or val in all_text or val in product_name_text:
                                            warns.append(f"⚠️ Contains: {val.upper()}")
                                            
                            warnings_col.append(" | ".join(list(set(warns))) if warns else "✅ Safe for Profile")
                            
                        df_display.insert(0, 'Medical Warning', warnings_col)
                        styled_df = df_display.style.apply(highlight_medical_warnings, axis=1)

                        st.success(f"Analysed {len(results)} records utilizing dynamic Partitions!")
                        st.dataframe(styled_df, use_container_width=True)
                        
                        if st.button("🤖 Ask AI to Evaluate This Table"):
                            with st.spinner("AI is dynamically evaluating these records against your profile..."):
                                user_eav = get_eav_profile(st.session_state["authenticated_user"])
                                profile_text = ", ".join([f"{p['name']}: {p['value']}" for p in user_eav]) if user_eav else "None"
                                eval_prompt = f"The user has this profile: {profile_text}. Evaluate these foods and state which are highly recommended or strictly forbidden: {df_display.to_dict('records')}"
                                try:
                                    response = ollama.chat(model='llama3', messages=[{'role': 'user', 'content': eval_prompt}])
                                    st.info(response['message']['content'])
                                except Exception as e:
                                    st.error(f"AI Evaluation Failed: {e}")
                    else:
                        st.warning("No products found matching those strict terms.")
            except Exception as e: st.error(f"SQL/Pandas Error: {e}")

with tab_plate:
    st.subheader("🍽️ My Plate Builder")
    st.info("""
    ℹ️ **How to use this feature (Examples & Logic)**
    **Plate Builder Logic:**
    1. Create a New Plate.
    2. Search for exact food words (e.g. 'chicken', 'egg').
    3. Add the food with a specific portion (e.g. '150g').
    4. The system calculates the combined macros.
    5. Use the 🗑️ buttons to delete incorrect items or entire plates.
    
    *Example Plates:*
    1. `150g White Rice` + `50g Chicken Breast` + `100g Green Beans`
    2. `200g Potatoes` + `100g Tomatoes` + `100g Beef`
    3. `100g Spinach Salad` + `50g Feta Cheese`
    4. `200g Lentils` + `100g Quinoa`
    5. `100g Apple` + `30g Almonds`
    """)
    uid = get_user_id(st.session_state["authenticated_user"])
    conn = get_db_connection('app_auth')
    if conn and uid:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, plate_name FROM plates WHERE user_id = %s", (uid,))
            plates = cursor.fetchall()
            
            with st.expander("➕ Create a New Plate"):
                new_plate_name = st.text_input("Plate Name")
                if st.button("Create Plate"):
                    cursor.execute("INSERT INTO plates (user_id, plate_name) VALUES (%s, %s)", (uid, new_plate_name))
                    conn.commit()
                    st.session_state["active_plate"] = new_plate_name
                    st.rerun()

            if plates:
                colA, colB = st.columns([4, 1])
                plate_names = [p['plate_name'] for p in plates]
                default_idx = plate_names.index(st.session_state["active_plate"]) if "active_plate" in st.session_state and st.session_state["active_plate"] in plate_names else 0
                selected_plate = colA.selectbox("Select Active Plate", plate_names, index=default_idx)
                st.session_state["active_plate"] = selected_plate
                active_p_id = next(p['id'] for p in plates if p['plate_name'] == selected_plate)
                
                if colB.button("🗑️ Delete Plate"):
                    cursor.execute("DELETE FROM plates WHERE id = %s", (active_p_id,))
                    conn.commit()
                    if "active_plate" in st.session_state: del st.session_state["active_plate"]
                    st.rerun()
                
                cursor.execute("""
                    SELECT i.id, i.product_code, i.quantity_grams, p.product_name, p.proteins_100g, p.fat_100g, p.carbohydrates_100g 
                    FROM plate_items i LEFT JOIN products p ON i.product_code = p.code WHERE i.plate_id = %s
                """, (active_p_id,))
                items = cursor.fetchall()
                if items:
                    for i in items:
                        c1, c2 = st.columns([5, 1])
                        c1.markdown(f"<li><b>{i['quantity_grams']}g</b> of {i['product_name']} (Pro: {i['proteins_100g'] or 0}g)</li>", unsafe_allow_html=True)
                        if c2.button("🗑️", key=f"del_item_{i['id']}"):
                            cursor.execute("DELETE FROM plate_items WHERE id = %s", (i['id'],))
                            conn.commit()
                            st.rerun()
                            
                    total_pro = sum((float(i['proteins_100g'] or 0) * (float(i['quantity_grams'])/100.0)) for i in items)
                    total_fat = sum((float(i['fat_100g'] or 0) * (float(i['quantity_grams'])/100.0)) for i in items)
                    total_carb = sum((float(i['carbohydrates_100g'] or 0) * (float(i['quantity_grams'])/100.0)) for i in items)
                    st.info(f"**Total Protein:** {total_pro:.1f}g | **Total Fat:** {total_fat:.1f}g | **Total Carbs:** {total_carb:.1f}g")
                
                st.markdown("---")
                st.markdown("#### ➕ Add Food to Plate")
                add_search = st.text_input("Search Exact Product Name (e.g. 'chicken', 'egg')")
                if add_search:
                    bool_search = " ".join([f"+{w}" for w in add_search.split()])
                    cursor.execute("""
                        SELECT c.code, c.product_name 
                        FROM food_db.products_core c
                        JOIN food_db.products_macros m ON c.code = m.code
                        WHERE MATCH(c.product_name, c.ingredients_text) AGAINST(%s IN BOOLEAN MODE)
                        AND c.product_name IS NOT NULL AND c.product_name != '' AND c.product_name != 'None'
                        AND m.proteins_100g IS NOT NULL AND m.fat_100g IS NOT NULL AND m.carbohydrates_100g IS NOT NULL
                        LIMIT 10
                    """, (bool_search,))
                    search_res = cursor.fetchall()
                    if search_res:
                        options = {f"{r['product_name']} ({r['code']})": r for r in search_res}
                        selected_str = st.selectbox("Select Product", list(options.keys()))
                        selected_product = options[selected_str]
                        
                        add_amount_str = st.text_input("Portion Quantity (e.g., '100g', '2 tbsp', '1.5 cups', '1 pinch')", value="100g")
                        
                        if st.button("Add Item to Plate"):
                            # Use UnitConverter to parse
                            grams = UnitConverter.parse_and_convert(add_amount_str, product_name=selected_product['product_name'])
                            if grams is not None:
                                cursor.execute("INSERT INTO plate_items (plate_id, product_code, quantity_grams) VALUES (%s, %s, %s)", 
                                              (active_p_id, selected_product['code'], grams))
                                conn.commit()
                                st.success(f"Added {grams}g of {selected_product['product_name']}!")
                                st.rerun()
                            else:
                                st.error("Could not parse unit. Please use format like '100g' or '1 cup'.")
                    else:
                        st.warning("No products found.")

with tab_planner:
    st.subheader("🤖 AI Meal Planner")
    st.info("""
    ℹ️ **How to use this feature (Examples)**
    **Your active conditions are automatically applied to the generated menu.**
    
    *Example Prompts:*
    1. "Generate a full day meal plan for me. I am pregnant, diabetic, and have kidney disease."
    2. "Plan a pregnancy-safe dinner that won't spike my blood sugar."
    3. "I need a high-iron lunch that is safe for my kidneys."
    4. "Plan a breakfast without dairy that is kidney-friendly."
    5. "Give me a 3-day meal prep plan ensuring no raw fish, controlled protein portions, and steady complex carbs."
    """)
    p_col1, p_col2, p_col3 = st.columns(3)
    target_cal = p_col1.number_input("Target Daily Calories (kcal)", 1000, 5000, 2000, 50)
    diet_pref = p_col2.selectbox("Dietary Preference", ["Omnivore", "Vegetarian", "Vegan", "Keto", "Paleo"])
    meal_count = p_col3.slider("Number of Meals", 2, 6, 3)
    extra_notes = st.text_input("Any additional allergies or goals?")
    
    if st.button("Generate Professional Menu"):
        with st.spinner("AI is formulating and interrogating the local database..."):
            user_eav = get_eav_profile(st.session_state["authenticated_user"])
            profile_text = ", ".join([f"{p['name']}: {p['value']}" for p in user_eav]) if user_eav else "None"
            
            sys_prompt = f"""You are a professional clinical Dietitian planner. Target: {target_cal}kcal over {meal_count} meals. 
            Dietary constraint: {diet_pref}. Additional notes: {extra_notes}.
            The user has the following health profile / conditions: {profile_text}. 
            You MUST autonomously deduce what foods are recommended, forbidden, or accepted for these specific conditions and ensure the menu perfectly respects their medical requirements!
            CRITICAL INSTRUCTIONS:
            - YOU MUST USE the `search_nutrition_db` tool to find real products and their exact macros before constructing the menu!
            - ALWAYS output exactly as a JSON array of objects. DO NOT OUTPUT MARKDOWN. DO NOT OUTPUT ANY TEXT EXCEPT JSON.
            - JSON Format required:
            [
                {{"meal": "Breakfast", "food": "100g Oatmeal with 50g berries", "calories": 300, "salt_mg": 10, "fat_g": 5, "iron_mg": 2}}
            ]
            - Ensure the total calories sum up closely to {target_cal}.
            """
            
            temp_messages = [{'role': 'system', 'content': sys_prompt}, {'role': 'user', 'content': 'Generate my meal plan. Find real foods from the DB.'}]
            response = ollama.chat(model='llama3', messages=temp_messages, tools=[search_tool_schema, db_search_tool_schema])
            
            # Simple loop to handle multiple tool calls (up to 3 times to prevent infinite loops)
            for _ in range(3):
                if response.get('message', {}).get('tool_calls'):
                    temp_messages.append(response['message'])
                    for tool in response['message']['tool_calls']:
                        if tool['function']['name'] == 'local_web_search':
                            query_arg = tool['function']['arguments'].get('query')
                            st.info(f"🔍 Planner Web Search triggered for: '{query_arg}'")
                            search_data = local_web_search(query_arg)
                            temp_messages.append({'role': 'tool', 'content': search_data, 'name': 'local_web_search'})
                        elif tool['function']['name'] == 'search_nutrition_db':
                            query_arg = tool['function']['arguments'].get('query')
                            st.info(f"🗄️ Planner DB Search triggered for: '{query_arg}'")
                            db_data = search_nutrition_db(query_arg)
                            temp_messages.append({'role': 'tool', 'content': db_data, 'name': 'search_nutrition_db'})
                    
                    response = ollama.chat(model='llama3', messages=temp_messages, tools=[search_tool_schema, db_search_tool_schema])
                else:
                    break
                    
            import json
            raw_text = response['message']['content']
            raw_text = re.sub(r'\[TOOL_CALLS\]\s*\[.*?\]', '', raw_text).strip()
            
            try:
                start_idx = raw_text.find('[')
                end_idx = raw_text.rfind(']') + 1
                if start_idx != -1 and end_idx != -1:
                    json_data = json.loads(raw_text[start_idx:end_idx])
                    df_plan = pd.DataFrame(json_data)
                    
                    total_cals = df_plan['calories'].sum() if 'calories' in df_plan else 0
                    total_salt = df_plan['salt_mg'].sum() if 'salt_mg' in df_plan else 0
                    total_fat = df_plan['fat_g'].sum() if 'fat_g' in df_plan else 0
                    total_iron = df_plan['iron_mg'].sum() if 'iron_mg' in df_plan else 0
                    
                    total_row = pd.DataFrame([{"meal": "TOTAL", "food": "---", "calories": total_cals, "salt_mg": total_salt, "fat_g": total_fat, "iron_mg": total_iron}])
                    df_plan = pd.concat([df_plan, total_row], ignore_index=True)
                    
                    st.dataframe(df_plan, use_container_width=True)
                    if abs(total_cals - target_cal) > 200:
                        st.warning(f"Note: Total calories ({total_cals}) differ from your target ({target_cal}).")
                else:
                    st.error("AI failed to output valid JSON. Raw output:")
                    st.text(raw_text)
            except Exception as e:
                st.error(f"Failed to parse AI output: {e}")
                st.text(raw_text)

if conn_reader: conn_reader.close()
