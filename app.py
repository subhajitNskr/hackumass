#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 13 01:06:04 2018

@author: kits
"""

from flask import Flask, request
import preprocessing

app = Flask(__name__)


@app.route('/<name>')
def query_example(name):
    words = preprocessing.process(name)
    string = ''
    for word in words:
        string = string+' ' + word
    return string

if __name__ == '__main__':
    app.run(debug=True, port = 5000)
