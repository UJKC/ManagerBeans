from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/aiback', methods=['POST'])
def aiback():

    data = request.json
    if 'message' in data:
        prompt_message = data['message']
    
    url_ai = "http://webapp-ai:11434/api/generate"  # Forwarding URL to AI server
    url_dashback = "/dashback/recieveai"  # URL for dashback endpoint

    # Data to be sent to the AI server
    data_ai = {
        "model": "mario",
        "prompt": prompt_message,
        "stream": False
    }
    
    # Forward the request to the AI server
    response_ai = requests.post(url_ai, json=data_ai)
    
    # Check if the request to AI server was successful
    if response_ai.status_code == 200:
        # Send the received data to '/dashback' endpoint
        response_dashback = requests.post(url_dashback, json=response_ai.json())
        if response_dashback.status_code == 200:
            return jsonify(response_ai.json()), 200  # Return JSON response from the forwarded request
        else:
            return "Error sending data to '/dashback': {}".format(response_dashback.status_code), response_dashback.status_code
    else:
        return "Error: {}".format(response_ai.status_code), response_ai.status_code  # Return error if request to AI server failed

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)  # Run the Flask app
