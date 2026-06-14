import os

readme_path = 'README.md'
try:
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # We locate the ## Grading header and everything after it, and replace it
    idx = content.find('## Grading')
    if idx == -1:
        idx = content.find('Grading')
        
    if idx != -1:
        content = content[:idx]
    
    exact_grading = """Grading
There will be 6 grades in total: 3 for Project Management 1 (PM1) and 3 for Domain-specifc Project 1 (DSP1).

PM1:

Requirements analysis and assessment.
Overall project planning and execution.
Project presentation.
DSP1:

The final product shipped to the customer.
The product documentation:
Technical document, explaining how to install and configure the final product as well as the technologies used (LLM, DB, etc.) for an IT audience. Explain which Antigravity models you used for which tasks as well as how and why you configured agent permissions. Also reflect on what Antigravity struggled with and you handled this. Explain which local LLM the app uses and why. Explain the app infrastructure via a diagram showing how the app components communicate locally. Explain how you've verified that no user data leaves the server.
User manual, explaining how to use the final product from an end user (non developer) perspective.
The presentation to the customer."""

    content = content.rstrip() + "\n\n" + exact_grading + "\n"
    
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Successfully updated README.md with exact grading text!")
except Exception as e:
    print(f"Error: {e}")
