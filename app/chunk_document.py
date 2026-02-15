import re

INPUT_PATH = "data/regulations/MD44_text_clean.txt"
OUTPUT_PATH = "data/regulations/MD44_chunks.txt"

with open(INPUT_PATH, "r", encoding="utf-8") as f:
    text = f.read()

# Split ONLY at section numbers at start of line
sections = re.split(r'(?m)^(?=\d+\.\s)', text)

sections = [s.strip() for s in sections if len(s.strip()) > 0]

# Merge extremely small sections (rare case)
merged = []
buffer = ""

MIN_LENGTH = 1500  # increase threshold

for section in sections:
    if len(section) < MIN_LENGTH:
        buffer += "\n" + section
    else:
        if buffer:
            merged.append(buffer.strip())
            buffer = ""
        merged.append(section)

if buffer:
    merged.append(buffer.strip())

print(f"Total improved chunks: {len(merged)}")

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    for i, chunk in enumerate(merged):
        f.write(f"\n--- CHUNK {i+1} ---\n")
        f.write(chunk)
        f.write("\n")

print("Saved improved structured chunks.")
