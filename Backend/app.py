from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    username = data.get('username')
    github_url = data.get('githubUrl')

    if not username or not github_url:
        return jsonify({'error': 'Both fields are required'}), 400

    # Process the data (e.g., save to database, etc.)
    return jsonify({'message': 'Data received successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)
