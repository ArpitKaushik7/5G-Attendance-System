from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

FILE_PATH = 'fingerprint_data.xlsx'

@app.route('/authenticate_fingerprint', methods=['POST'])
def authenticate_fingerprint():
    try:
        data = request.json
        template_position = data.get("Template Position")

        df_existing = pd.read_excel(FILE_PATH)

        # Check if template position exists
        match = df_existing[df_existing["Template Position"] == template_position]

        if not match.empty:
            user_info = match.to_dict(orient="records")[0]
            return jsonify({"authenticated": True, "user": user_info}), 200
        else:
            return jsonify({"authenticated": False}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/update_fingerprint', methods=['POST'])
def update_fingerprint():
    try:
        data = request.json
        df_new = pd.DataFrame([data])

        try:
            df_existing = pd.read_excel(FILE_PATH)
            df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        except FileNotFoundError:
            df_combined = df_new

        df_combined.to_excel(FILE_PATH, index=False)
        return jsonify({"message": "Fingerprint data updated successfully!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)