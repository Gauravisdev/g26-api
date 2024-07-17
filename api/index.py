from flask import Flask, request, jsonify
import requests
import time

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return 'gauravv._.'

@app.route('/delta', methods=['GET'])
def delta():
    start_time = time.time()  # Record start time

    url = request.args.get("url")
    if not url:
        return jsonify({"success": False, "error": "URL parameter is missing"}), 400
    
    required_prefix = "https://gateway.platoboost.com/a/8?id="
    if not url.startswith(required_prefix):
        return jsonify({"success": False, "error": f"URL must start with '{required_prefix}'"}), 400

    id = url.split('id=')[-1]

    try:
        link_info_response = requests.get(f"https://api-gateway.platoboost.com/v1/authenticators/8/{id}")
        if link_info_response.status_code != 200:
            return jsonify({"success": False, "error": "Failed to get link info", "status_code": link_info_response.status_code}), 502
        
        link_info = link_info_response.json()
        
        if link_info.get("key"):
            end_time = time.time()  # Record end time
            time_taken = end_time - start_time
            return jsonify({"success": True, "key": link_info.get("key"), "time_taken": f"{time_taken:.2f}"})
        
        session_data_response = requests.post(f"https://api-gateway.platoboost.com/v1/sessions/auth/8/{id}", json={"captcha": "", "type": ""})
        if session_data_response.status_code != 200:
            return jsonify({"success": False, "error": "Failed to start session", "status_code": session_data_response.status_code}), 502

        data = session_data_response.json()
        
        time.sleep(5)
        update_session_response = requests.put(f"https://api-gateway.platoboost.com/v1/sessions/auth/8/{id}/ui7c")
        if update_session_response.status_code != 200:
            return jsonify({"success": False, "error": "Failed to update session", "status_code": update_session_response.status_code}), 502

        response = update_session_response.json()
        
        link_info_response1 = requests.get(f"https://api-gateway.platoboost.com/v1/authenticators/8/{id}")
        if link_info_response1.status_code != 200:
            return jsonify({"success": False, "error": "Failed to get updated link info", "status_code": link_info_response1.status_code}), 502
        
        link_info1 = link_info_response1.json()
        
        if link_info1.get("key"):
            end_time = time.time()  # Record end time
            time_taken = end_time - start_time
            return jsonify({"success": True, "key": link_info1.get("key"), "time_taken": f"{time_taken:.2f}"})

        time.sleep(1)  # sleep for 1 second

        end_time = time.time()  # Record end time
        time_taken = end_time - start_time
        return jsonify({"success": False, "error": "Key not found", "time_taken": f"{time_taken:.2f}"})

    except requests.exceptions.RequestException as e:
        end_time = time.time()  # Record end time
        time_taken = end_time - start_time
        return jsonify({"success": False, "error": str(e), "time_taken": f"{time_taken:.2f}"})
    except ValueError as e:
        end_time = time.time()  # Record end time
        time_taken = end_time - start_time
        return jsonify({"success": False, "error": "Invalid JSON response", "time_taken": f"{time_taken:.2f}"})
