from flask import Flask, render_template, request, jsonify
import requests
import json

# Initialize Flask app
app = Flask(__name__)

# Hugging Face API Key Configuration
HF_API_KEY = "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"  # Replace with your Hugging Face API key

# Define the model you want to use
HF_MODEL = "codeparrot/codeparrot-small"  # You can replace this with any suitable model on Hugging Face

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/review', methods=['POST'])
def review_code():
    code_snippet = request.form.get('code')

    # Define the API endpoint and headers
    hf_url = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
    headers = {
        "Authorization": f"Bearer {HF_API_KEY}"
    }

    # Prepare the data payload
    payload = {
        "inputs": f"Review the following code and provide suggestions:\n\n{code_snippet}"
    }

    # Make the request to the Hugging Face API
    try:
        response = requests.post(hf_url, headers=headers, data=json.dumps(payload))
        response_data = response.json()

        # Extract suggestions from the response
        if response.status_code == 200:
            suggestions = response_data[0]['generated_text'].strip()  # Adjust based on response format
            return jsonify({"status": "success", "review": suggestions})
        else:
            return jsonify({"status": "error", "message": "Failed to get response from Hugging Face API"})
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
