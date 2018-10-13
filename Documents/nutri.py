# -*- coding: utf-8 -*-
"""
Created on Sat Oct 13 01:21:26 2018

@author: subha
"""

import pandas as pd
import numpy as np
import os
import datetime


def modify_name(x) :
    x = x.split(', ')
    if(len(x) == 1) :
        return x[0]
    else:
        return str(x[1] +" "+ x[0])

class NutritionManager:
    __instance = None
    @staticmethod
    def getInstance(database):
        if NutritionManager.__instance == None:
            NutritionManager(database)
        return NutritionManager.__instance
    
    def __init__(self, database = None) :
        if NutritionManager.__instance != None:
            return Exception("Nutrition manager is a singleton class")
        else :
            self.users = set()
            self.database = database
    def add_user(self, name):
        if name in self.users:
            return Exception("Username already exists")
        else:
            new_user = UserInfo(name)
            self.users.insert(new_user)
    def  get_food_score(self, food):
        return get_nearest_score(food)
    
    def add_meal(self, name, meal):
        if name in self.users:
            self.users[name].add_user_meal(meal)
        else:
            self.add_user(name)
            self.users[name].add_user_meal(meal)


class UserInfo:
    def __init__(self, name):
        self.name = name
        self.day_dict = {}
        self.meal_dict = {}
        self.max_calorie = 0
        self.height = 0
        self.weight = 0
        self.cholestorol = False
        self.user_score = UserScore()
        
    def add_user_meal(self, food_list = None, meal_type = None):
        now = datetime.datetime.now()
        date = str(now.day) + "-" + str(now.month) + "-" + str(now.year) 
        meal = Meal(food_list, meal_type)
        if date in self.meal_dict:
            self.meal_dict[date].add(meal)
        else :
            meal_list = []
            meal_list.add(meal)
            self.meal_dict[date] = meal_list
            self.day_dict[date] = MealScore()
            
        meal_score = self.calculate_meal_score(meal)
        self.update_meal_score(date, meal_score)
        return
    
        
    def calculate_meal_score(self, meal):
        for food in meal:
            meal_score += NutritionManager.get_food_score(food)
        
        return meal_score
    
    def calculate_scores(self) :
        nutritionMgr = NutritionManager.getInstance()
        for meal in self.meal_list:
            for food in meal:
                meal_score += nutritionMgr.get_food_score(food)
    
       
class Meal:
    def __init__(self,  food_list = None, meal_type = None):
        if meal_type is None:
            self.meal_type = 'misc'
        else:
            self.meal_type = meal_type
        
        self.food_list = food_list
        self.meal_score = MealScore()
        self.score = 0
        if food_list == None:
            self.isSkipped = True
        
        
class score:
    def __init__(self):
        self.calorie_val = 0
        self.colesterol_val = 0
        self.sugar_val = 0
        self.alcohol_val = 0

class MealScore:
    def __init__(self) :
        score.__init__()
        self.feedback = ""
    def set_score(): 
        return 0
        
class UserScore:
    def __init__(self) :
        self.feedback_score = 0
        self.feedback = ""
        self.bmi = 0
    
            


pre = os.path.dirname(os.path.realpath(__file__))
fname = 'FNDDS_food_value.xlsx'
path = os.path.join(pre, fname)
print(path)
data_xls = pd.read_excel(path)
print(data_xls.shape)
data_xls.dropna()
column_to_drop = data_xls.columns[49:68]
data_xls.drop(column_to_drop, axis=1, inplace = True)
column_to_drop = data_xls.columns[16:30]
data_xls.drop(column_to_drop, axis=1, inplace = True)
column_to_drop = data_xls.columns[14:15]

data_xls.drop(column_to_drop, axis =1, inplace = True)
column_to_drop = data_xls.columns[43:44]
data_xls.drop(column_to_drop, axis =1, inplace = True)
column_to_drop = data_xls.columns[47:48]
data_xls.drop(column_to_drop, axis =1, inplace = True)
column_to_drop = data_xls.columns[10:13]
data_xls.drop(column_to_drop, axis =1, inplace = True)
print(data_xls.shape)
print(modify_name("milk, human"))

np_data = data_xls.values
#print(np_data)
print("modified_ data")
for i in range(1, np_data.shape[0]): #np_data.shape[0]):
    np_data[i, 1] = modify_name(np_data[i, 1])

print(np_data)
nutriInst = NutritionManager(np_data)