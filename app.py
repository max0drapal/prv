import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)

# Pro školní projekt povolíme CORS všude (později se dá zpřísnit)
CORS(app)

client = OpenAI()


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
        response = client.responses.create(
            model="gpt-4o-mini",
            input=f"Jsi technická podpora pro VDF Games. Odpovídej stručně a česky. Uživatel ({student}) píše: {message}",
        )
        reply = (response.output_text or "").strip() or "Nepodařilo se vygenerovat odpověď."
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    app.run(host="0.0.0.0", port=port, debug=True)
