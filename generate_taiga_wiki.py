import os
from datetime import datetime, timedelta

os.makedirs('taiga_wiki', exist_ok=True)

start_date = datetime(2026, 4, 16)
sprints = 8
points_per_sprint = 1000

# 00_Epics.md
with open('taiga_wiki/00_Epics.md', 'w') as f:
    f.write("# Project Epics\n\n1. Environment & Infrastructure Setup\n2. Database Schema & User Security\n3. Data Ingestion Pipeline\n4. Advanced Text & Context Search\n5. Local LLM Integration (Ollama)\n6. Streamlit Chat Interface Development\n7. Testing & Refinement\n8. Production Deployment\n")

for i in range(1, sprints + 1):
    sprint_start = start_date + timedelta(weeks=i-1)
    sprint_end = sprint_start + timedelta(days=6)
    sprint_str = f"Sprint_{i}"
    
    file_path = f"taiga_wiki/Sprint_{i}.md"
    with open(file_path, 'w') as f:
        f.write(f"# Sprint {i}\n\n")
        f.write(f"**Sprint Tag**: {sprint_str}\n")
        f.write(f"**Story Points**: {points_per_sprint}\n")
        f.write(f"**Members**: francois, evegi144\n\n")
        
        # Sprint Planning
        f.write(f"## {sprint_start.strftime('%Y/%m/%d')} Planning\n")
        if i == 1:
            f.write("- [x] Initialize Git Repo and configure AI History context.\n")
            f.write("- [x] Setup Taiga Wiki and Backlog generation.\n")
            f.write("- [x] Finalize `deploy.sh` and Database Setup (`init.sql`, `setup_db.py`).\n")
            f.write("- [x] Data Ingestion Pipeline (`ingest_csv.py`, `convert_datatypes.py`).\n")
            f.write("- [x] Build basic Streamlit Base App (`app.py`).\n\n")
        else:
            f.write("- Planning notes...\n\n")
        
        # Daily Scrums
        for d in range(5):
            day_date = sprint_start + timedelta(days=d)
            f.write(f"### {day_date.strftime('%Y/%m/%d')} Daily Scrum\n")
            f.write("- **evegi144**: \n")
            if i == 1 and d == 0:
                f.write("- **francois**: Set up git, database, and ingestion scripts.\n\n")
            else:
                f.write("- **francois**: \n\n")
            
        # Sprint Review
        f.write(f"## {sprint_end.strftime('%Y/%m/%d')} Review\n")
        if i == 1:
            f.write("- **Review**: Successfully pushed all foundational files to Git and configured DB schemas.\n\n")
        else:
            f.write("- Review notes...\n\n")
        
        # Sprint Retrospective
        f.write(f"## {sprint_end.strftime('%Y/%m/%d')} Retrospective\n")
        if i == 1:
            f.write("- **Retrospective**: Good velocity. Environment setup went smoothly.\n\n")
        else:
            f.write("- Retrospective notes...\n\n")

print("Files generated successfully in taiga_wiki/")
