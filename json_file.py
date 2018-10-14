import json

a = [
            {
              "wednesday": {
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
              "summary": "Good that you ate Brocolli, next time avoid cheese and noodles. Too Bad!!",
              "day": "Wednesday"
            },
            {
              "thursday": {
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
              "day": "Thursday"
            },
            {
              "sunday": {
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
              "day": "Sunday"
            }
          ]

def return_base_json():
    return a
