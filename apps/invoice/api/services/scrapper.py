import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException

class DIANScraper:
    
    def __init__(self, chrome_driver_path="http://selenium:4444/wd/hub", url="https://catalogo-vpfe.dian.gov.co/User/SearchDocument"):
        self.chrome_driver_path = chrome_driver_path
        self.url = url
        self.driver = None

    def _get_driver(self):
        """Returns a WebDriver instance configured with Chrome options."""
        options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications": 2}
        options.add_experimental_option("prefs", prefs)
        driver = webdriver.Remote(
                command_executor=self.chrome_driver_path,
                options=options
                )

        return driver


    def _wait_and_click(self, locator):
        """Clicks on an element after waiting for it to be clickable within 10 seconds."""
        try:
            element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(locator))
            element.click()
        except TimeoutException:
            print(f"Error: Element not clickable within 10 seconds - {locator}")

    def _find_and_extract_data(self, container_locator, data_points):
        """Extracts data from a container element based on provided data points."""
        data = {}
        data_elements = self.driver.find_elements(By.CSS_SELECTOR, container_locator)
        data_elements = [element.text for element in data_elements]
        data_elements = [obj.replace("\n", " ") for obj in data_elements]

        for i, element in enumerate(filter(None, data_elements[:2])):
            nit_match = re.search(r'NIT: (\d+)', element)
            nombre_match = re.search(r'Nombre: (.+)$', element)
            if nit_match and nombre_match:
                data[data_points[i * 2]] = nit_match.group(1)
                data[data_points[i * 2 + 1]] = nombre_match.group(1)

        return data

    def _search_by_cufe(self, cufe):
        """Searches for an invoice by its CUFE on the DIAN website."""
        try:
            cufe_field = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[id='DocumentKey']")))
            cufe_field.clear()
            cufe_field.send_keys(cufe)

            self._wait_and_click((By.CSS_SELECTOR, "button"))
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".row-fe-details")))
        except TimeoutException:
            raise NoSuchElementException(f"No se encontraron documentos con el CUFE proporcionado")

    def _extract_invoice_events(self):
        """Extracts invoice event data from the DIAN website."""
        eventos_factura_rows = self.driver.find_elements(By.CSS_SELECTOR, "#container1 tbody tr")
        eventos_factura = []
        for row in eventos_factura_rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            event = {
                "Código": cells[0].text,
                "Descripción": cells[1].text,
                "Fecha": cells[2].text,
                "Nit Emisor": cells[3].text,
                "Emisor": cells[4].text,
                "Nit Receptor": cells[5].text,
                "Receptor": cells[6].text,
            }
            if any(event.values()):
                eventos_factura.append(event)
        return eventos_factura

    def _get_pdf_url(self):
        """Attempts to retrieve the PDF URL for the invoice."""
        try:
            enlace_pdf = self.driver.find_element(By.CSS_SELECTOR, "a.downloadPDFUrl")
            url_pdf = enlace_pdf.get_attribute("href")
        except NoSuchElementException:
            url_pdf = None
        return url_pdf

    def scrape_invoice_data(self, cufe):
        """
        Scrapes invoice data from the DIAN website.

        Args:
            cufe (str): The CUFE (Unique Electronic Invoice ID) of the invoice.

        Return the scraped data as a dictionary.
        """
        self.driver = self._get_driver()

        try:
            self.driver.get(self.url)
            self._search_by_cufe(cufe)

            eventos_factura = self._extract_invoice_events()
            data_points = [
                "DATOS DEL EMISOR NIT",
                "DATOS DEL EMISOR Nombre",
                "DATOS DEL RECEPTOR NIT",
                "DATOS DEL RECEPTOR Nombre",
            ]
            datos_factura = self._find_and_extract_data(".row-fe-details:nth-of-type(2) > div:nth-child(-n+2) p", data_points)
            url_pdf = self._get_pdf_url()

            data = {
                "invoice_events": eventos_factura,
                "datos": datos_factura,
                "graphic_representation": url_pdf,
            }

            return data
        finally:
            self.driver.quit()
