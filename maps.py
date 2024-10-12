from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from flask import Flask, request, render_template
import logging
import time

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

# Funzione per creare e configurare il driver Chrome
def create_driver():
    chromedriver_path = r'C:\Users\fabio\OneDrive\Desktop\chromedriver-win64 (1)\chromedriver-win64\chromedriver.exe'
    chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

    options = Options()
    options.binary_location = chrome_path
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')

    service = ChromeService(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=service, options=options)
    return driver

# Funzione per cercare e scaricare il contenuto di un elemento su Google Maps
def search_google_maps(place):
    driver = create_driver()
    found_class_1 = "no"
    found_class_2 = "no"
    nested_class_content = "no"

    try:
        # Carica Google Maps
        driver.get('https://www.google.it/maps')
        logging.debug("Pagina di Google Maps caricata")

        # Gestione dei cookies
        try:
            accept_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[contains(@aria-label, "Accetta tutto")]'))
            )
            accept_button.click()
            logging.debug("Cliccato su 'Accetta tutto' per i cookies")
        except Exception as e:
            logging.debug(f"Nessun popup di cookies trovato o errore nel cliccare: {e}")

        # Trova la barra di ricerca e invia il luogo da cercare
        search_box = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, 'searchboxinput'))
        )
        logging.debug("Trovata la barra di ricerca")

        search_box.clear()
        search_box.send_keys(place)
        search_box.send_keys(Keys.RETURN)
        logging.debug(f"Ricerca per '{place}' inviata")

        # Attendi che la mappa venga caricata
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'canvas.widget-scene-canvas'))
        )
        logging.debug("Canvas della mappa caricato")

        # Cerca l'elemento con jslog e scarica il testo
        try:
            element_with_jslog = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//*[@jslog[contains(., "25795;metadata")]]'))
            )
            nested_class_content = element_with_jslog.text
            logging.debug(f"Trovato elemento con jslog contenente '25795;metadata': {nested_class_content}")
        except Exception as e:
            logging.debug(f"Errore durante la ricerca dell'elemento con jslog '25795;metadata': {e}")

    except Exception as e:
        logging.debug(f"Errore nella richiesta: {e}")

    finally:
        if driver:
            driver.quit()

    # Restituisce il risultato delle ricerche
    return {"class_1": found_class_1, "class_2": found_class_2, "nested_class": nested_class_content}

# Route principale per il form e la visualizzazione dei risultati
@app.route('/')
def index():
    return render_template('index.html', results=[], total_pages=0)

# Route per la ricerca su Google Maps
@app.route('/search', methods=['POST'])
def google_maps_search():
    query = request.form['query']
    result = search_google_maps(query)
    return render_template('index.html', results=[result], found_text=result['nested_class'])

if __name__ == '__main__':
    app.run(debug=True)