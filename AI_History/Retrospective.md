# Agile Sprint Retrospective
**Project:** Local Food AI Platform
**Sprint Goal:** Secure Data Ingestion, Medical Expansion, and UI/UX Overhaul

## 🏆 What Went Well
* **Database Agility:** Transitioning from rigid SQL arrays to dynamic pandas DataFrame ingestion (`ingest_csv.py`) allowed us to process massive OpenFoodFacts schemas instantly without crashing.
* **Privacy-First Architecture:** Successfully establishing an air-gapped system where the AI scraper (SearXNG) and the Large Language Model (Mistral) operate entirely locally proves extreme Corporate Data Sovereignty.
* **Rapid Feature Integration:** Expanding the platform from a simple calculator to a full-fledged Clinical Profiler (incorporating Diabetes, Hypertension, and Pregnancy monitoring) was achieved incredibly fast using Pandas styling logic.

## 🚧 What Went Wrong (Or Needed Improvement)
* **Dataset Encoding Bugs:** The OpenFoodFacts CSV files contain heavy French datasets. Early ingestion attempts on Windows corrupted characters (`'Artichaut' -> 'Artichaut'`) due to OS-default rendering limitations over `utf-8`. This required an urgent hotfix in the data pipeline.
* **Schema Scalability:** Constantly injecting new tables (`plates`, `user_profiles`) into `setup_db.py` without a formal migration tool (like Alembic) makes iterative DevOps slightly dangerous for live production data.

## 🎯 Action Items for Next Sprint
* Implement a formal database schema migration tool (Flyway or Alembic) to prevent data loss during continuous integration.
* Optimize the SQL parsing speed by adding specific integer boundaries to the B-TREE indexes.
* Deploy an actual external SMTP server (e.g., Postfix/Sendgrid) to fully operationalize the mocked password-reset pipeline.
