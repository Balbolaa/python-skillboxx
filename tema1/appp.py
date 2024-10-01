
import datetime 
import random  
import re  # Regular expressions to extract words from text

# Import Flask for web application
from flask import Flask

# Create a Flask app instance
app = Flask(__name__)


cars_list = ['Chevrolet', 'Renault', 'Ford', 'Lada']


cats_list = ['Корниш-рекс', 'Русская голубая', 'Шотландская вислоухая', 'Мейн-кун', 'Манчкин']



war_and_peace = open('static/war_and_peace.txt', 'r', encoding='UTF-8').read()

# Global variable to count the number of visits
visits = 0

# Route for the /hello_world endpoint
@app.route('/hello_world')
def hello_world():

    return 'Привет, мир!'


# Route for the /cars endpoint
@app.route('/cars')
def cars():
    global cars_list
    # Joins the list of car brands into a single string and returns it
    return ' '.join(cars_list)


# Route for the /cats endpoint
@app.route('/cats')
def cats():
    # Chooses a random cat breed from the list and returns it
    return random.choice(cats_list)


# Route for the /get_time/now endpoint
@app.route('/get_time/now')
def get_time_now():
    # Gets the current date and time
    current_time = datetime.datetime.now()
    # Returns the current time in a formatted string
    return f'Точное время: {current_time}'


# Route for the /get_time/future endpoint
@app.route('/get_time/future')
def get_time_future():
  
    current_time = datetime.datetime.now()
    
    current_time_after_hour = current_time + datetime.timedelta(hours=1)
    # Returns the time one hour into the future in a formatted string
    return f'Точное время через час будет: {current_time_after_hour}'


def get_word_list():
    return re.findall(r'[a-zA-Zа-яА-Я]+', war_and_peace)



@app.route('/get_random_word')
def get_random_word():
  
    return random.choice(get_word_list())


# Route for the /counter endpoint
@app.route('/counter')
def counter():
    global visits
    # Increment the global visit counter
    visits += 1
    # Return the current visit count as a string
    return str(visits)


# This section runs the Flask app when the script is executed directly
if __name__ == '__main__':
    # Enable debug mode for easier development
    app.run(debug=True)
