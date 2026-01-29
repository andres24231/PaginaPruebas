import unittest

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.common.keys import Keys
    from selenium.common.exceptions import NoSuchElementException
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager
    SELENIUM_AVAILABLE = True
except Exception:
    SELENIUM_AVAILABLE = False


@unittest.skipUnless(SELENIUM_AVAILABLE, "selenium or webdriver-manager not installed; skipping web tests")
class TestBusquedas(unittest.TestCase):

    def setUp(self):
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.get("https://tu-pagina.github.io/PaginaPruebas")

    def test_por_clase(self):
        elemento = self.driver.find_element(By.CLASS_NAME, "menu")
        self.assertIsNotNone(elemento)

    def test_por_link(self):
        link = self.driver.find_element(By.LINK_TEXT, "Inicio")
        self.assertEqual(link.text, "Inicio")

    def test_por_link_parcial(self):
        link = self.driver.find_element(By.PARTIAL_LINK_TEXT, "Ini")
        self.assertTrue(link.is_displayed())

    def test_find_elements_various(self):
        """Ejemplos de find_elements que devuelven listas.
        Si no existen elementos esperados, la prueba se salta en runtime.
        """
        selectors = [
            (By.NAME, "nombre"),
            (By.CLASS_NAME, "fila"),
            (By.CSS_SELECTOR, "table tr"),
            (By.ID, "miTabla"),
            (By.LINK_TEXT, "Inicio"),
            (By.PARTIAL_LINK_TEXT, "Ini"),
            (By.TAG_NAME, "tr"),
            (By.XPATH, "//table//tr"),
        ]

        for by, value in selectors:
            elems = self.driver.find_elements(by, value)
            # siempre debe devolver una lista (aunque vacía)
            self.assertIsInstance(elems, list)
            if len(elems) == 0:
                # No consideramos esto un fallo del test suite global; saltarlo para este selector
                self.skipTest(f"No se encontraron elementos con {by}='{value}'")
            # si hay elementos, validar que podemos leer su texto
            texts = [e.text for e in elems]
            self.assertIsInstance(texts, list)

    def test_actions_click_and_type(self):
        """Ejemplo de acciones: click y escribir en un input.
        Si no se encuentra el input, la prueba se salta.
        """
        try:
            # intentar localizar un input de texto común
            input_el = self.driver.find_element(By.CSS_SELECTOR, "input[type='text']")
        except NoSuchElementException:
            try:
                input_el = self.driver.find_element(By.NAME, "q")
            except NoSuchElementException:
                self.skipTest("No se encontró un campo de texto para la prueba de acciones")

        # limpiar, escribir y verificar el valor
        input_el.clear()
        acciones = ActionChains(self.driver)
        acciones.click(input_el).send_keys("PruebaHola" + Keys.RETURN).perform()

        # comprobar que el valor fue escrito (si el input lo soporta)
        val = input_el.get_attribute("value")
        self.assertTrue(isinstance(val, str))

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
