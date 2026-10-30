import csv
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from agent.agent import is_emergency, ai_emergency_check

name = sys.argv[1] if len(sys.argv) > 1 else "test_cases_holdout2.csv"
path = os.path.join(ROOT, "tests", name)
total = 0
correct = 0
wrong = []

with open(path, encoding="utf-8-sig", newline="") as f:
    for row in csv.DictReader(f):
        expected = row["expected"].strip()
        flagged = is_emergency(row["text"]) or ai_emergency_check(row["text"])
        got = "emergency" if flagged else "not_emergency"
        total += 1
        if got == expected:
            correct += 1
        else:
            wrong.append((row["text"], expected, got))

lines = [f"{name} (word list + AI backup): {correct}/{total} correct ({100 * correct / total:.0f}%)"]
for text, exp, got in wrong:
    lines.append(f"WRONG: {text} | expected {exp} | got {got}")

out = os.path.join(ROOT, "tests", "results_ai_" + name.replace(".csv", ".txt"))
with open(out, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(lines[0])
print(f"{len(wrong)} wrong. Details saved in {os.path.basename(out)}")