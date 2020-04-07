from selenium import webdriver
from time import sleep
import dialogflow
from loginInfo import email, password

DIALOGFLOW_PROJECT_ID = 'diana-eoqlsq'
DIALOGFLOW_LANGUAGE_CODE = 'pl'
GOOGLE_APPLICATION_CREDENTIALS = 'diana-eoqlsq-98249f138627.json'
SESSION_ID = '118197476799899566966'


class TinderBot():
    def __init__(self):
        self.driver = webdriver.Chrome()


    def launchTinder(self):
        # uruchomienie aplikacji
        self.driver.get('https://tinder.com/')

        sleep(5)

        # znalezienie przycisku odpowiedzialnego za logowanie przy pomocy facebooka
        # loginButton = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/span/div[2]/button')
        # loginButton.click()

        try:
            moreOptions = self.driver.find_element_by_xpath("//button[@class='Td(u) Cur(p) Fw($medium) Tt(u)--ml focus-outline-style'][.='Więcej opcji']")
            if moreOptions is not None:
                moreOptions.click()
            sleep(2)
        except:
            pass

        try:
            loginByFB = self.driver.find_element_by_xpath("//button[@class='button Lts($ls-s) Z(0) CenterAlign Mx(a) Pos(r) Cur(p) Tt(u) Bdrs(100px) Px(48px) Px(40px)--s Py(0) Mih(54px) button--outline Bdw(2px) Bds(s) Trsdu($fast) Bdc($c-secondary) C($c-secondary) Bdc($c-base):h C($c-base):h Bdc($c-base):f C($c-base):f Bdc($c-base):a C($c-base):a Fw($semibold) focus-button-style Mb(20px)--ml W(100%)--ml W(100%)--s Fz(4vw)--s'][.='Zaloguj się przez Facebooka']")
            loginByFB.click()
            sleep(2)
        except:
            pass

        baseWindow = self.driver.window_handles[0]
        self.driver.switch_to_window(self.driver.window_handles[1])

        emailInput = self.driver.find_element_by_xpath('//*[@id="email"]')
        emailInput.send_keys(email)
        passwordInput = self.driver.find_element_by_xpath('//*[@id="pass"]')
        passwordInput.send_keys(password)
        confirmButton = self.driver.find_element_by_xpath('//*[@id="u_0_0"]')
        confirmButton.click()
        sleep(3)

        self.driver.switch_to_window(baseWindow)
        sleep(3)

        try:
            localizationButton = self.driver.find_element_by_xpath("//button[@class='button Lts($ls-s) Z(0) CenterAlign Mx(a) Cur(p) Tt(u) Ell Bdrs(100px) Px(24px) Px(20px)--s Py(0) Mih(40px) Pos(r) Ov(h) C(#fff) Bg($c-pink):h::b Bg($c-pink):f::b Bg($c-pink):a::b Trsdu($fast) Trsp($background) Bg($primary-gradient) button--primary-shadow StyledButton Fw($semibold) focus-button-style W(225px) W(a)'][.='Zezwól']")
            localizationButton.click()
            sleep(1)
        except:
            pass
        # noNotificationsButton = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/button[2]')
        try:
            noNotificationsButton = self.driver.find_element_by_xpath("//button[@class='button Lts($ls-s) Z(0) CenterAlign Mx(a) Cur(p) Tt(u) Ell Bdrs(100px) Px(24px) Px(20px)--s Py(0) Mih(40px) Fw($semibold) focus-button-style W(a) C($c-dark-gray)'][.='Nie interesuje mnie to']")
            noNotificationsButton.click()
        except:
            pass

        try:
            cookiesButton = self.driver.find_element_by_xpath("//button[@class='button Lts($ls-s) Z(0) CenterAlign Mx(a) Cur(p) Tt(u) Ell Bdrs(100px) Px(24px) Px(20px)--s Py(0) Mih(40px) button--outline Bdw(2px) Bds(s) Trsdu($fast) Bdc($c-secondary) C($c-secondary) Bdc($c-base):h C($c-base):h Bdc($c-base):f C($c-base):f Bdc($c-base):a C($c-base):a Fw($semibold) focus-button-style'][.='Wyrażam zgodę']")
            cookiesButton.click()
            sleep(1)
        except:
            pass

        try:
            noLocalizationChangeButton = self.driver.find_element_by_xpath("//button[@class='button Lts($ls-s) Z(0) CenterAlign Mx(a) Cur(p) Tt(u) Ell Bdrs(100px) Px(24px) Px(20px)--s Py(0) Mih(40px) Fw($semibold) focus-button-style C(#fff) Mb(8px)'][.='Nie, dziękuję']")
            noLocalizationChangeButton.click()
            sleep(1)
        except:
            pass


    def swipe(self):
        swipeLeftButton = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[2]/button')
        swipeRightButton = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[4]/button')

        try:
            # proba znalezienia trzeciego zdjecia, jesli nie ma -> swipe left
            self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[3]/div[1]/div[2]/button[3]')
            swipeRightButton.click()
        except:
            swipeLeftButton.click()
        finally:
            sleep(2)

        try:
            self.driver.find_element_by_xpath('//*[@id="modal-manager-canvas"]/div/div/div[1]/div/div[3]/a').click()
        except:
            pass
        sleep(1)
        
     def chat_bot(data, xd):
        session_client = dialogflow.SessionsClient();
        session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
        text_input = dialogflow.types.TextInput(text = data, language_code = DIALOGFLOW_LANGUAGE_CODE)
        query_input = dialogflow.types.QueryInput(text = text_input)
        response = session_client.detect_intent(session = session, query_input = query_input)
        if response:
            return response.query_result.fulfillment_text
        else:
            return ':)'


    def chat(self):
        messagesButton = self.driver.find_element_by_xpath('//*[@id="messages-tab"]')
        messagesButton.click()
        sleep(2)
        chat_windows = self.driver.find_elements_by_class_name('messageListItem')
        for convo in chat_windows:
            convo.click()
            sleep(3)
            all_messages = self.driver.find_elements_by_class_name('msg')
            last_message = all_messages[-1]
            #teraz sprawdzamy czy ostatnia wiadomość na czacie została napisana przez nas czy przez parę -
            #wiadomości napisane przez parę mają kolor #000
            if "C(#000)" in last_message.get_attribute('class').split():
                # Message might not have text, just emoji.
                last_message_text = last_message.find_element_by_xpath(".//span").text
                response = self.chat_bot(last_message_text)
                input_box = self.driver.find_element_by_class_name('sendMessageForm__input')
                input_box.send_keys(response)
                send_button = self.driver.find_element_by_class_name('sendMessageForm__input')
                send_button.click()
            x_button = self.driver.find_element_by_xpath('//a[@href="/app/matches"]')
            x_button.click()



a = TinderBot()
a.launchTinder()
for i in range(1, 5):
    a.swipe()
