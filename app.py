import os
from flask import Flask, request, jsonify, send_from_directory
from openai import OpenAI

app = Flask(__name__, static_folder="static")

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

@app.route("/")
def home():
    return send_from_directory("static", "index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        message = data.get("message", "").strip()

        if not message:
            return jsonify({"error": "Please enter a message"}), 400

        response = client.responses.create(
            model="gpt-5.5",
            instructions=(
                "You are My AI, a friendly personal assistant. "
                "Answer questions clearly and help students "
                "understand their studies in simple language."
            ),
            input=message
        )

        return jsonify({
            "reply": response.output_text
        })

    except Exception:
        app.logger.exception("AI request failed")
        return jsonify({
            "error": "Sorry, something went wrong. Please try again."
        }), 500

if __name__ == "__main__":
    app.run(debug=True)
            
