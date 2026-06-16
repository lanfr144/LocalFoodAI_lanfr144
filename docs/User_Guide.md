The current version is #ident "@(#)$Format:LocalFoodAI_lanfr144:User_Guide.md:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"


# Local Food AI - Clinician User Manual

Welcome to the **Local Food AI** clinical dietitian explorer. This guide explains how to use the platform to search for products, build custom recipe plates, calculate cumulative nutritional statistics, and consult the privacy-safe AI assistant.

---

## 1. Accessing the Application

To access the platform on your local network:
1. Open your web browser (Chrome, Firefox, or Safari).
2. Enter the host address provided by your IT administrator (e.g., `http://192.168.130.170:8502/` or `http://localhost:8502/`).
3. You will be greeted by the secure login screen.

---

## 2. Account Login & Security

To protect patient information, the system requires credentials:
* **Login**: Enter your standard clinician username and password.
* **Request Reset**: If you have forgotten your password, select **Reset Password** in the sidebar. Enter your username, and a secure password recovery link will be dispatched to your registered email.
* **Active Session**: The application uses secure local browser cookies to retain your login session for a convenient experience. Select **Logout** in the sidebar at any time to terminate your session.

---

## 3. Sidebar Features & Controls

The left-hand sidebar houses several global settings:
* **Network Status**: Visual indicator of whether you are in *Online/Server* mode or *Offline/Local Fallback* mode.
* **LLM Engine Status**: Displays the active local AI model being queried (e.g., `llama3.2:3b`).
* **Active User Info**: Shows the logged-in clinician profile.
* **Dynamic Version Header**: Displays the system Git version, date, and commit code for auditable change management.

---

## 4. Feature Guides

The application dashboard is split into three interactive workspace tabs:

### 4.1. Clinical Data Search Tab
Use this tab to browse the local OpenFoodFacts food database.
1. **Keyword Input**: Type a product name, brand, or barcode (e.g., "whole wheat bread" or "unpasteurized cheese").
2. **Dynamic Results**: The database performs a rapid search, displaying the top 10 matched products.
3. **Nutritional Score**: Shows the Nutri-Score grade (A to E) and details (Proteins, Carbs, Fats, Energy in kcal) per 100g.
4. **Allergen Warnings**: Shows highlight flags if the product contains common allergens matching your client's needs.

### 4.2. My Plate Builder Tab
Build custom meals or recipe portions to calculate total client nutritional intake.
1. **Adding Items**: When browsing foods in the Search Tab, click **Add to Plate**.
2. **Specifying Portions**: Input the quantity using either decimal weights (in grams) or common volume descriptors (e.g., "1.5 cups", "2 tablespoons"). The converter translates volume to metric weight based on the product density.
3. **Cumulative Intake Table**: The tab renders a table summarizing individual macros and total energy.
4. **Visual Metrics**: Renders a dynamic bar chart comparing Carbs, Proteins, and Fats against recommended clinical intake thresholds.
5. **Editing the Plate**: Use the trash bin icon (Delete) to instantly remove any item from the calculation.

### 4.3. Consultation Chat Tab
Consult the built-in clinical AI dietitian assistant for recipe validation, medical profile warnings, and meal plans.
1. **Client Profile Selection**: Select active dietary constraints (e.g., pregnancy, diabetes, kidney disease, vegetarian) in the dropdown.
2. **Asking Questions**: Type your prompt (e.g., "Is unpasteurized brie cheese safe for a pregnant client?" or "Design a low-sodium, high-protein menu").
3. **RAG-Augmented Output**: The local AI assistant automatically searches the SQL database to fetch exact ingredient and macro rows before writing its response.
4. **Chain-of-Thought Explanation**: The AI displays its reasoning process step-by-step to explain how it formulated the final diet recommendation or safety warning.

---

## 5. Privacy and Offline Support

Because patient privacy is critical:
* **No Cloud Overhead**: All search strings, chat prompts, and plate records are processed locally inside the host node.
* **Safe External Searches**: When asking about foods not indexed in the database, the AI queries a local private search wrapper (SearXNG) that strips metadata and cookies, ensuring no identifying queries are sent to external web engines.
