from selenium import webdriver

from webdriver_manager.chrome import ChromeDriverManager
from time import sleep;

class TinderBot():
    def __init__(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

	def launchTinder(self):
		self.driver.get('https://tinder.com') #uruchomienie aplikacji

        sleep(5);
		loginButton = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/span/div[2]/button')
		#znalezienie przycisku odpowiedzialnego za logowanie przy pomocy facebooka
		loginButton.click()

		baseWindow = self.driver.window_handles[0]
        self.driver.switch_to_window(self.driver.window_handles[1])
        #w tym momencie otwiera się nowe okno, gdzie wprowadzamy dane do logowania

        emailInput = self.driver.find_element_by_xpath('//*[@id="email"]')
        emailInput.send_keys('dianarakoln@gmail.com')
        #wprowadzamy email
        passwordInput = self.driver.find_element_by_xpath('//*[@id="pass"]')
        passwordInput.send_keys('tinderbot')
        #wprowadzamy hasło

        confirmButton = self.driver.find_element_by_xpath('//*[@id="u_0_0"]')
        confirmButton.click()
        #potwierdzamy logowanie
        sleep(3)

        self.driver.switch_to_window(baseWindow)
        sleep(2)
        localizationButton = self.driver.find_element_by_xpath(
            '// *[ @ id = "modal-manager"] / div / div / div / div / div[3] / button[1]')
        localizationButton.click()
        #ustawiamy lokalizację

        noNotificationsButton = self.driver.find_element_by_xpath(
            '//*[@id="modal-manager"]/div/div/div/div/div[3]/button[2]')
        noNotificationsButton.click()
        #wyłączamy powiadomienia

    a = TinderBot()
    a.launchTinder()
