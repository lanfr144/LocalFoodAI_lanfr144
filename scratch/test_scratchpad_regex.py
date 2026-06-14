import re

def strip_scratchpad(text: str) -> str:
    # Strip out the XML <scratchpad> tag and everything in between, non-greedily
    clean_text = re.sub(r'<scratchpad>.*?</scratchpad>', '', text, flags=re.DOTALL)
    return clean_text.strip()

def filter_scratchpad_stream(stream):
    buffer = ""
    in_scratchpad = False
    for content in stream:
        buffer += content
        
        while True:
            if not in_scratchpad:
                start_idx = buffer.find("<scratchpad>")
                if start_idx != -1:
                    yield buffer[:start_idx]
                    buffer = buffer[start_idx:]
                    in_scratchpad = True
                else:
                    yield_len = max(0, len(buffer) - 11)
                    if yield_len > 0:
                        yield buffer[:yield_len]
                        buffer = buffer[yield_len:]
                    break
            else:
                end_idx = buffer.find("</scratchpad>")
                if end_idx != -1:
                    buffer = buffer[end_idx + 13:]
                    in_scratchpad = False
                else:
                    keep_len = 12
                    if len(buffer) > keep_len:
                        buffer = buffer[-keep_len:]
                    break
    if not in_scratchpad and buffer:
        yield buffer

# Test data
test_input = """<scratchpad>
- Cups to grams conversion
- Calorie summation
</scratchpad>
| Meal Time | Exact Food | Portion Size | Calories | Protein |
| --- | --- | --- | --- | --- |
| Breakfast | Oatmeal | 1 cup | 150 kcal | 5g |"""

# 1. Test strip_scratchpad
stripped = strip_scratchpad(test_input)
print("--- Test strip_scratchpad ---")
print(repr(stripped))
assert "<scratchpad>" not in stripped
assert "</scratchpad>" not in stripped
assert "Oatmeal" in stripped
print("Pass!")

# 2. Test filter_scratchpad_stream
stream_chunks = [
    "| Meal Time | ",
    "<scrat",
    "chpad>\n- Co",
    "T\n</scrat",
    "chpad>\n| Breakfast |",
    " Oatmeal |",
]
stream_result = "".join(filter_scratchpad_stream(stream_chunks))
print("\n--- Test filter_scratchpad_stream ---")
print(repr(stream_result))
assert "<scratchpad>" not in stream_result
assert "</scratchpad>" not in stream_result
assert "Oatmeal" in stream_result
print("Pass!")
