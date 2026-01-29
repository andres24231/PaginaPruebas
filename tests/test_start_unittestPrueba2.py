import unittest

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager
    SELENIUM_AVAILABLE = True
except Exception:
    SELENIUM_AVAILABLE = False


@unittest.skipUnless(SELENIUM_AVAILABLE, "selenium or webdriver-manager not installed; skipping web tests")
class TestPaginaInicio(unittest.TestCase):

    def setUp(self):
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.get("https://tu-pagina.github.io/PaginaPruebas")

    def test_titulo(self):
        self.assertIn("Pagina", self.driver.title)

    def test_url(self):
        self.assertTrue("PaginaPruebas" in self.driver.current_url)

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
