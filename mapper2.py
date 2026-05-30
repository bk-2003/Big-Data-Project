import sys
import os
import re
import string

STOPWORDS = set(['a','an','the','is','it','in','on','at','to','and','or','of','for','with','this','that','was','are','be','as','by','from','but','not','have','had','has','he','she','they','we','you','i','its','his','her','their'])

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    words = text.split()
    words = [w for w in words if w not in STOPWORDS and len(w) > 1]
    return words

filename = os.environ.get('mapreduce_map_input_file', 'unknown')
doc_id = os.path.basename(filename).replace('.txt', '')

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    words = clean_text(line)
    for word in words:
        print(f"{word}:\t{doc_id}")