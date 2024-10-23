import africastalking

# Initialize Africa's Talking SDK with sandbox credentials
username = "sandbox"  # Use 'sandbox' for testing
api_key = "atsk_7ab5eb7344b16d5b8bb583e8eb49d0d2a18e7b91ff86389f0887366b4dea08ac587b9eae"  # Your sandbox API key

africastalking.initialize(username, api_key)

# Initialize SMS service
sms = africastalking.SMS

# Recipient's phone number (use sandbox number for testing)
to = "+254735489527"  # Replace with your own sandbox test number

# Message to be sent
message = ("Dear Farmer, this is a reminder that it's time to vaccinate your poultry layers "
           "against Fowl Pox. Please ensure timely vaccination to maintain the health and "
           "well-being of your birds. Thank you for your attention to this matter.")

try:
    # Send SMS message
    response = sms.send(message, [to])
    print("SMS sent successfully:", response)
except Exception as e:
    print("Error:", e)
