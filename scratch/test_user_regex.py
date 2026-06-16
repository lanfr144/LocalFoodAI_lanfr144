import re

pattern = r'\$F' + r'ormat:[^$]+\$'
content = """
                    if "$Format:LocalFoodAI:app.py:" in line:
                        match = re.search(r'\\$Format:LocalFoodAI_lanfr144:test_user_regex.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$', line)
"""

match = re.search(pattern, content)
if match:
    print("MATCHED BLOCK:")
    print(match.group(0))
else:
    print("NO MATCH")
