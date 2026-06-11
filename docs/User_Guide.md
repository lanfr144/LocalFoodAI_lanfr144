The current version is #ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"

# $Id$
# User Guide

## 1. Clinical Data Search
Search for products using keywords. The system utilizes FULLTEXT matching to instantly return the top 10 relevant matches alongside macronutrient data.

## 2. My Plate Builder
Add portion sizes of different foods to calculate cumulative nutritional intake. Use the 🗑️ icon to remove items.

## 3. Chat with AI
Ask the `qwen2.5:7b` model complex dietary questions. It natively utilizes RAG Tool Calling to silently search the database and formulate clinical answers.