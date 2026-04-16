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
        f.write(f"## Sprint Planning {sprint_str} {sprint_start.strftime('%Y/%m/%d')}\n")
        f.write("- Planning notes...\n\n")
        
        # Daily Scrums
        for d in range(5):
            day_date = sprint_start + timedelta(days=d)
            f.write(f"### Daily Scrum {day_date.strftime('%Y/%m/%d')}\n")
            f.write("- **evegi144**: \n")
            f.write("- **francois**: \n\n")
            
        # Sprint Review
        f.write(f"## Sprint Reviews {sprint_str} {sprint_end.strftime('%Y/%m/%d')}\n")
        f.write("- Review notes...\n\n")
        
        # Sprint Retrospective
        f.write(f"## Sprint Retrospective {sprint_str} {sprint_end.strftime('%Y/%m/%d')}\n")
        f.write("- Retrospective notes...\n\n")

print("Files generated successfully in taiga_wiki/")
