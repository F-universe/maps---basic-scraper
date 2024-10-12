Google Maps Scraper
This project is a simple Flask web application that uses Selenium to automate searching for a place on Google Maps, and extracts specific content from the resulting page. The web application allows users to input a location and retrieve relevant text associated with a specific jslog attribute on Google Maps.

Features
Automated search on Google Maps via Selenium.
Extracts text related to specific map elements (e.g., places, descriptions).
Displays results on a Flask-powered web page.
Designed to allow internationalization by changing the language of interface text.
How to Use
Clone the repository:

bash

git clone https://github.com/yourusername/google-maps-scraper.git
cd google-maps-scraper
Install the required dependencies:

bash

pip install flask selenium
Make sure to download and place the correct version of ChromeDriver for your Chrome version in the appropriate folder. You will need to update the path in the Python code:

python

chromedriver_path = r'C:\path\to\chromedriver.exe'
Start the Flask server by running the Python script:

bash

python maps.py
Open your browser and go to http://127.0.0.1:5000.

Internationalization
The current implementation is in English, but you can easily adjust the application to support your preferred language. To do this:

Open the maps.py file.
Find all the logging and user-facing messages written in English (such as "Search for {place} sent" or "Google Maps page loaded").
Replace these messages with their equivalent in your desired language.
For example:

python

logging.debug("Página de Google Maps cargada")  # Spanish
Adjust the template files in the templates directory if any further localization is required.
Dependencies
Flask – Micro web framework for building the web interface.
Selenium – Tool for automating web browsers.
Required PIP Installs:
Make sure you have the following Python packages installed:

bash

pip install flask selenium
Notes
Browser Compatibility: This project is designed to work with Chrome and requires ChromeDriver to be installed. Make sure your chromedriver.exe is compatible with your version of Chrome.
Google Maps Accessibility: This script is designed to work with the layout of Google Maps as of the time of writing. If Google updates its interface, the script might need adjustments to work correctly.
