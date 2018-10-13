#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 13 01:06:04 2018

@author: kits
"""

from flask import Flask, request, jsonify
import preprocessing
# import urllib2
import urllib.parse
app = Flask(__name__)


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

@app.route('/getFooodHistory')
def getFoodHistory():
    # For testing purposes
    return jsonify({
              "item": [
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
              ]
            })
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port = 5000)
