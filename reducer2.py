import sys
from collections import defaultdict

current_word = None
doc_list = defaultdict(int)

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    parts = line.split('\t')
    if len(parts) != 2:
        continue
    word, doc_id = parts[0], parts[1]
    if current_word and word != current_word:
        doc_str = ', '.join([f"{d}({c})" for d, c in sorted(doc_list.items())])
        print(f"{current_word}\t{doc_str}")
        doc_list = defaultdict(int)
    current_word = word
    doc_list[doc_id] += 1

if current_word:
    doc_str = ', '.join([f"{d}({c})" for d, c in sorted(doc_list.items())])
    print(f"{current_word}\t{doc_str}")