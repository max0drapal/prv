import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai

app = Flask(__name__)
CORS(app)

client = genai.Client()


@app.get("/")
def home():
    return "VDF Support Backend is running"


@app.post("/chat")
def chat():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()
    student = (data.get("student") or "unknown").strip()

    if not message:
        return jsonify({"error": "message is required"}), 400

    try:
        prompt = (
            f"Jsi technická podpora pro VDF Games. Odpovídej stručně, přátelsky a česky. "
            f"Uživatel ({student}) píše: {message}"
        )
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        reply = (response.text or "").strip() or "Nepodařilo se vygenerovat odpověď."
        return jsonify({"reply": reply})
    except Exception as e:
        print("GEMINI ERROR:", e, flush=True)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    app.run(host="0.0.0.0", port=port, debug=True)
