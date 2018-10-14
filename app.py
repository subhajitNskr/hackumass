#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 13 01:06:04 2018

@author: kits
"""

import pandas as pd
import numpy as np
import os

from flask import Flask, request, jsonify
# import urllib2
import urllib.parse
import meal_query_from_input
import sys
import Documents.nutri as nutri

app = Flask(__name__)

pre = os.path.dirname(os.path.realpath(__file__))
fname = 'dataset.xlsx'
path = os.path.join(pre, fname)
data_xls = pd.read_excel(path)
np_data = data_xls.values
nutriInst = nutri.NutritionManager(np_data)

@app.route('/<name>')
def query_example(name):
    name = urllib.parse.unquote(name)
    # name = urllib2.unquote(name)
    words = preprocessing.process(name)
    string = ''
    for word in words:
        string = string+' ' + word
    return jsonify({'name':name})
    return string

@app.route('/entry')
def entry():
    return "What did you have for breakfast today"

@app.route('/breakfast/<input_string>')
def breakfast(input_string):
    food = urllib.parse.unquote(input_string)
    food_keywords = meal_query_from_input.find_meal(food)
    abc.thismeal(food_keywords)
    response = "And how about lunch"
    return jsonify([{'response': response}])

@app.route('/lunch/<input_string>')
def lunch(food):
    food = urllib.parse.unquote(input_string)
    food_keywords = meal_query_from_input.find_meal(food)
    abc.thismeal(food_keywords)
    response = "What was for dinner"
    return jsonify([{'response': response}]) 

@app.route('/dinner/<input_string>')
def dinner(food):
    food = urllib.parse.unquote(input_string)
    food_keywords = meal_query_from_input.find_meal(food)
    abc.thismeal(food_keywords)
    response = "Did you have anything else throughout the day"
    return jsonify([{'response': response}])

@app.route('/misc/<input_string>')
def misc(food):
    food = urllib.parse.unquote(input_string)
    food_keywords = meal_query_from_input.find_meal(food)
    abc.thismeal(food_keywords)
    response = "Great! I have all the information stored."
    return jsonify([{'response': response}])

@app.route('/negative')
def negativeResponse():
    return "Okay. We can add the rest of the information later."

@app.route('/alexa/feedback')
def getFeedback():
    feedback = "Here is your feedback."
#    pre = os.path.dirname(os.path.realpath(__file__))
#    fname = 'dataset.xlsx'
#    path = os.path.join(pre, fname)
#    data_xls = pd.read_excel(path)
#    np_data = data_xls.values
    nutriInst = nutri.NutritionManager.getInstance()
    feedback = nutriInst.get_feedback("bbb")
    return jsonify([{'response': feedback}])

@app.route('/getFooodHistory')
def getFoodHistory():
    # For testing purposes
    return jsonify([
                {
                  "meals": {
                    "breakfast": [],
                    "lunch": [
                      "cheese",
                      "noodles"
                    ],
                    "dinner": [
                      "rice",
                      "brocolli",
                      "salads"
                    ]
                  },
                  "summary": "Good that you ate Brocolli, next time avoid cheese and noodles",
                  "day": "Wednesday"
                },
                {
                  "meals": {
                    "breakfast": [],
                    "lunch": [
                      "tuna",
                      "salad"
                    ],
                    "dinner": [
                      "caesar",
                      "salads"
                    ]
                  },
                  "summary": "Good that you ate Brocolli, next time avoid cheese and noodles",
                  "day": "Wednesday"
                },
                {
                  "meals": {
                    "breakfast": [],
                    "lunch": [
                      "tuna",
                      "noodles"
                    ],
                    "dinner": [
                      "rice",
                      "rajma"
                    ]
                  },
                  "summary": "Good that you ate Brocolli, next time avoid cheese and noodles",
                  "day": "Wednesday"
                }
              ])

@app.route('/alexa/<input_string>')
def getResponse(input_string):
    ip = urllib.parse.parse_qs(input_string)
    food = ip['Food']
    time_of_day = ip['Time'][0]
    print(food, file=sys.stderr)
    nutriInst.add_meal("bbb", 100, food, time_of_day)
    response_list = ['Cool.', 'Great!', 'Seems like you had a good meal.', 'I hope you enjoyed your meal!']
    response = response_list[np.random.randint(len(response_list))] + ' Do you want to add other meals?'
    return jsonify([{'response': response}])     

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port = 5000)

    
