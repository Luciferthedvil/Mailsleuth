from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    headers = data.get("headers", "")
    # Placeholder response
    return jsonify({
        "status": "success",
        "message": "Header received",
        "threat_score": "pending"
    })

if __name__ == '__main__':
    app.run(debug=True)
