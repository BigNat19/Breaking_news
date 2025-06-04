import requests
from bs4 import BeautifulSoup

print("Welcome to my headline printer!")

try:
    from googlesearch import search
except ImportError:
    print("No module named 'google' found")
    exit()

user_input = input("Search: ")
query = user_input.replace(" ", ".")

links = []
for j in search(query, num=10, stop=10):
    links.append(j)

for idx, link in enumerate(links, start=1):
    print(f"{idx}. {link}")

user_num = int(input("Which link would you like to access (num)? "))
selected_link = links[user_num - 1]

response = requests.get(selected_link)

soup = BeautifulSoup(response.content, "html.parser")
headlines = soup.find_all('h3')

if not headlines:
    print("Error! Please check website!")
else:
    for headline in headlines:
        start_value = ord('.')  # ASCII value of '.'
        numbered_text = ""
        for i, line in enumerate(headline.text.strip().split('\n'), start=start_value):
            # Convert the integer back to character
            char_start = chr(i)
            # Append character start to line
            numbered_text += f"{char_start}. {line}\n"

        print(numbered_text)