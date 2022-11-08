from bs4 import BeautifulSoup
import requests
import datetime

user_response = input("What year do you want to travel to? Type the date in this format YYYY-MM-DD: ")


def validate_user_response(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        user_response = input("Sorry, that wasn't type out correctly. Please use this format when entering the date: YYYY-MM-DD: ")
        validate_user_response(user_response)


validate_user_response(user_response)

URL=f"https://www.billboard.com/charts/hot-100/{user_response}/"
response = requests.get(URL)
webpage = response.text

soup = BeautifulSoup(webpage, "html.parser")

results = soup.select("li ul li h3")
names = [result.text.strip() for result in results]

for name in names:
    print(name)