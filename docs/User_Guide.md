# $Id: 03cbc893f143c3ae43fc35e97913bedb89b41e23 Lange François lanfr144@school.lu 2026/06/11 10:38:26 Lange François lanfr144@school.lu 2026/06/11 10:38:26   [#1] chore: fix git-ident-filter self-modification regex bug by concatenating search strings [PreRelease-1.0-28-g03cbc89] $
# User Guide

## 1. Clinical Data Search
Search for products using keywords. The system utilizes FULLTEXT matching to instantly return the top 10 relevant matches alongside macronutrient data.

## 2. My Plate Builder
Add portion sizes of different foods to calculate cumulative nutritional intake. Use the 🗑️ icon to remove items.

## 3. Chat with AI
Ask the `qwen2.5:7b` model complex dietary questions. It natively utilizes RAG Tool Calling to silently search the database and formulate clinical answers.
