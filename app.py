from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json, os
app = Flask(__name__)
CORS(app)
DB_FILE = 'database.json'
def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE,'r',encoding='utf-8') as f:
            try: return json.load(f)
            except: return []
    return []
def save_data(data):
    with open(DB_FILE,'w',encoding='utf-8') as f:
        json.dump(data,f,indent=2,ensure_ascii=False)
@app.route('/')
def home(): return send_from_directory('.', 'index.html')
@app.route('/api/issues', methods=['GET'])
def get_issues():
    issues = load_data()
    return jsonify(issues)
@app.route('/api/issues', methods=['POST'])
def add_issue():
    new_issue = request.json
    if not new_issue.get('type') or not new_issue.get('location'):
        return jsonify({"error": "Type aur Location zaroori"}), 400
    issues = load_data()
    issues.append(new_issue)
    save_data(issues)
    return jsonify({"message": "AWAAZ save!"})
@app.route('/api/issues/<int:issue_id>', methods=['PUT'])
def update_issue(issue_id):
    body = request.json
    issues = load_data()
    for issue in issues:
        if issue['id'] == issue_id: issue['status'] = body.get('status')
    save_data(issues)
    return jsonify({"message":"Status updated"})
@app.route('/<path:path>')
def serve_static(path): return send_from_directory('.', path)
if __name__ == '__main__':
    if not os.path.exists(DB_FILE): save_data([])
    app.run(debug=True, port=5000)
  
