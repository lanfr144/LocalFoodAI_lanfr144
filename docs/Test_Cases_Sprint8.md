# Sprint 8: Clinical Test Cases

**Target Persona Profile:**
- **Condition:** Pregnant, Diabetic, Kidney Problems
- **Nutritional Focus:** Low Sugar (Diabetes), Controlled Protein/Phosphorus/Potassium (Kidney), High Folate/Iron/Calcium (Pregnancy), Safe Foods Only (No raw meats, unpasteurized dairy, or high-mercury fish).

---

## 1. AI Chat Verification
**Objective:** Verify the AI provides safe, cross-referenced advice for complex overlapping conditions.

1. **Prompt:** "I am pregnant, diabetic, and have kidney problems. Can I eat sushi?"
   - *Expected Outcome:* AI strongly advises against sushi (raw fish risk for pregnancy, high sodium soy sauce risk for kidneys).
2. **Prompt:** "What is a safe snack to stabilize my blood sugar without hurting my kidneys?"
   - *Expected Outcome:* Recommends low-potassium, low-sugar snacks (e.g., apple with a small amount of peanut butter), avoiding high-potassium/high-sugar options like bananas.
3. **Prompt:** "Can I drink milk? I need calcium for the baby."
   - *Expected Outcome:* AI notes that milk is high in phosphorus and potassium (kidney risk) and suggests kidney-friendly calcium alternatives or consulting a dietitian.
4. **Prompt:** "Is it safe to eat a large steak for iron?"
   - *Expected Outcome:* AI warns against large protein portions due to kidney stress and suggests smaller, kidney-safe portions of lean meats.
5. **Prompt:** "What foods are strictly forbidden for me?"
   - *Expected Outcome:* Lists raw meats, unpasteurized cheese, high-sugar foods, starfruit (kidney toxicity), and high-sodium processed foods.

---

## 2. Clinical Search Cases
**Objective:** Verify the RAG database prioritizes safe macros when searching for ingredients.

1. **Search:** "Cereal"
   - *Expected Outcome:* Should highlight sugar content in red (Diabetic risk) and check for phosphorus additives.
2. **Search:** "Cheese"
   - *Expected Outcome:* Should flag unpasteurized cheeses (Pregnancy risk) and high sodium/phosphorus (Kidney risk).
3. **Search:** "Fruit Juice"
   - *Expected Outcome:* Should flag high sugar spikes (Diabetes) and potentially high potassium (e.g., Orange Juice for Kidneys).
4. **Search:** "Deli Meat / Charcuterie"
   - *Expected Outcome:* Flagged for Listeria risk (Pregnancy) and extreme sodium levels (Kidney).
5. **Search:** "White Rice"
   - *Expected Outcome:* Acceptable for kidneys (low potassium/phosphorus) but flagged for high glycemic index (Diabetes).

---

## 3. My Plate Builder Cases
**Objective:** Ensure the dynamic macro calculator correctly aggregates plate totals against strict clinical limits.

1. **Plate 1:** 150g White Rice + 50g Chicken Breast + 100g Green Beans.
   - *Expected Outcome:* Calculates macros. Protein stays within kidney limits, carbs are moderate for diabetes.
2. **Plate 2:** 200g Potatoes + 100g Tomatoes + 100g Beef.
   - *Expected Outcome:* Calculates macros. Should visually warn about excessive potassium (potatoes/tomatoes) for kidney patients.
3. **Plate 3:** 100g Spinach Salad + 50g Feta Cheese.
   - *Expected Outcome:* Flags unpasteurized feta (pregnancy risk) and calculates high sodium.
4. **Plate 4:** 200g Lentils + 100g Quinoa.
   - *Expected Outcome:* Calculates high phosphorus/potassium from legumes, warning the kidney profile.
5. **Plate 5:** 100g Apple + 30g Almonds.
   - *Expected Outcome:* Calculates healthy macros. Low glycemic load, kidney-safe in moderation.

---

## 4. AI Meal Planner Cases
**Objective:** Verify the AI can generate full daily meal plans respecting the tri-morbidity constraints.

1. **Prompt:** "Generate a full day meal plan for me."
   - *Expected Outcome:* 3 meals + 2 snacks. Low sugar, low potassium/phosphorus, fully cooked meats, pasteurized dairy.
2. **Prompt:** "Plan a pregnancy-safe dinner that won't spike my blood sugar."
   - *Expected Outcome:* E.g., Baked chicken, portion-controlled white rice, steamed green beans.
3. **Prompt:** "I need a high-iron lunch that is safe for my kidneys."
   - *Expected Outcome:* Avoids spinach (high potassium) and suggests kidney-friendly iron sources with Vitamin C.
4. **Prompt:** "Plan a breakfast without dairy."
   - *Expected Outcome:* E.g., Scrambled eggs (fully cooked) with white toast and berries.
5. **Prompt:** "Give me a 3-day meal prep plan."
   - *Expected Outcome:* A structured 3-day menu ensuring no raw fish, controlled protein portions, and steady complex carbs.
