from flask import Flask, request, abort
import africastalking
import logging

# Initialize Flask app
app = Flask(__name__)

# Africa's Talking credentials for the sandbox
username = "sandbox"  # For sandbox environment, the username is always 'sandbox'
api_key = "atsk_7ab5eb7344b16d5b8bb583e8eb49d0d2a18e7b91ff86389f0887366b4dea08ac587b9eae"  # Replace with your Africa's Talking API key

# Initialize Africa's Talking
africastalking.initialize(username, api_key)

# Set up basic logging
logging.basicConfig(level=logging.DEBUG)

# Define route to handle USSD requests
@app.route('/ussd', methods=['POST'])
def ussd():
    try:
        # Retrieve the incoming POST data from Africa's Talking
        session_id = request.values.get('sessionId', None)
        service_code = request.values.get('serviceCode', None)
        phone_number = request.values.get('phoneNumber', None)  # Phone number sent by simulator
        text = request.values.get('text', '')

        # Ensure the required parameters are provided
        if not session_id or not service_code or not phone_number:
            logging.error("Missing required parameters.")
            abort(400, description="Bad request, missing required parameters.")

        # Log the phone number for debugging (optional)
        logging.info(f"Received USSD request from phone number: {phone_number}")

        # Split the user input into steps based on '*'
        user_input = text.split("*")

        # Initialize response variable
        response = ""

        # USSD logic based on user input
        if text == "":
            # Initial prompt for language selection
            response = "CON Welcome to Poultry Management\n"
            response += "Choose your language:\n"
            response += "1. English\n"
            response += "2. Kiswahili"

        # Step 1: Handle language selection
        elif len(user_input) == 1:
            if user_input[0] == "1":
                response = "CON Enter the hatching date (dd-mm-yyyy):"
            elif user_input[0] == "2":
                response = "CON Weka tarehe ya kuangua (dd-mm-yyyy):"
            else:
                response = "CON Invalid option. Choose your language:\n"
                response += "1. English\n"
                response += "2. Kiswahili"

        # Step 2: Ask for phone number after hatching date is entered
        elif len(user_input) == 2:
            if user_input[0] == "1":
                response = "CON Enter your phone number:"
            elif user_input[0] == "2":
                response = "CON Weka nambari yako ya simu:"
            else:
                response = "CON Invalid option. Please try again."

        # Step 3: Ask if they want to choose Vaccination or Management
        elif len(user_input) == 3:
            if user_input[0] == "1":
                response = "CON Choose an option:\n1. Vaccination\n2. Management"
            elif user_input[0] == "2":
                response = "CON Chagua chaguo:\n1. Chanjo\n2. Usimamizi"
            else:
                response = "CON Invalid option. Please try again."

        # Step 4a: Vaccination -> Ask for poultry type (Broilers or Layers)
        elif len(user_input) == 4 and user_input[2] == "1":
            if user_input[0] == "1":
                response = "CON Choose poultry type for vaccination:\n1. Broilers\n2. Layers"
            elif user_input[0] == "2":
                response = "CON Chagua aina ya kuku kwa chanjo:\n1. Broilers\n2. Layers"
            else:
                response = "CON Invalid option. Please try again."

        # Step 5a: Display summary for vaccination
        elif len(user_input) == 5 and user_input[2] == "1":
            poultry_type = "Broilers" if user_input[3] == "1" else "Layers"
            if user_input[0] == "1":
                response = f"CON You selected Vaccination for {poultry_type}.\nSend 1 to confirm."
            elif user_input[0] == "2":
                response = f"CON Umechagua Chanjo kwa {poultry_type}.\nTuma 1 kuthibitisha."

        # Step 4b: Management -> Ask for poultry type (Broilers or Layers)
        elif len(user_input) == 4 and user_input[2] == "2":
            if user_input[0] == "1":
                response = "CON Choose poultry type for management:\n1. Broilers\n2. Layers"
            elif user_input[0] == "2":
                response = "CON Chagua aina ya kuku kwa usimamizi:\n1. Broilers\n2. Layers"

        # Step 5b: Display summary for management
        elif len(user_input) == 5 and user_input[2] == "2":
            poultry_type = "Broilers" if user_input[3] == "1" else "Layers"
            if user_input[0] == "1":
                response = f"CON You selected Management for {poultry_type}.\nSend 1 to confirm."
            elif user_input[0] == "2":
                response = f"CON Umechagua Usimamizi kwa {poultry_type}.\nTuma 1 kuthibitisha."

        # Step 6: Confirmation and success message
        elif len(user_input) == 6 and user_input[5] == "1":
            if user_input[0] == "1":
                response = "END Your request has been processed successfully."
            elif user_input[0] == "2":
                response = "END Ombi lako limefanikiwa kutumwa."

        # Handle unrecognized input
        else:
            response = "CON Invalid option. Please try again."

        # Return the USSD response to Africa's Talking
        return response

    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return "END An error occurred. Please try again later.", 500


# Start the Flask app
if __name__ == '__main__':
    app.run(port=5000, debug=True)
