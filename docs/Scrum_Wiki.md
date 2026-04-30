# Local Food AI - Agile Scrum Wiki

This document outlines the Agile methodologies, specifically the Scrum framework rituals, utilized during the lifecycle of the Local Food AI project.

## 1. Sprint Planning
**Frequency:** Start of every Sprint (Weekly).
**Participants:** Product Owner (Customer), Scrum Master, Development Team.
**Objective:** 
- Define the Sprint Goal.
- Review and prioritize the Product Backlog in Taiga.
- Estimate User Stories (using story points or hours).
- Select User Stories to form the Sprint Backlog.
- Break down selected User Stories into actionable Technical Tasks.

## 2. Daily Scrum (Stand-up)
**Frequency:** Daily (15 minutes time-boxed).
**Participants:** Development Team, Scrum Master.
**Objective:** 
To synchronize activities and create a plan for the next 24 hours. Each member answers three questions:
1. *What did I do yesterday that helped the Development Team meet the Sprint Goal?*
2. *What will I do today to help the Development Team meet the Sprint Goal?*
3. *Do I see any impediment that prevents me or the Development Team from meeting the Sprint Goal?*

## 3. Sprint Review
**Frequency:** End of every Sprint.
**Participants:** Scrum Team, Stakeholders (Customer).
**Objective:** 
- Inspect the Increment (the completed work).
- Demonstrate new features (e.g., Zabbix Integration, Medical AI Chat).
- Adapt the Product Backlog if needed.
- Gather feedback from the stakeholders to ensure the project remains aligned with their needs.

## 4. Sprint Retrospective
**Frequency:** End of every Sprint, immediately following the Sprint Review.
**Participants:** Scrum Team.
**Objective:** 
To identify areas of improvement for the upcoming Sprint.
- **What went well?** (e.g., "Dockerizing Zabbix reduced deployment time.")
- **What didn't go well?** (e.g., "SQL schema initialization was brittle.")
- **Actionable improvements:** (e.g., "Implement `SET GLOBAL log_bin_trust_function_creators = 1` permanently.")

## 5. Artifacts Used
- **Taiga Platform:** Used for managing the Product Backlog, Sprint Backlog, and Kanban board.
- **GitHub:** Used for version control, code review, and CI/CD pipelines.
- **Documentation:** The `docs/` folder maintains the Ground Truth architectural state.
