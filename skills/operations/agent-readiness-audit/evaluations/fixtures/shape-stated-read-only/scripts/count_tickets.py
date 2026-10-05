#!/usr/bin/env python3
"""Count the tickets in a CSV export by status. Prints one line per status."""
import csv
import sys
from collections import Counter

with open(sys.argv[1], newline="", encoding="utf-8") as f:
    counts = Counter(row["status"] for row in csv.DictReader(f))
for status, n in sorted(counts.items()):
    print(f"{status}: {n}")
print(f"total: {sum(counts.values())}")
