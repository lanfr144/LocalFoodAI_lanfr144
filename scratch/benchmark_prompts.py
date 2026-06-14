import time
import ollama

model = "llama3.2:3b"

# Old prompt
sys_prompt_old = """You are a helpful medical data analyst AI. 
Health profile: Condition: Pregnancy. 
Act as a specialized clinical dietitian. Provide a direct answer. Skip all thinking, reasoning, and pleasantries.
Local Database Context: No database records found.
"""

# New prompt
sys_prompt_new = """You are a helpful medical data analyst AI. 
Health profile: Condition: Pregnancy. 
Act as a specialized clinical dietitian. Provide a direct answer. Use Chain of Thought reasoning, and skip pleasantries.
Local Database Context: No database records found.
"""

user_query = "Can I eat unpasteurized cheese during pregnancy?"

print("--- RUNNING BENCHMARK ON SERVER ---")

# Run old prompt
print("\\n[Old Prompt] - Skip all thinking and reasoning...")
t0 = time.time()
resp_old = ollama.chat(model=model, messages=[
    {"role": "system", "content": sys_prompt_old},
    {"role": "user", "content": user_query}
])
t1 = time.time()
elapsed_old = t1 - t0
content_old = resp_old['message']['content']
token_count_old = resp_old.get('eval_count', len(content_old.split()))
print(f"Time Taken: {elapsed_old:.4f} seconds")
print(f"Response length (chars): {len(content_old)}")
print(f"Generated tokens: {token_count_old}")
print(f"Speed: {token_count_old / elapsed_old:.2f} tokens/sec")
print("Response preview:")
print(content_old[:300] + "...")

# Run new prompt
print("\\n[New Prompt] - Chain of Thought...")
t2 = time.time()
resp_new = ollama.chat(model=model, messages=[
    {"role": "system", "content": sys_prompt_new},
    {"role": "user", "content": user_query}
])
t3 = time.time()
elapsed_new = t3 - t2
content_new = resp_new['message']['content']
token_count_new = resp_new.get('eval_count', len(content_new.split()))
print(f"Time Taken: {elapsed_new:.4f} seconds")
print(f"Response length (chars): {len(content_new)}")
print(f"Generated tokens: {token_count_new}")
print(f"Speed: {token_count_new / elapsed_new:.2f} tokens/sec")
print("Response preview:")
print(content_new[:300] + "...")

diff_time = elapsed_new - elapsed_old
pct_change = (diff_time / elapsed_old) * 100
print(f"\\n--- SUMMARY ---")
print(f"Old Prompt time: {elapsed_old:.2f}s")
print(f"New Prompt time: {elapsed_new:.2f}s")
print(f"Difference: {diff_time:+.2f}s ({pct_change:+.1f}%)")
