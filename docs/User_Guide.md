# User Guide: Local Food AI

Welcome to the **Local Food AI** medical explorer application. This guide will explain how to utilize the various modules within the Streamlit interface.

## 🔐 1. User Authentication & Profiling
When you launch the application, you will be greeted by the Login portal.
- **Register**: Create a secure account (passwords are Bcrypt hashed).
- **Dynamic Health Profile**: Once logged in, navigate to the sidebar to define your "EAV" (Entity-Attribute-Value) health profile.
  - You can add specific `Illnesses` (e.g., Diabetes), `Conditions` (e.g., Pregnant), or `Diets` (e.g., Vegan).
  - *This profile acts as the foundation for the AI.* The AI reads this profile dynamically to deduce which foods you can or cannot eat.

## 💬 2. AI Chat
The **AI Chat** tab allows you to speak conversationally with a clinical dietitian AI.
- **RAG Powered**: If you ask "Which foods are high in protein?", the AI will actively run SQL queries against your local OpenFoodFacts database to find verifiable answers.
- **Profile Aware**: The AI knows your health profile. If you have "Hypertension" registered, it will automatically warn you against high-sodium suggestions.

## 🔬 3. Clinical Search
The **Clinical Search** tab allows you to manually explore the massive 24GB dataset.
- Type any product name (e.g., "apple") and set your macro limits (Max Sugar, Min Protein).
- **AI Evaluation**: After loading a dataframe, click **"🤖 Ask AI to Evaluate This Table"**. The AI will analyze the visible rows against your active health profile and flag them as recommended or strictly forbidden!

## 🍽️ 4. My Plate Builder
Build recipes or daily plates.
- Search for a food by name.
- Input natural culinary measurements (e.g., "1.5 cups of flour", "2 tbsp of butter"). Our custom unit conversion engine will automatically translate this to metric grams based on the specific product's density and save it to your plate.

## 🤖 5. AI Meal Planner
Request full daily menus.
- Input your target calories (e.g., 2000 kcal) and diet preference.
- The AI will hit the database, find real products matching your needs, and construct a precise Markdown table (`| Meal | Food | Calories | Salt | Fat | Iron |`).
