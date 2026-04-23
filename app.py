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

def get_db_connection(login_path):
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
        send_email(email, "Welcome to Local Food AI", f"Hello {username}, your account was securely created!")
        return True
    except pymysql.err.IntegrityError:
        return False

def send_email(to_email, subject, body):
    try:
        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = "security@localfoodai.com"
        msg['To'] = to_email
        s = smtplib.SMTP('localhost', 25)
        s.send_message(msg)
        s.quit()
    except Exception:
        print(f"Mock SMTP -> Sent to {to_email} | Subject: {subject}")

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
            send_email(email, "Password Reset", f"Your new temporary password is: {new_pass}")
            return True
    return False

# UI Theming
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
            l_user = st.text_input("Username", key="l_user")
            l_pass = st.text_input("Password", type="password", key="l_pass")
            if st.button("Login"):
                if verify_login(l_user, l_pass):
                    st.session_state["authenticated_user"] = l_user
                    st.rerun()
                else: st.error("Invalid login.")
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
                if reset_password(f_user, f_email): st.success("Password reset emailed.")
                else: st.error("Failed.")

if not st.session_state["authenticated_user"]:
    st.title("🍔 Food AI Medical Explorer")
    st.info("Please login to interrogate the Clinical Data.")
    st.stop()

st.title("🍔 Food AI Clinical Explorer")
conn_reader = get_db_connection('app_reader')

tab_chat, tab_explore, tab_plate, tab_planner = st.tabs(["💬 AI Chat", "🔬 Clinical Search", "🍽️ My Plate Builder", "🤖 AI Meal Planner"])

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
        with st.spinner("Analyzing..."):
            try:
                temp_messages = [{"role": "system", "content": sys_prompt}] + [m for m in st.session_state.messages if m["role"] != "tool"]
                response = ollama.chat(model='mistral', messages=temp_messages, tools=[search_tool_schema])
                
                if response.get('message', {}).get('tool_calls'):
                    for tool in response['message']['tool_calls']:
                        if tool['function']['name'] == 'local_web_search':
                            query_arg = tool['function']['arguments'].get('query')
                            st.info(f"🔍 Web Search triggered for: '{query_arg}'")
                            search_data = local_web_search(query_arg)
                            st.session_state.messages.append(response['message'])
                            st.session_state.messages.append({'role': 'tool', 'content': search_data, 'name': 'local_web_search'})
                            temp_messages = [{"role": "system", "content": sys_prompt}] + st.session_state.messages
                            response = ollama.chat(model='mistral', messages=temp_messages)
                ai_reply = response['message']['content']
            except Exception as e: ai_reply = f"Hold on! Engine execution fault: {e}"

        st.session_state.messages.append({"role": "assistant", "content": ai_reply})
        st.chat_message("assistant").write(ai_reply)

def highlight_medical_warnings(row):
    if '⚠️' in str(row.get('Medical Warning', '')): return ['background-color: rgba(255, 0, 0, 0.4); color: white;'] * len(row)
    return [''] * len(row)

