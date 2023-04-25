from bs4 import BeautifulSoup
import requests
from validate_email import validate_email

url = 'https://empresite.eleconomista.es/SOLBIOSUR.html'

reply = requests.get(url)

soup = BeautifulSoup(reply.content, 'html.parser')

email_tag = soup.find('span', {'class': 'email'})

# Replace with the email address you want to check
print(email_tag)