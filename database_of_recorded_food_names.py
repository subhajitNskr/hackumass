import datetime
import json_file
import sys

class database:
    def __init__(self):
        self.json = json_file.return_base_json()

    def appendToDatabase(self, string):
        with open("database.csv", "a") as myfile:
            myfile.write(string)

    def addToDatabase(self, foodNames):
        now = datetime.datetime.now()
        hour = now.hour
        time_of_day = ''
        if hour<=10:
            time_of_day = 'Breakfast'
        elif hour>10 and hour<=18:
            time_of_day = 'Lunch'
        else:
            time_of_day = 'Dinner'

        day = now.strftime("%A")
        print("day -> ", day)
        csv_text = day + "," + time_of_day + "," + foodNames + "\n"
        self.add_to_json(day, time_of_day, foodNames)
        self.appendToDatabase(csv_text)

    def add_to_json(self, day, time_of_day, foodNames):
        try:
            foodNames = foodNames.split(';')
            foodNames = [x.strip() for x in foodNames]
            foodNames = [x for x in foodNames if x != '']
            print("foodName", foodNames)
            for days in self.json:
                print(days.keys())
                if day.lower() in days.keys() or day.title() in days.keys():
                    print("current day", days[day.lower()][time_of_day.lower()], day)
                    days[day.lower()][time_of_day.lower()] += foodNames
                    days[day.lower()][time_of_day.lower()] = list(set(days[day.lower()][time_of_day.lower()]))
                    print("current day", days[day.lower()][time_of_day.lower()], day)
            print(self.json)
        except:
            print("Error in function add_to_json", sys.exc_info())
            return

if __name__ == '__main__':
    db = database()
    db.add_to_json('Sunday', 'lunch', 'Rice; And; Beef;')