with tab_explore:
    st.subheader("Clinical Data Search")
    sq = st.text_input("Search Product Name or Ingredient")
    cols = st.columns(5)
    min_pro = cols[0].number_input("Min Protein (g)", 0, 1000, 0)
    min_fat = cols[1].number_input("Min Fat (g)", 0, 1000, 0)
    min_carb = cols[2].number_input("Min Carbs (g)", 0, 1000, 0)
    max_sug = cols[3].number_input("Max Sugar (g)", 0, 1000, 1000)
    
    # Load dynamically fetched limit as index 
    opts = [10, 20, 50, 100, "All"]
    user_lim_str = get_user_limit(st.session_state["authenticated_user"])
    user_lim_val = "All" if user_lim_str == "All" else int(user_lim_str)
    idx = opts.index(user_lim_val) if user_lim_val in opts else 2
    limit_rc = cols[4].selectbox("Limit Results", opts, index=idx)
    
    if st.button("Search Database") and sq and conn_reader:
        with st.spinner("Processing massive clinical query..."):
            try:
                with conn_reader.cursor() as cursor:
                    l_str = "" if limit_rc == "All" else f"LIMIT {limit_rc}"
                    query = f"""
                        SELECT code, product_name, generic_name, brands, allergens, ingredients_text,
                               proteins_100g, fat_100g, carbohydrates_100g, sugars_100g, sodium_100g, energy_kcal_100g
                        FROM products 
                        WHERE MATCH(product_name, ingredients_text) AGAINST(%s IN NATURAL LANGUAGE MODE)
                        AND (proteins_100g >= %s OR proteins_100g IS NULL)
                        AND (fat_100g >= %s OR fat_100g IS NULL)
                        AND (carbohydrates_100g >= %s OR carbohydrates_100g IS NULL)
                        AND (sugars_100g <= %s OR sugars_100g IS NULL)
                        {l_str}
                    """
                    cursor.execute(query, (sq, min_pro, min_fat, min_carb, max_sug))
                    results = cursor.fetchall()
                    
                    if results:
                        # Fetch EAV Medical Profile
                        eav_profile = get_eav_profile(st.session_state["authenticated_user"])
                        df = pd.DataFrame(results)
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
                                    if val == 'diabetes' and pd.notnull(row['sugars_100g']) and float(row['sugars_100g']) > 10.0:
                                        warns.append("⚠️ High Sugar (Diabetes)")
                                    if (val == 'hypertension' or val == 'high bp') and pd.notnull(row['sodium_100g']) and float(row['sodium_100g']) > 1.5:
                                        warns.append("⚠️ High Salt (Hypertension)")
                                        
                                # Condition Analytics
                                if cat == 'condition':
                                    if val == 'pregnant' and ('cru' in ing_text or 'raw' in ing_text or 'viande crue' in ing_text):
                                        warns.append("⚠️ Raw Foods (Pregnancy Toxoplasmosis)")
                                    if val == 'low fat' and pd.notnull(row['fat_100g']) and float(row['fat_100g']) > 20.0:
                                        warns.append("⚠️ High Fat")
                                        
                                # Dietary Analytics (Best-Effort Keyword Filters)
                                if cat == 'diet':
                                    if val in ['vegan', 'kosher', 'halal']:
                                        if val not in ing_text:
                                            warns.append(f"⚠️ Cannot verify {val.title()} compliance. Please check manual label.")
                                        if val == 'vegan' and ('lait' in ing_text or 'milk' in ing_text or 'oeuf' in ing_text or 'egg' in ing_text or 'meat' in ing_text or 'viande' in ing_text):
                                            warns.append("⚠️ Contains Animal Products (Not Vegan)")
                                        if val == 'halal' and ('porc' in ing_text or 'gelatin' in ing_text or 'vin' in ing_text or 'wine' in ing_text):
                                            warns.append("⚠️ Probable Haram Ingredients (e.g. Pork/Wine)")
                                            
                                # Simple Exclusion List Analytics
                                if cat in ['dislike', 'allergy']:
                                    if val in ing_text or val in all_text:
                                        warns.append(f"⚠️ Contains: {val.upper()}")
                                        
                            warnings_col.append(" | ".join(list(set(warns))) if warns else "✅ Safe for Profile")
                            
                        df.insert(0, 'Medical Warning', warnings_col)
                        styled_df = df.style.apply(highlight_medical_warnings, axis=1)

                        st.success(f"Analysed {len(results)} records utilizing dynamic EAV parameters.")
                        st.dataframe(styled_df, use_container_width=True)
                    else:
                        st.warning("No products found matching those strict terms.")
            except Exception as e: st.error(f"SQL/Pandas Error: {e}")

with tab_plate:
    st.subheader("🍽️ My Plate Builder")
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
                    st.rerun()

            if plates:
                selected_plate = st.selectbox("Select Active Plate", [p['plate_name'] for p in plates])
                active_p_id = next(p['id'] for p in plates if p['plate_name'] == selected_plate)
                
                cursor.execute("""
                    SELECT i.id, i.product_code, i.quantity_grams, p.product_name, p.proteins_100g, p.fat_100g, p.carbohydrates_100g 
                    FROM plate_items i LEFT JOIN products p ON i.product_code = p.code WHERE i.plate_id = %s
                """, (active_p_id,))
                items = cursor.fetchall()
                if items:
                    st.dataframe(items, use_container_width=True)
                    total_pro = sum((float(i['proteins_100g'] or 0) * (float(i['quantity_grams'])/100.0)) for i in items)
                    total_fat = sum((float(i['fat_100g'] or 0) * (float(i['quantity_grams'])/100.0)) for i in items)
                    total_carb = sum((float(i['carbohydrates_100g'] or 0) * (float(i['quantity_grams'])/100.0)) for i in items)
                    st.info(f"**Total Protein:** {total_pro:.1f}g | **Total Fat:** {total_fat:.1f}g | **Total Carbs:** {total_carb:.1f}g")
                
                st.markdown("---")
                add_code = st.text_input("Enter exact Product `code`")
                add_grams = st.number_input("Portion Quantity (Grams)", min_value=1.0, value=100.0)
                if st.button("Add Item"):
                    cursor.execute("INSERT INTO plate_items (plate_id, product_code, quantity_grams) VALUES (%s, %s, %s)", 
                                  (active_p_id, add_code, add_grams))
                    conn.commit()
                    st.rerun()

with tab_planner:
    st.subheader("🤖 AI Meal Planner")
    p_col1, p_col2, p_col3 = st.columns(3)
    target_cal = p_col1.number_input("Target Daily Calories (kcal)", 1000, 5000, 2000, 50)
    diet_pref = p_col2.selectbox("Dietary Preference", ["Omnivore", "Vegetarian", "Vegan", "Keto", "Paleo"])
    meal_count = p_col3.slider("Number of Meals", 2, 6, 3)
    extra_notes = st.text_input("Any additional allergies or goals?")
    
    if st.button("Generate Professional Menu"):
        with st.spinner("AI is formulating..."):
            sys_prompt = f"Dietitian planner. {diet_pref}, {target_cal}kcal, {meal_count} meals. Notes: {extra_notes}. OUTPUT AS STRICT MARKDOWN TABLE."
            response = ollama.chat(model='mistral', messages=[{'role': 'system', 'content': sys_prompt}, {'role': 'user', 'content': 'Generate menu'}])
            st.markdown(response['message']['content'])

if conn_reader: conn_reader.close()
