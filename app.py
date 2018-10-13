#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 13 01:06:04 2018

@author: kits
"""

from flask import Flask
import preprocessing
import abc

app = Flask(__name__)


@app.route('/<name>')
def query_example(name):
    words = preprocessing.process(name)
    string = ''
    for word in words:
        string = string+' ' + word
    return string

@app.route('/entry')
def entry():
    return "What did you have for breakfast today"

@app.route('/breakfast/<food>')
def breakfast(food):
    food_keywords = preprocessing.process(food)
    abc.thismeal(food_keywords)
    return "And how about lunch"

@app.route('/lunch/<food>')
def lunch(food):
    food_keywords = preprocessing.process(food)
    abc.thismeal(food_keywords)
    return "What was for dinner"

@app.route('/dinner/<food>')
def dinner(food):
    food_keywords = preprocessing.process(food)
    abc.thismeal(food_keywords)
    return "Did you have anything else throughout the day"

@app.route('/misc/<food>') 
def misc(food):
    food_keywords = preprocessing.process(food)
    abc.thismeal(food_keywords)
    return "Great! I have all the information stored."

@app.route('/negative')
def negativeResponse():
    return "Okay. We can add the rest of the information later."

@app.route('/feedback')
def getFeedback():
    feedback = abc.getMealFeedback()
    return feedback

if __name__ == '__main__':
    app.run(debug=True, port = 5000)
