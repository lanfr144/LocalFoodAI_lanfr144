import subprocess

test_input = '#ident "@(#)$Format:LocalFoodAI_lanfr144:test_filter.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"\n'

# Test smudge
p = subprocess.Popen(
    ['python', 'local_tools/git-ident-filter.py', 'smudge', 'app.py'],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)
out, err = p.communicate(test_input)
print("SMUDGE OUT:", repr(out))
print("SMUDGE ERR:", repr(err))

# Test clean on smudged
p2 = subprocess.Popen(
    ['python', 'local_tools/git-ident-filter.py', 'clean'],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)
out2, err2 = p2.communicate(out)
print("CLEAN OUT:  ", repr(out2))
print("CLEAN ERR:  ", repr(err2))
