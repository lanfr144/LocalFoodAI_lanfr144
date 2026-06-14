import re

# Test clean mode
clean_pattern = r'\$Format' + r':([^%:\r\n]+):([^%:\r\n]+):[^\r\n$]*?\$'

def clean_content(content):
    return re.sub(clean_pattern, r'$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$', content)

# Test cases
test_app_py_lines = """
#ident "@(#)LocalFoodAI:app.py:$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
"""

print("1. Testing clean on smudged headers:")
cleaned = clean_content(test_app_py_lines)
print("Original:")
print(test_app_py_lines)
print("Cleaned:")
print(cleaned)
print("Did it change?", cleaned != test_app_py_lines)
