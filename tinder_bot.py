from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from time import sleep
import dialogflow
from loginInfo import email, password
import os
import dialogflow
server=smtplib.SMTP('smtp.gmail.com',587)

DIALOGFLOW_PROJECT_ID = 'diana-eoqlsq'
DIALOGFLOW_LANGUAGE_CODE = 'pl'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = './diana-eoqlsq-98249f138627.json'
SESSION_ID = '118197476799899566966'


class TinderBot():
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(chrome_options=options)


    def launchTinder(self):
        # uruchomienie aplikacji
        self.driver.get('https://tinder.com/')
        wait = WebDriverWait(self.driver, 5)


        # znalezienie przycisku odpowiedzialnego za logowanie przy pomocy facebooka
        # loginButton = self.driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/span/div[2]/button')
        # loginButton.click()

        try:
            moreOptions = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='Td(u) Cur(p) Fw($medium) Tt(u)--ml focus-outline-style'][.='Więcej opcji']")))
            moreOptions.click()
        except:
            pass 

        try:
            loginByFB = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='button Lts($ls-s) Z(0) CenterAlign Mx(a) Pos(r) Cur(p) Tt(u) Bdrs(100px) Px(48px) Px(40px)--s Py(0) Mih(54px) button--outline Bdw(2px) Bds(s) Trsdu($fast) Bdc($c-secondary) C($c-secondary) Bdc($c-base):h C($c-base):h Bdc($c-base):f C($c-base):f Bdc($c-base):a C($c-base):a Fw($semibold) focus-button-style Mb(20px)--ml W(100%)--ml W(100%)--s Fz(4vw)--s'][.='Zaloguj się przez Facebooka']")))
            loginByFB.click()
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

        self.driver.switch_to_window(baseWindow)

        try:
            localizationButton = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='button Lts($ls-s) Z(0) CenterAlign Mx(a) Cur(p) Tt(u) Ell Bdrs(100px) Px(24px) Px(20px)--s Py(0) Mih(40px) Pos(r) Ov(h) C(#fff) Bg($c-pink):h::b Bg($c-pink):f::b Bg($c-pink):a::b Trsdu($fast) Trsp($background) Bg($primary-gradient) button--primary-shadow StyledButton Fw($semibold) focus-button-style W(225px) W(a)'][.='Zezwól']")))
            localizationButton.click()
        except:
            pass

        try:
            noNotificationsButton = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='button Lts($ls-s) Z(0) CenterAlign Mx(a) Cur(p) Tt(u) Ell Bdrs(100px) Px(24px) Px(20px)--s Py(0) Mih(40px) Fw($semibold) focus-button-style W(a) C($c-dark-gray)'][.='Nie interesuje mnie to']")))
            noNotificationsButton.click()
        except:
            pass

        try:
            cookiesButton = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='button Lts($ls-s) Z(0) CenterAlign Mx(a) Cur(p) Tt(u) Ell Bdrs(100px) Px(24px) Px(20px)--s Py(0) Mih(40px) button--outline Bdw(2px) Bds(s) Trsdu($fast) Bdc($c-secondary) C($c-secondary) Bdc($c-base):h C($c-base):h Bdc($c-base):f C($c-base):f Bdc($c-base):a C($c-base):a Fw($semibold) focus-button-style'][.='Wyrażam zgodę']")))
            cookiesButton.click()
        except:
            pass

        try:
            noLocalizationChangeButton = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='button Lts($ls-s) Z(0) CenterAlign Mx(a) Cur(p) Tt(u) Ell Bdrs(100px) Px(24px) Px(20px)--s Py(0) Mih(40px) Fw($semibold) focus-button-style C(#fff) Mb(8px)'][.='Nie, dziękuję']")))
            noLocalizationChangeButton.click()
        except:
            pass


    def swipe(self):
        wait = WebDriverWait(self.driver, 5)
        swipeLeftButton = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[2]/button')))
        swipeRightButton = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[4]/button')))

        # proba znalezienia trzeciego zdjecia, jesli nie ma -> swipe left
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[3]/div[1]/div[2]/button[3]')))
            swipeRightButton.click()
        except:
            swipeLeftButton.click()
        # finally:
            # sleep(2)

        # zamkniecie ewentualnego powiadomienia o nowym matchu
        try:
            continueSwiping = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="modal-manager-canvas"]/div/div/div[1]/div/div[3]/a')))
            continueSwiping.click()
        except:
            pass
        # sleep(1)
        
        
    def chat_bot(self, xd, name_of_guy):
        #podłączenie dialog flow
        session_client = dialogflow.SessionsClient()
        session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
        text_input = dialogflow.types.TextInput(text=xd, language_code=DIALOGFLOW_LANGUAGE_CODE)
        query_input = dialogflow.types.QueryInput(text=text_input)
        response = session_client.detect_intent(session=session, query_input=query_input)

        #sprawdzanie czy intent jest typu propozycja spotkania
        if(response.query_result.intent.display_name == "meeting prop"):
            self.send_mail(name_of_guy)

        if response:
            return response.query_result.fulfillment_text
        else:
            return ':)'


    def chat(self):
        wait = WebDriverWait(self.driver, 5)
        messagesButton = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="messages-tab"]')))
        # messagesButton = self.driver.find_element_by_xpath('//*[@id="messages-tab"]')

        messagesButton.click()
        sleep(2)

        # chat_windows = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'messageListItem')))
        chat_windows = self.driver.find_elements_by_class_name('messageListItem')
        for convo in chat_windows:
            convo.click()
            sleep(3)
            # all_messages = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'msg')))
            all_messages = self.driver.find_elements_by_class_name('msg')
            last_message = all_messages[-1]
            # last_message = all_messages[0]
            print(str(last_message))
            name_of_guy = #ZNALEŹĆ ŚCIEŻKĘ

            #teraz sprawdzamy czy ostatnia wiadomość na czacie została napisana przez nas czy przez parę -
            #wiadomości napisane przez parę mają kolor #000
            if "C(#000)" in last_message.get_attribute('class').split():
                # Message might not have text, just emoji.
                last_message_text = last_message.find_element_by_xpath(".//span").text
                print(last_message_text)/main/div[1]/div/div/div[1]/div/div[2]/div[2]/button')))
        swipeRightButton = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[4]/button')))

        # proba znalezienia trzeciego zdjecia, jesli nie ma -> swipe left
        try:
            wait.until(EC.element_t
                print(str(last_message_text))
                response = self.chat_bot(last_message_text, name_of_gut)/main/div[1]/div/div/div[1]/div/div[2]/div[2]/button')))
        swipeRightButton = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[4]/button')))



#mordo co to tu robi
        # proba znalezienia trzeciego zdjecia, jesli nie ma -> swipe left
        try:
            wait.until(EC.element_t

                input_box = self.driver.find_element_by_class_name('sendMessageForm__input')
                input_box.send_keys(response)
                send_button = self.driver.find_element_by_xpath('//form/button[@type="submit"]')
                send_button.click()
            try:
                x_button = self.driver.find_element_by_xpath('//a[@href="/app/matches"]')
                x_button.click()
            except:
                pass


     def send_mail(self, name_of_guy):
        #wysyłanie powiadomienia o randce

        message = MIMEText("You've got a new date invitation from", name_of_guy)
        message["From"] = email
        message["To"] = email
        message["Subject"] = "Tinder date"

        server.sendmail(email, email, message.as_string())
        
        
      #tu będzie filtrowanie bio
    def bio_filter(self, bio):
                       
       #tu będzie szukanie twarzy
    def face_detector(self, pics)
        



a = TinderBot()
a.launchTinder()
for i in range (0, 10)
  for j in range(0, 10):
     a.swipe()
  a.chat()
