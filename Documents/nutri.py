# -*- coding: utf-8 -*-
"""
Created on Sat Oct 13 01:21:26 2018
@author: subha
"""

import pandas as pd
import numpy as np
import os
import datetime
import json
from json import JSONEncoder
from fuzzywuzzy import process
import pickle
import random
feedbacks = []

def modify_name(x) :
    x = x.split(', ')
    if(len(x) == 1) :
        return x[0]
    else:
        return str(x[1] +" "+ x[0])

class NutritionManager:
    __instance = None
   
    @staticmethod
    def getInstance():
        if NutritionManager.__instance == None:
            NutritionManager()
        return NutritionManager.__instance
    
    def __init__(self, database = None) :
        if NutritionManager.__instance != None:
            self.users = {}
            self.database = database
            NutritionManager.__instance = self
        else :
            self.users = {}
            self.database = database
            NutritionManager.__instance = self


    def add_user(self, name):
        if name in self.users:
            return Exception("Username already exists")
        else:
            new_user = UserInfo(name)
            self.users[name] = new_user

    ##################To Be done###############################
    def  get_food_score(self, food):
        with open('truncated_dict.pkl', 'rb') as td:
            truncated_dict = pickle.load(td)
        with open('set_of_keywords.pkl', 'rb') as sk:
            set_of_keywords = pickle.load(sk)
            
        list_of_vals = [*truncated_dict]
        search_string = ""
        for i in food.split(" "):
            if i in set_of_keywords:
                search_string += (i + " ")
        
        search_string = search_string.strip()
        # print(process.extract(search_string, list_of_vals, limit = 1))
        index = truncated_dict[process.extract(search_string, list_of_vals, limit = 1)[0][0]]
        row_0 = data_xls['Food code']
        for r in range(len(row_0)):
            if (row_0.loc[r]) == index:
                row_val = r


        calorie_val = 0
        sugar_val = 0
        colesterol_val = 0
        fat_val = 0
        try:
            calorie_val = np_data[row_val, 2]
            sugar_val = np_data[row_val, 4]
            colesterol_val = np_data[row_val, 8]
            fat_val = np_data[row_val, 7]
        except:
            KeyError
        print("Individual Scores : ", calorie_val, colesterol_val, sugar_val, fat_val)
        return calorie_val, colesterol_val, sugar_val, fat_val
    ###########################################################


    def add_meal(self, name, food_ids, meal_info, meal_type):  # food_ids = < 100, 121> meal_info = "rice, pork"
        if name in self.users:
            self.users[name].add_user_meal(meal_info, meal_type)
            
        else:
            self.add_user(name)
            self.users[name].add_user_meal(meal_info, meal_type)
            

    def get_meal_score(self, name, meal_type):
        if meal_type != "lunch" or meal_type != "breakfast" or meal_type != "dinner" or meal_type != "misc":
            return Exception("invalid meal")
        now = datetime.datetime.now()
        date = str(now.day) + "-" + str(now.month) + "-" + str(now.year)
        if name in self.users:
            all_meals_for_a_day = self.users[name].meal_dicts[date]
            for meal in all_meals_for_a_day:
                if meal.meal_type == meal_type:
                    return meal.get_meal_score
        else :
            return Exception("Username not found")


    def get_day_meal_score(self, name) :
        if name in self.users:
            now = datetime.datetime.now()
            date = str(now.day) + "-" + str(now.month) + "-" + str(now.year) 
            return self.users[name].day_dict[date]
        else:
            return Exception("Username not found")
        
    def get_food_history(self, name):
        for user_info in self.users.values():
            print(user_info.get_user_history())
    
    def get_feedback(self, name, meal_type = None):
        now = datetime.datetime.now()
        date = str(now.day) + "-" + str(now.month) + "-" + str(now.year)
        count = len(self.users[name].meal_dict[date])
        if count == 0 :
            return Exception("No food data")
        if meal_type != None:
            meal_score = self.get_meal_score(name, meal_type)
            return meal_score.get_feedback(count)
        else:         
            meal_score = self.get_day_meal_score(name)
            return meal_score.get_feedback(count)
    
    def return_food_histroy(self, name):
        if name in self.users:
            # print("food history")
            r = UserInfoEncoder().encode(self.users[name].meal_dict)
            r = json.loads(r)
            feedback = self.get_feedback(name)
            day_activities = {}
            for key in r:
                print(type(r))
                for meal in r[key]:
                    if meal["meal_type"] == 'breakfast':
                        day_activities["breakfast"] = meal["food_list"]
                    if meal["meal_type"] == 'lunch':
                        day_activities["lunch"] = meal["food_list"]
                    if meal["meal_type"] == 'dinner':
                        day_activities["dinner"] = meal["food_list"]

                    day_activities["summary"] = feedback
                    day_activities["day"] = datetime.datetime.today().strftime("%A")

            print(day_activities)
            return json.dumps(day_activities)
        
