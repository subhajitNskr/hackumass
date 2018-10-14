from flask import Flask
from flask_ask import Ask, statement, question, session
import json
import requests
import time
import urllib
import logging
import sys

app = Flask(__name__)
ask = Ask(app, "/alexa")
backend_url = "https://cebd9d6b.ngrok.io/alexa/"
context = "Initial context"

# logging.getLogger('flask_ask').setLevel(logging.DEBUG)

def get_(subquery):
	data = requests.get(backend_url + subquery, headers={'User-Agent':'test'})
	print(data.text, file=sys.stderr)
	print(subquery, file=sys.stderr)
	return json.loads(data.text, encoding='utf8')

def get_feedback():
    data = requests.get(backend_url + 'feedback', headers={'User-Agent':'test'})
    print(data.text, file=sys.stderr)
    return json.loads(data.text, encoding='utf8')


@app.route('/')
def homepage():
	return "hello"

@ask.launch
def start_skill():
	welcome_message = "Hi! Let's talk about what you ate today?"
	return question(welcome_message)



@ask.intent("FoodSearch")
def search_food(Food, Time):
    global context
    context = "Food Search"
	query = {'Food' : Food, 'Time' : Time}
	reply_query = get_(urllib.parse.urlencode(query))
	return question(reply_query[0]['response'])


@ask.intent("AMAZON.NoIntent")
def no_intent():
    global context
    if(context == "Food Search"):
        text = 'Do you want to know how you did today?'
        context = "Feedback"
        return question(text)
    else:
        text = 'Okay then... Bye'
        return statement(text)

@ask.intent("AMAZON.YesIntent")
def yes_intent():
    global context
    if (context == "Food Search"):
        text = 'Okay! I\'m listening. Go on?'
        return question(text)
    else:
        reply = get_feedback()
        context = "Feedback"
        return statement(reply[0]['summary'])
    

@ask.intent("AMAZON.FallbackIntent")
def fallback_intent():
    text = 'Sorry. I didn\'t catch that. Please try again?'
    return question(text)

if __name__=='__main__':
	app.run(debug=True)
