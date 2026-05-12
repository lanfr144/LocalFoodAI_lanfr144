# Local Food AI: Retro Planning

*Document compiled in accordance with BTS-AI DOPRO Guidelines on Backward/Reverse Planning.*

## 1. Concept of Retro Planning
As defined in the course material, Retro Planning (Backward Planning) is constructed in reverse chronological order from a fixed deadline. This ensures that the D-Day (Capstone Submission) is immutably fixed, and all prior sprints and tasks are mathematically bound to ensure the feasibility of the project. 

Our delivery date is set for **May 15th, 2026**.

## 2. Reverse Chronological Timeline (Gantt Structure)

```mermaid
gantt
    title Local Food AI - Capstone Reverse Plan
    dateFormat  YYYY-MM-DD
    axisFormat  %m-%d

    section Delivery & Sign-off
    Final Capstone Submission   :milestone, m1, 2026-05-15, 0d
    Disaster Recovery & PoC Test:done, 2026-05-13, 2d
    Documentation Finalization  :done, 2026-05-11, 2d

    section Feature Freeze
    Web Search (SearXNG) Integration :done, 2026-05-12, 1d
    Medical Constraints & PDF Export :done, 2026-05-09, 3d
    AI Meal Planner (Ollama 1B)      :done, 2026-05-05, 4d

    section Core Architecture
    Plate Builder & Macros           :done, 2026-05-01, 4d
    Clinical Explorer Search         :done, 2026-04-28, 3d
    Zabbix Telemetry & SNMP          :done, 2026-04-26, 2d

    section Foundation
    OpenFoodFacts Ingestion (3GB)    :done, 2026-04-20, 6d
    Docker Multi-Container Setup     :done, 2026-04-18, 2d
    Taiga/Git Agile Integration      :done, 2026-04-15, 3d
```

## 3. Resource & Buffer Analysis
- **Milestone Buffers**: By utilizing a reverse plan, we identified that the massive 3GB OpenFoodFacts dataset required a 6-day window for background ingestion without blocking the frontend development. 
- **Leeway Analysis**: The final 2 days (May 13 - 15) are strictly reserved for Disaster Recovery (DR) drills and Multi-VM Proof of Concept (PoC) validation, ensuring the presentation runs flawlessly regardless of infrastructure hiccups.
