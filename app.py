from flask import Flask, render_template, request
import subprocess
app = Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html', results=None, query="")
@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query', '').strip().lower()
    results = []
    if query:
        try:
            cmd = 'hdfs dfs -cat /searchengine1/output/part-00000'
            output = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            for line in output.stdout.splitlines():
                line = line.strip()
                if not line:
                    continue
                if '\t' in line:
                    parts = line.split('\t', 1)
                else:
                    parts = line.split(None, 1)
                if len(parts) != 2:
                    continue
                # Strip colon from word if present
                word = parts[0].strip().lower().rstrip(':')
                if word == query:
                    docs = parts[1].split(',')
                    for doc in docs:
                        doc = doc.strip()
                        if doc:
                            results.append(doc)
                    break
        except Exception as e:
            results = [f"Error: {str(e)}"]
    return render_template('index.html', results=results, query=query)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)