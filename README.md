# Local Food AI 🍔

A strictly local, privacy-first AI Medical Dietitian and Food Explorer. This project leverages the OpenFoodFacts dataset and local LLMs (Ollama) to provide medically sound dietary advice, recipe parsing, and menu planning without sending any user data to the cloud.

## Features
- **Dynamic Medical Profiling**: Configure your health profile (e.g., Kidney issues, pregnancy, vegan). The AI dynamically adjusts all responses, recommendations, and warnings based on these exact medical needs.
- **RAG Architecture**: The AI is connected to a massively partitioned local MySQL database. When you ask a question or request a meal plan, the AI executes SQL queries autonomously to fetch precise nutritional data.
- **SearXNG Web Integration**: When the local Database lacks culinary heuristics, the AI securely queries a local, private instance of SearXNG to answer questions without compromising patient privacy.
- **Plate Builder & Unit Conversion**: Input culinary recipes (e.g., "1.5 cups of flour") and the system converts them to metric standard weights based on the product's density.
- **Distributed Microservice Topology**: Supports decoupling across VirtualBox, Hyper-V, and WSL2 using Bridged Networking and SNMP container telemetry for Zabbix.

## Documentation (Capstone Deliverables)
Please refer to the `docs/` folder for detailed guides:
- [Architecture Map](docs/architecture.md)
- [Distributed Deployment Procedure (PoC)](docs/distributed_deployment.md)
- [Disaster Recovery & Backup Plan](docs/disaster_recovery_plan.md)
- [Zabbix Telemetry Guide](docs/zabbix_monitoring.md)
- [Agile Retro Planning](docs/retro_planning.md)
- [Taiga Final Audit Report](docs/taiga_audit_report.md)

## Tech Stack
- **Frontend**: Streamlit
- **Database**: MySQL 8.0
- **AI Engine**: Ollama (Llama 3.2:1B)
- **Web Search**: SearXNG
- **Monitoring**: Zabbix (SNMPv2c)
- **Deployment**: Native Ubuntu, Docker Compose, Hyper-V / VirtualBox
- **Project Management**: Taiga (Synced dynamically via Python)
