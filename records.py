import requests
from bs4 import BeautifulSoup

# Specify the URL of the page containing the search form
url = 'https://empresite.eleconomista.es/'

# Send a GET request to the URL and store the response
response = requests.get(url)

# Create a BeautifulSoup object to parse the HTML content of the response
soup = BeautifulSoup(response.content, 'html.parser')

# Find the form element that contains the search fields
form = soup.find('input', {'class':"text01 mr4"})
print(form)
# Extract the names of the search fields

name_fields = [field.get('name') for field in form.find_all('input')]

# Specify the search parameters 
params = {
    name_fields[0]: 'Search query 1',  # Replace with your search query
    name_fields[1]: 'Search query 2',  # Replace with your search query
    # Add more search parameters as necessary
}

# Send a POST request to the search form URL with the search parameters
response = requests.post(url, data=params)

# Create a BeautifulSoup object to parse the HTML content of the response
soup = BeautifulSoup(response.content, 'html.parser')

# Find the total number of search results
total_results = soup.find('strong', {'class': 'text-primary'}).text

# Calculate the number of pages based on the total number of results and the number of results per page
results_per_page = 25  # This may vary depending on the website's settings
num_pages = int(total_results / results_per_page) + 1

# Loop through all the search result pages and extract the data
for page in range(1, num_pages + 1):
    # Send a GET request to the search result page URL
    page_url = f'{url}page-{page}'
    response = requests.get(page_url)

    # Create a BeautifulSoup object to parse the HTML content of the response
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the data from the search results
    # Add your code here to extract the data you need

