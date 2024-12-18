import os
from flask import Flask, request, jsonify
from flask_cors import CORS  # to enable frontend-backend communication
try:
    from groq import Groq  # Ensure Groq library is installed
except ImportError:
    raise ImportError("Please install the Groq library using 'pip install groq'.")

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing for frontend access

# Initialize the Groq API client with error handling
try:
  # Use environment variable for security
    client = Groq(api_key="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")
except Exception as e:
    client = None
    print(f"Error initializing Groq client: {e}")

@app.route("/", methods=["GET"])
def home():
    """
    Home route for basic status message.
    """
    return "Welcome to the Personalized Learning Assistant API!"

@app.route("/ask", methods=["POST"])
def ask_question():
    """
    Handles POST requests to answer user questions based on grade level.
    """
    if client is None:
        return jsonify({"error": "Groq client is not initialized"}), 500

    # Get the JSON data from the request
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid input, JSON data is required"}), 400

    user_question = data.get("question", "").strip()
    grade_level = data.get("grade_level", "middle school").strip()

    if not user_question:
        return jsonify({"error": "Question field is required"}), 400

    try:
        # Use the Groq client to generate a response
        response = client.chat.completions.create(
            model="llama3-8b-8192",  # Replace with the correct model identifier for Groq
            messages=[
                {"role": "system", "content": f"You are a helpful learning assistant for {grade_level} students."},
                {"role": "user", "content": user_question}
            ],
            max_tokens=200  # Limit the response length
        )

        # Extract the answer from the API response
        answer = response.choices[0].message.content.strip()
        return jsonify({"answer": answer})

    except Exception as e:
        # Handle errors and return an error message
        print(f"Error during Groq API call: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Run the Flask app on port 5000
    app.run(host="127.0.0.1", port=5000, debug=True)
