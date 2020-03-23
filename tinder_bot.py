from selenium import webdriver
from time import sleep

class TinderBot():
    def __init__(self):
        self.driver = webdriver.Chrome()

    def launchTinder(self):
        # uruchomienie aplikacji
        self.driver.get('https://tinder.com/')

        sleep(5);
        # znalezienie przycisku odpowiedzialnego za logowanie przy pomocy facebooka
        loginButton = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/span/div[2]/button')
        loginButton.click()

        baseWindod = self.driver.window_handles[0]
        self.driver.switch_to_window(self.driver.window_handles[1])

        emailInput = self.driver.find_element_by_xpath('//*[@id="email"]')
        emailInput.send_keys('dianarakoln@gmail.com')
        passwordInput = self.driver.find_element_by_xpath('//*[@id="pass"]')
        passwordInput.send_keys('tinderbot')
        confirmButton = self.driver.find_element_by_xpath('//*[@id="u_0_0"]')
        confirmButton.click()
        sleep(3)

        self.driver.switch_to_window(baseWindod)
        sleep(2)
        localizationButton = self.driver.find_element_by_xpath('// *[ @ id = "modal-manager"] / div / div / div / div / div[3] / button[1]')
        localizationButton.click()
        noNotificationsButton = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/button[2]')
        noNotificationsButton.click()

a = TinderBot()
a.launchTinder()