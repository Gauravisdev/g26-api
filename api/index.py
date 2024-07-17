from flask import Flask, request, jsonify
import requests
import time

app = Flask(__name__)

@app.route('/')
def home():
    return 'gauravv._.'

@app.route('/delta', methods=['GET'])
def delta():
    start_time = time.time()  # Record start time

    url = request.args.get("url")
    if not url:
        
        return jsonify({"success": False, "error": "URL parameter is missing"}), 400
    
    # Check if URL starts with the required prefix
    required_prefix = "https://gateway.platoboost.com/a/8?id="
    if not url.startswith(required_prefix):
        
        return jsonify({"success": False, "error": "URL must start with 'https://gateway.platoboost.com/a/8?id='"}), 400

    try:
        id = url.split('id=')[-1]

        link_info_response = requests.get(f"https://api-gateway.platoboost.com/v1/authenticators/8/{id}")
        link_info = link_info_response.json()
        print(link_info)

        if link_info.get("key"):
            end_time = time.time()  # Record end time
            time_taken = end_time - start_time
            
            return jsonify({"success": True, "key": link_info.get("key"), "time_taken": f"{time_taken:.2f}"})

        session_data_response = requests.post(f"https://api-gateway.platoboost.com/v1/sessions/auth/8/{id}", json={"captcha": "", "type": ""})
        data = session_data_response.json()
        print('> =-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= <')
        print(f"post response : {data}")
        data = session_data_response.json()
        print('> =-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= <')
        
        time.sleep(5)
        update_session_response = requests.put(f"https://api-gateway.platoboost.com/v1/sessions/auth/8/{id}/ui7c")
        response = update_session_response.json()
        print('> =-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= <')
        print(f'put response : {response}')
        print('> =-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= <')

        link_info_response1 = requests.get(f"https://api-gateway.platoboost.com/v1/authenticators/8/{id}")
        link_info1 = link_info_response1.json()

        if link_info1.get("key"):
            end_time = time.time()  # Record end time
            time_taken = end_time - start_time
            
            return jsonify({"success": True, "key": link_info1.get("key"), "time_taken": f"{time_taken:.2f}"})

        time.sleep(1)  # sleep for 3 seconds

        end_time = time.time()  # Record end time
        time_taken = end_time - start_time
        
        return jsonify({"success": False, "key": "Key not found", "time_taken": f"{time_taken:.2f}"})

    except Exception as error:
        end_time = time.time()  # Record end time
        time_taken = end_time - start_time
        
        return jsonify({"success": False, "error": str(error), "time_taken": f"{time_taken:.2f}"})

