# Premium UI Overhaul & "My Plate" Combinations Plan

Now that our backend is perfectly scaled, we need to focus heavily on the **Frontend Experience** to completely conquer User Stories `#5, #6, #7,` and `#8`. The goal is to evolve the currently simple Streamlit layout into a stunning, glassmorphic, premium "Web Application" feel, while unlocking the ability to save custom food combinations.

## User Review Required

Because Streamlit natively lacks advanced multi-table relational persistence, we must add new tables to MySQL to save a user's food lists permanently across sessions. **Are you okay with me modifying `setup_db.py` to add `plates` and `plate_items` tables, and does the proposed Premium UI style match your vision?**

## Proposed Changes

### 1. Database Persistence ("My Plates")
We will add two cleanly structured tables right after the `users` table logic:
- **`plates`**: Stores `id`, `user_id` (foreign key), and `plate_name`.
- **`plate_items`**: Stores `id`, `plate_id` (foreign key), `product_code`, and `grams`.
*This solves Story #8 perfectly without breaking existing data.*

### 2. Premium Aesthetics & Logic Overhaul
**Premium CSS Styling:** I will inject a massive `<style>` block to enforce a **curated dark mode**, smooth gradients, glassmorphic container aesthetics, modern typography *(e.g., Google's 'Inter')*, and micro-animations on interactive elements to ensure the project looks like an absolute state-of-the-art enterprise app.

**Nutritional Search Filters (Story #6):** 
I will add sleek Streamlit sliders and multi-select dropdowns to the "Raw Data Search" tab. Instead of just searching by name, you will be able to say: *"Show me foods with > 20g Protein and < 5g Sugar, sorted by energy."*

**My Plate Tab (Story #7):** 
I will build a dedicated 3rd Tab called "🍽️ My Plates" where users can:
- Create named plates (e.g., "Post-Workout Meal").
- Add searched foods directly to their active plate.
- Define the gram quantity for each item.
- The app will dynamically sum up the combined macro totals (Proteins, Carbs, Fats) across the entire plate locally using a Pandas aggregation over the grabbed SQL data!

## Open Questions

1. **Macro Priorities:** Are there specific macro nutrients (like Energy, Proteins, Fat, Sugars, Salt) that you want explicitly highlighted when viewing a "Combined Nutritional Value Overview" of a Plate, or should I attempt to dynamically graph as many as possible?
2. **Visual Theme:** Do you prefer a vibrant "Cyberpunk Dark Mode" or a more elegant "Sleek Dark Medical/Scientific" aesthetic with softer blues and greens?
