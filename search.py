import sys
import subprocess

def search_index(keyword):
    keyword = keyword.lower().strip()
    print(f"\nSearching for: '{keyword}'\n")
    result = subprocess.run(['hdfs', 'dfs', '-cat', '/searchengine/output/part-00000'], capture_output=True, text=True)
    found = False
    for line in result.stdout.splitlines():
        if line.startswith(keyword + '\t'):
            parts = line.split('\t')
            if len(parts) == 2:
                print(f"Found in documents: {parts[1]}")
                found = True
            break
    if not found:
        print(f"No documents found for '{keyword}'")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        keyword = input("Enter search keyword: ")
    else:
        keyword = sys.argv[1]
    search_index(keyword)