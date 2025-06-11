'''
Import request, bs4, and search.
Search the web for user input.
Store the links in a dictionary and output 10 of them.
Ask the user to pick one.
Sends a GET request to the selected page, Includes a User-Agent header
to make the request look like it's coming from a real browser (helps prevent getting blocked by the site).
Parses the HTML of the page.
Searches for all headline tags: <h1>, <h2>, and <h3>.
If no headlines were found, warns the user.
Prints the headlines.
'''

import requests
from bs4 import BeautifulSoup

# Get search results from Google
def get_search_results(query):
    from googlesearch import search
    return [j for j in search(query, num=10, stop=10)]

# Let the user select one of the links
def select_link(links):
    print("\nSearch Results:")
    for idx, link in enumerate(links, start=1):
        print(f"{idx}. {link}")
    user_num = int(input("Which link would you like to access (num)? "))
    return links[user_num - 1]

# Scrape the headlines from the chosen URL
def get_headlines_from_url(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup.find_all(['h1', 'h2', 'h3']), soup

# Print all headlines and return them in a list
def print_headlines(headlines):
    if not headlines:
        print("Error! No headlines found on this site.")
        return []
    
    print("\nHeadlines:")
    cleaned = []
    for i, tag in enumerate(headlines, start=1):
        text = tag.get_text(strip=True)
        cleaned.append(tag)  # Save original tag
        print(f"{i}. {text}")
    return cleaned

# Count how many different headlines include the keyword
def count_keyword_in_headlines(headlines, keyword):
    keyword = keyword.lower()
    matching = []

    for tag in headlines:
        text = tag.get_text(strip=True)
        if keyword in text.lower():
            matching.append(text)

    print(f"\nThe keyword '{keyword}' was found in {len(matching)} headline(s).")

    if matching:
        show = input("Would you like to see the matching headlines? (yes/no): ").lower()
        if show == "yes":
            print("\nMatching Headlines:")
            for h in matching:
                print(f"- {h}")

# Show detailed content near the selected headline
def show_headline_details(headline_tag):
    print("\n--- Full Content Near the Headline ---\n")
    # Print the headline text again
    print(f"Headline: {headline_tag.get_text(strip=True)}\n")

    # Print paragraphs that come after the headline in the HTML
    next_tag = headline_tag.find_next_sibling()
    count = 0
    while next_tag and count < 5:  # limit to first few paragraphs
        if next_tag.name == 'p':
            print(next_tag.get_text(strip=True))
            count += 1
        next_tag = next_tag.find_next_sibling()

    if count == 0:
        print("No additional content found under this headline.")

# Main program logic
def main():
    print("Welcome to my headline printer!")

    try:
        user_input = input("Search: ")
        query = user_input.replace(" ", ".")
        links = get_search_results(query)

        selected_link = select_link(links)
        headlines, soup = get_headlines_from_url(selected_link)

        headline_tags = print_headlines(headlines)

        if headline_tags:
            keyword = input("\nEnter a keyword to search for in the headlines: ")
            count_keyword_in_headlines(headlines, keyword)

            # Ask user if they want to select a headline for more details
            view = input("\nDo you want to see more content under a headline? (yes/no): ").lower()
            if view == "yes":
                choice = int(input("Enter the number of the headline: "))
                if 1 <= choice <= len(headline_tags):
                    show_headline_details(headline_tags[choice - 1])
                else:
                    print("Invalid choice.")

    except ImportError:
        print("No module named 'google' found")
    except Exception as e:
        print(f"An error occurred: {e}")

# Entry point
if __name__ == "__main__":
    main()
