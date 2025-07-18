from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all origins (localhost calls from extension)

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json(force=True)
        headers = data.get("headers", "").strip()

        if not headers:
            return jsonify({
                "status": "error",
                "message": "No headers received"
            }), 400

        print("✅ Received headers:")
        print(headers[:300] + "..." if len(headers) > 300 else headers)

        # Placeholder for threat scoring or analysis logic
        # For now, just echo back a success message
        return jsonify({
            "status": "success",
            "message": "Headers received successfully",
            "threat_score": "pending"
        })

    except Exception as e:
        print("❌ Error processing request:", str(e))
        return jsonify({
            "status": "error",
            "message": "Internal server error",
            "details": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