class UserInfoEncoder(JSONEncoder):
    def default(self, o) :
        return o.__dict__
    
class UserInfo:
    def __init__(self, name):
        self.name = name
        self.day_dict = {}
        self.meal_dict = {}
        #user infos
        self.max_calorie = 0
        self.height = 0
        self.weight = 0
        
        self.bmi = 0
        self.cholestorol = False
        #self.user_score = UserScore()
    
    #debug 
    def get_user_history(self):
        #print(self.name)
        for day in self.meal_dict:
            #print(day)
            for meal in self.meal_dict[day]:
                meal.get_meal_info()
        
        
    def calculate_bmi(self):
        if self.height == 0 :
            self.bmi = 0
        else :
            self.bmi = 703*self.weight/self.height**2
    
    def add_user_info(self, height = 0 , weight = 0, hascholestorol = False):
        self.height = height
        self.weight = weight
        self.calculate_bmi()
        self.cholestorol = hascholestorol
        self.user_score.update_user_score(height, weight)

    def add_user_meal(self, food_list = None, meal_type = None):
        now = datetime.datetime.now()
        date = str(now.day) + "-" + str(now.month) + "-" + str(now.year) 
        meal = Meal(food_list, meal_type)
        if date in self.meal_dict:
            self.meal_dict[date].append(meal)
        else :
            meal_list = []
            meal_list.append(meal)
            self.meal_dict[date] = meal_list
            self.day_dict[date] = MealScore()
            
        meal_score  = self.calculate_meal_score(self.meal_dict[date])
        self.update_meal_score(meal_score)

    
    def update_meal_score(self, meal_score):
        now = datetime.datetime.now()
        date = str(now.day) + "-" + str(now.month) + "-" + str(now.year) 
        self.day_dict[date].update_score(meal_score)
        
################################# TO BE DONE ##################################
    def calculate_meal_score(self, meals):
        nutritionMgr = NutritionManager.getInstance()
        
        meal_score = MealScore()
        #if nutritionMgr == None:
        #    return meal_score
        for meal in meals:
            for food in meal.get_food_list():
                score = nutritionMgr.get_food_score(food)
                # print(score)
                meal_score.update_score_individual(score[0], score[1], score[2], score[3] )
        return meal_score
    
"""
    def calculate_scores(self) :
        nutritionMgr = NutritionManager.getInstance()
        meal_score = MealScore()
        for meal in self.meal_list:
            for food in meal:
                meal_score.update_score(nutritionMgr.get_food_score(food))
    
"""
    
        

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

    def get_meal_score(self) :
        return self.meal_score   
    
    #debug utility
    def get_meal_info(self):
        # print(self.meal_type)
        for food in self.food_list :
            print(food)
    
    def get_food_list(self):
        return self.food_list

      

