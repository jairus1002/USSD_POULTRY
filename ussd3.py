from flask import Flask, request
import africastalking
import requests
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# Africa's Talking credentials for the sandbox
username = "sandbox"
api_key = "atsk_7ab5eb7344b16d5b8bb583e8eb49d0d2a18e7b91ff86389f0887366b4dea08ac587b9eae"

# Initialize Africa's Talking
africastalking.initialize(username, api_key)

# Define the PHP endpoint to which we will send the USSD data
php_url = "http://127.0.0.1/PROJECT_3/ussd.php"  # Update this to your actual PHP endpoint URL

# Define route to handle USSD requests
@app.route('/ussd', methods=['POST'])
def ussd():
    # Retrieve the incoming POST data from Africa's Talking
    session_id = request.values.get('sessionId', None)
    service_code = request.values.get('serviceCode', None)
    phone_number = request.values.get('phoneNumber', None)  # Phone number sent by simulator
    text = request.values.get('text', '')

    # Log the phone number for debugging (optional)
    print(f"Received USSD request from phone number: {phone_number}")

    # Split the user input into steps based on '*'
    user_input = text.split("*")

    # USSD logic based on user input
    if text == "":
        # Step 1: Initial prompt to ask for hatching date
        response = "CON Welcome to Poultry Management\n"
        response += "Enter the hatching date (yyyy-mm-dd):"  # Changed to match database expectations
    
    elif len(user_input) == 1:
        response = "CON Enter your phone number (as it appears on the SIM):"
    
    elif len(user_input) == 2:
        response = "CON Choose an option:\n"
        response += "1. vaccination\n"
        response += "2. management"

    elif len(user_input) == 3 and user_input[2] == "1":
        response = "CON Choose poultry type for vaccination:\n"
        response += "1. broilers\n"
        response += "2. layers"

    elif len(user_input) == 4 and user_input[2] == "1":
        poultry_type = "broilers" if user_input[3] == "1" else "layers"
        response = f"CON You selected Vaccination for {poultry_type}.\n"
        response += "Send 1 to confirm."

    elif len(user_input) == 3 and user_input[2] == "2":
        response = "CON Choose poultry type for management:\n"
        response += "1. broilers\n"
        response += "2. layers"

    elif len(user_input) == 4 and user_input[2] == "2":
        poultry_type = "broilers" if user_input[3] == "1" else "layers"
        response = f"CON You selected Management for {poultry_type}.\n"
        response += "Send 1 to confirm."

    elif len(user_input) == 5 and user_input[4] == "1":
        # Data to be sent to the PHP script
        hatching_date = datetime.strptime(user_input[0], "%Y-%m-%d").date()  # Ensure date is in the right format
        data = {
            "hatching_date": hatching_date,
            "phone_number": phone_number,
            "option": "vaccination" if user_input[2] == "1" else "management",
            "poultry_type": "broilers" if user_input[3] == "1" else "layers"
        }

        # Define the PHP script URLs
        php_scripts = ["time.php", "notify_A.php", "notify_B.php", "notify_C.php", "notify_D.php"]
        
        # Base URL for PHP scripts
        base_url = "http://localhost/PROJECT_3/"  # Update with your actual base URL

        # Simulate the execution of PHP scripts in the specified order
        for script in php_scripts:
            script_url = base_url + script
            response_php = requests.post(script_url, data=data)

            if response_php.status_code != 200:
                response = "END Failed to process your request at " + script
                break
        else:
            response = "END Your request has been processed successfully."

    else:
        response = "END Invalid option. Please try again."

    return response

# Start the Flask app
if __name__ == '__main__':
    app.run(port=5000, debug=True)
