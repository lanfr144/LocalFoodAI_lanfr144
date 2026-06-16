The current version is #ident "@(#)$Format:LocalFoodAI_lanfr144:User_Description.md:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"


# Local Food AI - User Description & Functional Guide

## 1. System Vision
The **Local Food AI** system is a strictly local, privacy-first, professional-grade clinical dietetics assistant. Developed specifically for clinics and healthcare practitioners, it provides offline nutritional analysis, meal planning, and warning flags based on dynamic patient health profiles. 

Since the system operates entirely locally on local hypervisors, **zero patient medical data or search queries ever leave the server boundary**, ensuring 100% HIPAA compliance and data sovereignty.

---

## 2. Core Functional Pillars

### 📊 tab 1: Clinical Data Search (🔬 Clinical Search)
Allows practitioners to search the 24GB OpenFoodFacts dataset in real time (average query response time < 0.04 seconds).
- **Dynamic Medical Warnings**: Based on the active patient profile, foods are immediately flagged in the search results:
  - ⚠️ **Red Warning Flags**: Highlight high-risk ingredients (e.g. Unpasteurized dairy or raw fish for pregnant patients, high-sodium foods for hypertensive patients, or high-sugar foods for diabetic patients).
  - 💚 **Green Recommendations**: Highlight recommended dietary components (e.g. High iron/calcium for pregnant or breastfeeding mothers, high Vitamin C for scurvy prevention, or high iron for anemia).
- **Flexible Column Customization**: Multi-select column headers to inspect specific macro and micro-nutrients.

### 💬 tab 2: AI Clinical Chat (💬 AI Chat)
An interactive NLP dialogue interface powered by a local lightweight LLM (**Qwen2.5:7b**).
- **RAG-Driven Precision**: The AI dietitian automatically retrieves and reviews local database records and private meta-search results before formulating an answer.
- **Dynamic Medical Guardrails**: The user's active illnesses, diets, and conditions are injected into the AI's system prompt in the background, forcing the AI to strictly enforce clinical safety constraints.

### 🍽️ tab 3: My Plate Builder (🍽️ My Plate Builder)
A recipe formulation utility to calculate combined nutritional intake.
- **Natural Language Parsing**: Enables entering quantities in natural units (e.g., "1.5 cups", "2 tablespoons", "150g").
- **Exact Conversion**: The system translates these custom units into metric grams based on product density metrics.
- **Macro Summaries**: Instantly calculates and displays the total combined Protein, Fat, and Carbohydrates.

### 🤖 tab 4: AI Meal Planner (🤖 AI Meal Planner)
An automated clinical diet planner.
- Generates a multi-meal daily menu formatted strictly as a Markdown table.
- Dynamically enforces user-defined calorie limits and active medical restrictions.

---

## 3. Supported Health & Medical Profiles
- **Conditions**: Pregnant, Breastfeeding, Low Fat, Osteoporosis.
- **Illnesses**: Diabetes, Hypertension, Kidney Disease, Scurvy, Anemia.
- **Diets**: Vegan, Vegetarian, Kosher, Halal, Keto, Paleo, Christian (Lent/Good Friday).
