from flask import Flask, request, jsonify
import requests
import time

# Discord webhook URL for logging
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1243059707304873994/LSWY1CHOd-4fzEvOdMgOHBy9fgxrOVSjGMYmUFH4eS3ZIbkAshBygAu0rYDoi1nkEMeJ"

app = Flask(__name__)

def log_to_discord(message):
    """
    Sends a formatted message to Discord webhook URL.
    """
    try:
        payload = {
            "content": None,
            "embeds": [
                {
                    "title": "Delta api logs",
                    "description": message,
                    "color": 16711680  # Red color
                }
            ]
        }
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
    except Exception as error:
    	log_to_discord(f"Error: {str(error)} - Failed")

@app.route('/')
def home():
    return "api by gaurav_26"

@app.route('/delta', methods=['GET'])
def delta():
    start_time = time.time()  # Record start time

    url = request.args.get("url")
    if not url:
        log_to_discord("URL parameter is missing - Failed")
        return jsonify({"success": False, "error": "URL parameter is missing"}), 400
    
    # Check if URL starts with the required prefix
    required_prefix = "https://gateway.platoboost.com/a/8?id="
    if not url.startswith(required_prefix):
        log_to_discord("URL must start with 'https://gateway.platoboost.com/a/8?id=' - Failed")
        return jsonify({"success": False, "error": "URL must start with 'https://gateway.platoboost.com/a/8?id='"}), 400

    try:
        id = url.split('id=')[-1]

        link_info_response = requests.get(f"https://api-gateway.platoboost.com/v1/authenticators/8/{id}")
        link_info = link_info_response.json()

        if link_info.get("key"):
            end_time = time.time()  # Record end time
            time_taken = end_time - start_time
            log_to_discord(f"Success! \n Key: {link_info.get('key')} \n Time taken: {time_taken:.2f} seconds \n Requested Link: {url}")
            return jsonify({"success": True, "key": link_info.get("key"), "time_taken": f"{time_taken:.2f}"})

        session_data_response = requests.post(f"https://api-gateway.platoboost.com/v1/sessions/auth/8/{id}", json={"captcha": "", "type": ""})
        data = session_data_response.json()
        
        update_session_response = requests.put(f"https://api-gateway.platoboost.com/v1/sessions/auth/8/{id}/ui7c")
        response = update_session_response.json()

        session_data_response2 = requests.get(f"https://api-gateway.platoboost.com/v1/sessions/auth/8/{id}")
        data2 = session_data_response2.json()
        
        time.sleep(4)
        
        update_session_response2 = requests.put(f"https://api-gateway.platoboost.com/v1/sessions/auth/8/{id}/ui7c")
        response = update_session_response2.json()

        link_info_response1 = requests.get(f"https://api-gateway.platoboost.com/v1/authenticators/8/{id}")
        link_info1 = link_info_response1.json()

        if link_info1.get("key"):
            end_time = time.time()  # Record end time
            time_taken = end_time - start_time
            log_to_discord(f"Success! \n Key: {link_info.get('key')} \n Time taken: {time_taken:.2f} seconds \n Requested Link: {url}")
            return jsonify({"success": True, "key": link_info1.get("key"), "time_taken": f"{time_taken:.2f}"})

        time.sleep(1)  # sleep for 3 seconds

        end_time = time.time()  # Record end time
        time_taken = end_time - start_time
        log_to_discord("Key not found - Failed")
        return jsonify({"success": False, "key": "Key not found", "time_taken": f"{time_taken:.2f}"})

    except Exception as error:
        end_time = time.time()  # Record end time
        time_taken = end_time - start_time
        log_to_discord(f"Error: {str(error)} - Failed")
        return jsonify({"success": False, "error": str(error), "time_taken": f"{time_taken:.2f}"})
