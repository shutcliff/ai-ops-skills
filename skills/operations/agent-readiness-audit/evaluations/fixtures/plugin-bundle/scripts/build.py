"""Count tickets per category in an export and print the weekly report."""
import csv
import sys
from collections import Counter

rows = list(csv.DictReader(open(sys.argv[1], encoding="utf-8")))
counts = Counter(r.get("category", "uncategorised") for r in rows)
for name, n in sorted(counts.items()):
    print(f"- {name}: {n}")
print(f"Total: {len(rows)}")
