# Local Food AI 🍔

A strictly local, privacy-first AI Medical Dietitian and Food Explorer. This project leverages the OpenFoodFacts dataset and local LLMs (Ollama) to provide medically sound dietary advice, recipe parsing, and menu planning without sending any user data to the cloud.

## Features
- **Dynamic Medical Profiling**: Configure your health profile (e.g., Kidney issues, pregnancy, vegan). The AI dynamically adjusts all responses, recommendations, and warnings based on these exact medical needs.
- **RAG Architecture**: The AI is connected to a massively partitioned local MySQL database. When you ask a question or request a meal plan, the AI executes SQL queries autonomously to fetch precise nutritional data.
- **Plate Builder & Unit Conversion**: Input culinary recipes (e.g., "1.5 cups of flour") and the system converts them to metric standard weights based on the product's density.
- **High-Performance Database**: Implements Grouped Vertical Partitioning to bypass InnoDB limits, featuring `FULLTEXT` indexing for lightning-fast search capabilities across millions of foods.

## Documentation
Please refer to the `docs/` folder for detailed guides:
- [Installation Guide](docs/Installation_Guide.md)
- [User Guide](docs/User_Guide.md)
- [Data Ingestion Guide](docs/Data_Ingestion.md)

## Tech Stack
- **Frontend**: Streamlit
- **Database**: MySQL 8.0
- **AI Engine**: Ollama (Mistral / Llama3)
- **Deployment**: Native Ubuntu, Docker, Kubernetes
- **Project Management**: Taiga (Synced dynamically via Python)
