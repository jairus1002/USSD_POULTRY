from flask import Flask, request
import africastalking
import google.generativeai as genai
import requests
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# Africa's Talking credentials for the sandbox
username = "sandbox"  # Use sandbox for testing
api_key_sms = "atsk_7ab5eb7344b16d5b8bb583e8eb49d0d2a18e7b91ff86389f0887366b4dea08ac587b9eae"  # Your sandbox API key

# Initialize Africa's Talking for SMS
africastalking.initialize(username, api_key_sms)
sms = africastalking.SMS

# Configure the Gemini API key
api_key_gemini = "AIzaSyB0exgFLLDaljxqXN2qPtQ2AVdDDRLoQaw"
genai.configure(api_key=api_key_gemini)

@app.route('/ussd', methods=['POST'])
def ussd():
    # Retrieve the incoming POST data from Africa's Talking
    session_id = request.values.get('sessionId', None)
    service_code = request.values.get('serviceCode', None)
    phone_number = request.values.get('phoneNumber', None)
    text = request.values.get('text', '')

    # Split the user input into steps based on '*'
    user_input = text.split("*")

    # Initialize response
    response = ""

    # Step 1: Initial prompt to choose between setting a reminder or AI consultant
    if text == "":
        response = "CON Welcome to Poultry Management\n"
        response += "Choose an option:\n"
        response += "1. Set a Reminder\n"
        response += "2. AI Consultant"

    # Step 2: If the user selects "Set a Reminder"
    elif len(user_input) == 1 and user_input[0] == "1":
        # Now ask for the hatching date
        response = "CON Enter the hatching date (yyyy-mm-dd):"

    # Step 3: Handle the hatching date input and continue the flow
    elif len(user_input) == 2 and user_input[0] == "1":
        try:
            # Validate hatching date
            hatching_date = datetime.strptime(user_input[1], "%Y-%m-%d").date()
            response = "CON Hatching date: {}.\n".format(hatching_date)
            response += "Choose an option:\n"
            response += "1. Vaccination\n"
            response += "2. Management"
        except ValueError:
            # Invalid date format
            response = "CON Invalid date format. Please enter the hatching date in the format yyyy-mm-dd:"

    # Step 4: Handle "Set a Reminder" options (Vaccination or Management)
    elif len(user_input) == 3 and user_input[0] == "1":
        if user_input[2] == "1":  # Vaccination
            response = "CON Choose poultry type for vaccination:\n"
            response += "1. Broilers\n"
            response += "2. Layers"
        elif user_input[2] == "2":  # Management
            response = "CON Choose poultry type for management:\n"
            response += "1. Broilers\n"
            response += "2. Layers"

    # Step 5: Process poultry type selection
    elif len(user_input) == 4 and user_input[0] == "1":
        poultry_type = "broilers" if user_input[3] == "1" else "layers"
        option = "Vaccination" if user_input[2] == "1" else "Management"
        response = f"CON You selected {option} for {poultry_type}.\nSend 1 to confirm."

    # Step 6: Final confirmation and sending to PHP scripts
    elif len(user_input) == 5 and user_input[0] == "1" and user_input[4] == "1":
        hatching_date = datetime.strptime(user_input[1], "%Y-%m-%d").date()  # Ensure date is in the right format
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

    # Step 7: AI Consultant Flow (If the user selects AI Consultant)
    elif len(user_input) == 1 and user_input[0] == "2":
        response = "CON Please describe the disease symptoms:"

    # Step 8: Handle AI Consultant symptom input and use Gemini API
    elif len(user_input) == 2 and user_input[0] == "2":
        symptoms = user_input[1]  # Capture the symptoms description
        
        # Generate text using Gemini API
        prompt = f"Explain the symptoms of a poultry disease: {symptoms} and summarize the main points and state the possible diesease let it come out clearly ; limit to 50 characters."
        model = genai.GenerativeModel(model_name="gemini-1.5-flash-exp-0827")
        
        try:
            response_gemini = model.generate_content(prompt)
            generated_text = response_gemini.text  # Get the generated text
            
            # Send the generated text as an SMS
            sms_response = sms.send(generated_text, [phone_number])

            if sms_response:
                response = "END A description of the disease has been sent to your phone via SMS."
            else:
                response = "END Failed to send the SMS. Please try again."

        except Exception as e:
            response = f"END An error occurred while generating the response: {str(e)}"
    else:
        response = "END Invalid option. Please try again."

    return response

# Start the Flask app
if __name__ == '__main__':
    app.run(port=3000, debug=True)