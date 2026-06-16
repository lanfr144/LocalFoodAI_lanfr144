import re

pattern = r'\$Format:LocalFoodAI_lanfr144:test_regex.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$)?[^$]*?\$'
repl = r'$Format:LocalFoodAI_lanfr144:test_regex.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$'
content = '#ident "@(#)$Format:LocalFoodAI_lanfr144:test_regex.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"\n'

print("Testing clean pattern...")
try:
    res = re.sub(pattern, repl, content)
    print("Clean pattern works! Result:", res)
except Exception as e:
    print("Clean pattern failed:", e)

smudge_pattern = r'\$Format:LocalFoodAI_lanfr144:test_regex.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$'
replacement = "$Format:LocalFoodAI_lanfr144:test_regex.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
print("Testing smudge pattern...")
try:
    res = re.sub(smudge_pattern, replacement, content)
    print("Smudge pattern works! Result:", res)
except Exception as e:
    print("Smudge pattern failed:", e)
