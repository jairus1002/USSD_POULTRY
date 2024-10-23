import africastalking

# Initialize the Africastalking API with sandbox credentials
username = "sandbox"  # Sandbox username is always 'sandbox'
api_key = "atsk_7ab5eb7344b16d5b8bb583e8eb49d0d2a18e7b91ff86389f0887366b4dea08ac587b9eae"  # Replace with your sandbox API key
africastalking.initialize(username, api_key)

# Initialize the SMS service
sms = africastalking.SMS

# Recipient's phone number (same throughout)
to = "+254735489527"  # Include the country code

# Message to be sent
message = "Dear Farmer This is a reminder that its time to vaccinate your poultry layers against bronchitis. Administer dose 1. Please ensure timely vaccination to maintain the health and well-being of your birds. Thank you for your attention to this matter."

try:
    # Send SMS message
    response = sms.send(message, [to])
    print("SMS sent successfully:", response)
except Exception as e:
    print("Error:", e)
