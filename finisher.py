import africastalking

# Initialize the Africa's Talking API with sandbox credentials
username = "sandbox"  # Sandbox username
api_key = "atsk_7ab5eb7344b16d5b8bb583e8eb49d0d2a18e7b91ff86389f0887366b4dea08ac587b9eae"  # Your sandbox API key
africastalking.initialize(username, api_key)

# Initialize the SMS service
sms = africastalking.SMS

# Send SMS function using sandbox
def send_sms():
    recipients = ["+254735489527"]  # Replace with your own phone number for testing in sandbox
    message = "Dear Farmer, this is a reminder to introduce your poultry broilers to finisher feeds."  # Your test message
    sender_id = None  # No need for sender ID in sandbox mode

    try:
        # Send the SMS (the response will simulate the SMS being sent in the sandbox)
        response = sms.send(message, recipients)
        print("SMS sent successfully:", response)  # Print the response from Africa's Talking sandbox
    except Exception as e:
        print(f"Error sending SMS: {e}")

# Call the function to send the SMS
send_sms()
