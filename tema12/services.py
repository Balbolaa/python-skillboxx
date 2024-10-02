from flask import Flask  # Importing Flask to create a web application.
from datetime import datetime  # Importing datetime to work with date and time.

# Initializing the Flask app
app = Flask(__name__)
# Enabling debug mode to provide better error messages and auto-reloading during development
app.config['DEBUG'] = True

# Defining a route to handle URLs like /timestamp/<stamp>
# <stamp> is a dynamic part of the URL that the user will provide.
@app.route('/timestamp/<stamp>')
def timestamp(stamp):
    # Convert the URL parameter 'stamp' (which is a string) into a float
    # This float value is treated as a Unix timestamp
    # datetime.fromtimestamp() converts it into a human-readable date and time
    return f'{datetime.fromtimestamp(float(stamp))}'

# Defining the main function that runs the Flask app
def main():
    # Starts the Flask development server so it can listen to HTTP requests
    app.run()

# This block ensures that the Flask app runs only if the script is executed directly,
# and not imported as a module in another script
if __name__ == '__main__':
    main()