class MealScore:
    def __init__(self) :
        self.calorie_val = 0
        self.colesterol_val = 0
        self.sugar_val = 0
        self.fat_val = 0
        self.feedback = ""
        
    def set_score(self, calorie_val, colesterol_val, sugar_val, fat_val):
        self.calorie_val = calorie_val
        self.colesterol_val = colesterol_val
        self.sugar_val = sugar_val
        self.fat_val = fat_val
    
    def update_score_individual(self, calorie_val, colesterol_val, sugar_val, fat_val):
        self.calorie_val += calorie_val
        self.colesterol_val += colesterol_val
        self.sugar_val += sugar_val
        self.fat_val += fat_val
        # # print("debug")
        # print(self.calorie_val)
        
        
    def update_score(self, meal_score):
        self.calorie_val = meal_score.calorie_val
        self.colesterol_val = meal_score.colesterol_val
        self.sugar_val = meal_score.sugar_val
        self.fat_val = meal_score.fat_val
        self.feedback = meal_score.feedback
        # print("debug")
        # print(self.calorie_val)
        
    def get_calorie_val(self):
        return self.calorie_val
    def get_colesterol_val(self):
        return self.colesterol_val 
    def sugar_val(self):
        return self.sugar_val 
    def fat_val(self):
        return self.fat_val
    def get_feedback(self, count):
        if count == 0:
            count = 1
        self.evaluate_feedback(count)
        return self.feedback
    
    def evaluate_feedback(self, count):
        self.calorie_val /= count
        self.colesterol_val /= count
        self.sugar_val /= count
        self.fat_val /= count
        print(self.calorie_val, self.colesterol_val, self.sugar_val, self.fat_val, count)

        calorie_score = 0 
        if self.calorie_val < 50:
            calorie_score = -1
        
        elif self.calorie_val > 500:
            calorie_score = 1

        
        sugar_score = -1
        if self.sugar_val > 30:
            sugar_score = 1

        colesterol_score = -1
        if self.colesterol_val > 25:
            colesterol_score = 1

        fat_score = -1
        if self.fat_val > 78 / 3 :
            fat_score = 1

        if calorie_score == 0 and sugar_score == 0 and colesterol_score == 0 and fat_score ==0 :
            self.feedback = ["Keep it going.", "You're doing great", "High Five on having a good diet"][random.randrange(3)]

        elif colesterol_score > 0 :
            self.feedback = ["You should watch out your cholesterol", "You need to eat healthier", "Try to avoid cholesterol"][random.randrange(3)]

        elif sugar_score > 0:
            print(self.sugar_val, sugar_score)
            self.feedback = ["Try to reduce your sugar intake", "You need to control your sweet tooth"][random.randrange(2)]

        elif calorie_score > 0:
            self.feedback = ["You've been taking in too many calories", "You need to control your calorie intake", "You should reduce your diet"][random.randrange(3)]

        elif fat_score > 0:
            self.feedback = ["Avoid fat", "Avoid food with saturated and trans fats", "Try low fat food options"][random.randrange(3)]

        elif calorie_score < 0:
            self.feedback = ["Please eat something", "Eat something", "You're not eating enough food"][random.randrange(3)]
        else :
            self.feedback = ["Good job"][random.randrange(3)]


class UserScore:
    def __init__(self) :
        self.feedback_score = 0
        self.feedback = ""
        self.bmi = 0
    
    def get_feedback(self):
        return self.feedback
    def get_feedback_score(self):
        return self.feedback_score
    def get_bmi(self):
        return self.bmi
    def update_user_score(self, height, weight):
        if height == 0 :
            self.bmi = 0
        else :
            self.bmi = 703*weight/height**2
        

#
pre = os.path.dirname(os.path.realpath(__file__))
fname = 'dataset.xlsx'
path = os.path.join(pre, fname)
## print(path)
data_xls = pd.read_excel(path)
## print(data_xls.shape)
#data_xls.dropna()
#column_to_drop = data_xls.columns[49:68]
#data_xls.drop(column_to_drop, axis=1, inplace = True)
#column_to_drop = data_xls.columns[16:30]
#data_xls.drop(column_to_drop, axis=1, inplace = True)
#column_to_drop = data_xls.columns[14:15]
#
#data_xls.drop(column_to_drop, axis =1, inplace = True)
#column_to_drop = data_xls.columns[43:44]
#data_xls.drop(column_to_drop, axis =1, inplace = True)
#column_to_drop = data_xls.columns[47:48]
#data_xls.drop(column_to_drop, axis =1, inplace = True)
#column_to_drop = data_xls.columns[10:13]
#data_xls.drop(column_to_drop, axis =1, inplace = True)
## print(data_xls.shape)
##print(modify_name("milk, human"))
#
np_data = data_xls.values
##print(np_data)
## print("modified_ data")
## for i in range(1, np_data.shape[0]): #np_data.shape[0]):
##     np_data[i, 1] = modify_name(np_data[i, 1])
#
## print(np_data)
#
#nutriInst = NutritionManager(np_data)
##nutriInst.add_meal("aaa", 100, ["rice, pork"], "dinner")
## nutriInst.add_meal("bbb", 100, ["rice, eggs"], "lunch")
#nutriInst.add_meal("bbb", 100, ["cereal"], "dinner")
#nutriInst.get_food_history("bbb")
#nutriInst.return_food_histroy("bbb")
## print(nutriInst.get_day_meal_score("aaa").calorie_val)
## print (nutriInst.get_feedback("aaa"))
