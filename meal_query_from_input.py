from fuzzywuzzy import process
import pickle
from database_of_recorded_food_names import database
import re

with open('truncated_dict.pkl', 'rb') as file:
	truncated_dict = pickle.load(file)
with open('set_of_keywords.pkl', 'rb') as file:
	set_of_keywords = pickle.load(file)
banned_words = ['appetizer', 'breakfast', 'dainty', 'delicious', 'dessert',
				'dinner',  'food',  'leftovers',  'lunch',  'meal',  'micronutrient',
				'multivitamin', 'ration', 'supper', 'vintage', 'vitamin', 'for', 'and', 'with']
# print (truncated_dict)
def find_meal(meal_string):
	list_of_vals = [*truncated_dict]
	search_string = ""
	for i in meal_string.split(" "):
		if i in set_of_keywords:
			search_string += (i + " ")

	search_string = search_string.title().strip()
	return truncated_dict[process.extract(search_string, list_of_vals, limit = 1)[0][0]]

def find_meal_to_store_data(meal_string):
	list_of_vals = [*truncated_dict]
	search_string = ""
	for i in meal_string.lower().split(" "):
		i = " ".join(re.findall("[a-zA-Z]+", i))
		if i in set_of_keywords and i not in banned_words:
			search_string += (i + "; ")

	search_string = search_string.title().strip()
	return truncated_dict[process.extract(search_string, list_of_vals, limit = 1)[0][0]], search_string
	print("See the process", process.extract(search_string, list_of_vals, limit = 1)[0], search_string)
	db = database()
	db.addToDatabase(search_string)
	return truncated_dict[process.extract(search_string, list_of_vals, limit = 1)[0][0]]

# print(find_meal("I had rice and beef today"))
# print(find_meal_to_store_data("I had rice and beef today"))
# print(find_meal_to_store_data("Hello! I ate broccoli, rice and meat for dinner."))
# print(find_meal_to_store_data("I ate egg and cheese for breakfast along with bacon"))
# print (len(truncated_dict), truncated_dict[11360000])
