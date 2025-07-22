from flask import Flask, request, jsonify
from flask_cors import CORS
from email import message_from_string
import re

app = Flask(__name__)
CORS(app)  # Allow requests from extensions like Chrome

def extract_auth_results(headers):
    auth_results = {
        "spf": "unknown",
        "dkim": "unknown",
        "dmarc": "unknown"
    }

    # Match full Authentication-Results block (handle multiline)
    auth_match = re.search(r'Authentication-Results:.*?(?=\n\S|$)', headers, flags=re.IGNORECASE | re.DOTALL)
    if auth_match:
        auth_block = auth_match.group(0).lower()
        if 'spf=pass' in auth_block:
            auth_results["spf"] = "pass"
        elif 'spf=fail' in auth_block:
            auth_results["spf"] = "fail"

        if 'dkim=pass' in auth_block:
            auth_results["dkim"] = "pass"
        elif 'dkim=fail' in auth_block:
            auth_results["dkim"] = "fail"

        if 'dmarc=pass' in auth_block:
            auth_results["dmarc"] = "pass"
        elif 'dmarc=fail' in auth_block:
            auth_results["dmarc"] = "fail"

    return auth_results

def compute_threat_score(parsed, auth):
    score = 0
    issues = []

    if auth["spf"] != "pass":
        score += 25
        issues.append("SPF failed or missing")
    if auth["dkim"] != "pass":
        score += 25
        issues.append("DKIM failed or missing")
    if auth["dmarc"] != "pass":
        score += 25
        issues.append("DMARC failed or missing")

    from_addr = parsed.get("From", "")
    return_path = parsed.get("Return-Path", "")

    if return_path and from_addr and return_path not in from_addr:
        score += 15
        issues.append("From and Return-Path mismatch")

    if not return_path:
        score += 10
        issues.append("Missing Return-Path")

    if score >= 75:
        verdict = "Dangerous"
    elif score >= 40:
        verdict = "Suspicious"
    else:
        verdict = "Safe"

    return score, verdict, issues

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json(force=True)
        raw_headers = data.get("headers", "").strip()

        if not raw_headers:
            return jsonify({
                "status": "error",
                "message": "No headers received"
            }), 400

        print("\n📥 Raw headers received:")
        print(raw_headers[:500] + ("..." if len(raw_headers) > 500 else ""))

        email_msg = message_from_string(raw_headers)
        parsed_headers = dict(email_msg.items())
        auth_results = extract_auth_results(raw_headers)
        score, verdict, issues = compute_threat_score(parsed_headers, auth_results)

        received = parsed_headers.get("Received", "N/A")
        if isinstance(received, list):
            received = received[0]

        # 🔽 NEW: Print the extracted analysis result in terminal
        print("🧪 Analysis Results:")
        print(f"  🛡️ Verdict: {verdict}")
        print(f"  ⚠️ Threat Score: {score}")
        print(f"  🚨 Issues: {issues}")
        print(f"  ✅ Auth Results: {auth_results}")
        print("  📋 Summary:")
        print(f"    - From: {parsed_headers.get('From', 'N/A')}")
        print(f"    - Return-Path: {parsed_headers.get('Return-Path', 'N/A')}")
        print(f"    - Subject: {parsed_headers.get('Subject', 'N/A')}")
        print(f"    - Received: {received}\n")

        return jsonify({
            "status": "success",
            "verdict": verdict,
            "threat_score": score,
            "issues": issues,
            "auth": auth_results,
            "summary": {
                "From": parsed_headers.get("From", "N/A"),
                "Return-Path": parsed_headers.get("Return-Path", "N/A"),
                "Received": received,
                "Subject": parsed_headers.get("Subject", "N/A"),
            }
        })

    except Exception as e:
        print("❌ Exception during analysis:", str(e))
        return jsonify({
            "status": "error",
            "message": "Internal server error",
            "details": str(e)
        }), 500


if __name__ == '__main__':
    app.run(debug=True)
