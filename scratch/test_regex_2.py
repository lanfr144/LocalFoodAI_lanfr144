import re

pattern = r'\$Format' + r':[^:]+:[^:]+:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N\$'
repl = 'REPLACED'
content = 'test $Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$ test'

print("Pattern:", pattern)
print("Content:", content)
print("Match:", re.search(pattern, content))
print("Result:", re.sub(pattern, repl, content))
