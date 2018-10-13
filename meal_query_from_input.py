from fuzzywuzzy import process
import pickle


with open('truncated_dict.pkl', 'rb') as file:
	truncated_dict = pickle.load(file)
with open('set_of_keywords.pkl', 'rb') as file:
	set_of_keywords = pickle.load(file)

def find_meal(meal_string):
	list_of_vals = [*truncated_dict]
	search_string = ""
	for i in meal_string.split(" "):
		if i in set_of_keywords:
			search_string += (i + " ")

	search_string = search_string.strip()
	return truncated_dict[process.extract(search_string, list_of_vals, limit = 1)[0][0]]

print(find_meal("I had rice and beef today"))