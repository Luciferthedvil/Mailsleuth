from flask import Flask, request, jsonify
from flask_cors import CORS
from email import message_from_string
import re

app = Flask(__name__)
CORS(app)

# Heuristic scoring function
def analyze_headers(headers: str):
    result = {
        "verdict": "Safe",
        "threat_score": 0,
        "issues": [],
        "auth_results": {
            "spf": "unknown",
            "dkim": "unknown",
            "dmarc": "unknown"
        },
        "recommendation": ""
    }

    if not headers.strip():
        result["verdict"] = "Invalid"
        result["threat_score"] = 100
        result["issues"].append("Empty headers received")
        result["recommendation"] = "No headers to analyze. Ensure the email is loaded properly."
        return result

    # Look for SPF, DKIM, DMARC results
    spf = re.search(r"spf=(pass|fail|softfail|neutral|none|temperror|permerror)", headers, re.IGNORECASE)
    dkim = re.search(r"dkim=(pass|fail|policy|none)", headers, re.IGNORECASE)
    dmarc = re.search(r"dmarc=(pass|fail|policy|none)", headers, re.IGNORECASE)

    if spf:
        result["auth_results"]["spf"] = spf.group(1).lower()
        if result["auth_results"]["spf"] != "pass":
            result["issues"].append("SPF failed or missing")
            result["threat_score"] += 30
    else:
        result["issues"].append("SPF result missing")
        result["threat_score"] += 30

    if dkim:
        result["auth_results"]["dkim"] = dkim.group(1).lower()
        if result["auth_results"]["dkim"] != "pass":
            result["issues"].append("DKIM failed or missing")
            result["threat_score"] += 30
    else:
        result["issues"].append("DKIM result missing")
        result["threat_score"] += 30

    if dmarc:
        result["auth_results"]["dmarc"] = dmarc.group(1).lower()
        if result["auth_results"]["dmarc"] != "pass":
            result["issues"].append("DMARC failed or missing")
            result["threat_score"] += 30
    else:
        result["issues"].append("DMARC result missing")
        result["threat_score"] += 30

    # Final verdict
    if result["threat_score"] >= 70:
        result["verdict"] = "Dangerous"
        result["recommendation"] = "This email is likely a phishing attempt. Avoid clicking links or replying."
    elif result["threat_score"] >= 30:
        result["verdict"] = "Suspicious"
        result["recommendation"] = "Exercise caution. The email failed some authentication checks."
    else:
        result["verdict"] = "Safe"
        result["recommendation"] = "No major issues detected. Proceed normally, but always stay vigilant."

    return result


@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json
        raw_email = data.get("email", "").strip()
        print("📥 Raw headers received:\n", raw_email[:1000] or "[EMPTY]")

        email_obj = message_from_string(raw_email)
        from_header = email_obj.get("From", "N/A")
        subject = email_obj.get("Subject", "N/A")
        return_path = email_obj.get("Return-Path", "N/A")
        received_headers = email_obj.get_all("Received", []) or []

        analysis = analyze_headers(raw_email)

        print("🧪 Analysis Results:")
        print(f"  🛡️ Verdict: {analysis['verdict']}")
        print(f"  ⚠️ Threat Score: {analysis['threat_score']}")
        print(f"  🚨 Issues: {analysis['issues']}")
        print(f"  ✅ Auth Results: {analysis['auth_results']}")
        print(f"  📋 Summary:")
        print(f"    - From: {from_header}")
        print(f"    - Return-Path: {return_path}")
        print(f"    - Subject: {subject}")
        if received_headers:
            print(f"    - Received: {received_headers[0][:300]}...")

        return jsonify({
            "headers": {
                "from": from_header,
                "subject": subject,
                "return_path": return_path,
                "received": received_headers
            },
            "analysis": analysis
        })

    except Exception as e:
        print("❌ Server error:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
