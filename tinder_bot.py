from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import re
import smtplib
from email.mime.text import MIMEText
import cv2
import sys
from io import BytesIO
from time import sleep
import dialogflow
import os


from loginInfo import email, password


server=smtplib.SMTP('smtp.gmail.com',587)


DIALOGFLOW_PROJECT_ID = 'diana-eoqlsq'
DIALOGFLOW_LANGUAGE_CODE = 'pl'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = './diana-eoqlsq-98249f138627.json'
SESSION_ID = '118197476799899566966'
# server.login(email,password)


class TinderBot():
    keywords: []
    keywordsVerification: []
    keywordsVerificationKey: []

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(chrome_options=options)
        self.keywordsVerificationKey = []
        with open("keywords", "r") as keywordsFile, open("keywordsVerification", "r") as keywordsVerificationFile:
            self.keywords = keywordsFile.readlines()
            self.keywordsVerification = keywordsVerificationFile.readlines()
            for i in range(0, len(self.keywordsVerification)):
                # usuniecie znaku konca linii
                tmp = re.split("\n", self.keywordsVerification[i])
                self.keywordsVerification[i] = tmp[0]
                # podział pliku weryfikujacego (klucz:wartosci)
                tmp = re.split(":", self.keywordsVerification[i])
                self.keywordsVerificationKey.append(tmp[0])
                # podział wartości zeby potem sprawdzac je w opisie
                self.keywordsVerification[i] = re.split(", ", tmp[1])

   def launchTinder(self):
        # uruchomienie aplikacji
        self.driver.get('https://tinder.com/')
        wait = WebDriverWait(self.driver, 5)

        # zawsze w bloku try zeby nie wyrzucalo bledu jak nie znajdzie
        try:
            privacyButton = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div[1]/button/span")))
            privacyButton.click()
        except:
            pass

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
            # localizationButton = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='button Lts($ls-s) Z(0) CenterAlign Mx(a) Cur(p) Tt(u) Ell Bdrs(100px) Px(24px) Px(20px)--s Py(0) Mih(40px) Pos(r) Ov(h) C(#fff) Bg($c-pink):h::b Bg($c-pink):f::b Bg($c-pink):a::b Trsdu($fast) Trsp($background) Bg($primary-gradient) button--primary-shadow StyledButton Fw($semibold) focus-button-style W(225px) W(a)][.='Zezwól']")))
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

        # if self.checkPhotos() and self.checkDescription():
        p = self.checkPhotos()
        q = self.checkDescription()
        
        photoElement = self.driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[3]/div[1]/div[1]/div/div[4]/div/div')
        photoPath = photoElement.get_attribute("src")
        r = self.findFace(photoPath)
        
        if p and q and r:
            swipeRightButton = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div[1]/div[2]/div/div/div[4]/button')))
            swipeRightButton.click()
        else:
            swipeLeftButton = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div[1]/div[2]/div/div/div[2]/button')))
            swipeLeftButton.click()

        # zamkniecie ewentualnego powiadomienia o nowym matchu
        try:
            continueSwiping = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="modal-manager-canvas"]/div/div/div[1]/div/div[3]/a')))
            continueSwiping.click()
        except:
            pass

    def chat_bot(self, xd, name_of_guy):
        session_client = dialogflow.SessionsClient()
        session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
        text_input = dialogflow.types.TextInput(text=xd, language_code=DIALOGFLOW_LANGUAGE_CODE)
        query_input = dialogflow.types.QueryInput(text=text_input)
        response = session_client.detect_intent(session=session, query_input=query_input)
        #sprawdzanie czy intent jest typu propozycja spotkania
        
        if(response.query_result.intent.display_name == "meeting prop"):
            #jesli intent wiadomości to meeting prop - w Dialogflow folder z propozycjami spotkania
            #wysyłąmy email
            self.send_mail(name_of_guy)
            return 'daj mi się zastanowić :)'
            
        if response:
            return response.query_result.fulfillment_text
        else:
            return ':)'

    def send_mail(self, name_of_guy):
        message = MIMEText("You've got a new date invitation from", name_of_guy)
        message["From"] = email
        message["To"] = email
        message["Subject"] = "Tinder date"

        server.sendmail(email, email, message.as_string())


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
            # last_message = all_messages   [0]
            print(str(last_message))
            #teraz sprawdzamy czy ostatnia wiadomość na czacie została napisana przez nas czy przez parę -
            #wiadomości napisane przez parę mają kolor #000
            if "C(#000)" in last_message.get_attribute('class').split():
                # Message might not have text, just emoji.
                last_message_text = last_message.find_element_by_xpath(".//span").text
                print(last_message_text)
                print(str(last_message_text))
                name_of_guy = self.driver.find_element_by_xpath('//*[@id="matchListWithMessages"]/div[2]/a[1]/div[2]/div[1]/div/h3')
                response = self.chat_bot(last_message_text, name_of_guy)
                input_box = self.driver.find_element_by_class_name('sendMessageForm__input')
                input_box.send_keys(response)
                send_button = self.driver.find_element_by_xpath('//form/button[@type="submit"]')
                send_button.click()
            try:
                x_button = self.driver.find_element_by_xpath('//a[@href="/app/matches"]')
                x_button.click()
            except:
                pass

    def checkDescription(self):
        wait = WebDriverWait(self.driver, 5)
        profileOk = True
        try:
            # rozwiniecie opisu
            # descriptionButton = self.driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[3]/div[6]/button/svg/path')
            descriptionButton = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[3]/div[6]/button')))
            descriptionButton.click()

            description = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[2]/div[2]"))).text
            # description = None

            print("OPIS:\n", description)
            if description == [] or description is None:
                profileOk = False

            # szukamy czy zakazane slowo/wyrazenie wystepuje na stronie
            for i in range(0, len(self.keywords)):
                if self.keywords[i] in description:
                    word = self.keywords[i].lower()
                    profileOk = False
                    # jesli wystepuje, szukamy czy jest to fraza ktora nie jest zakazana
                    for j in range(0, len(self.keywordsVerificationKey)):
                        if word == self.keywordsVerificationKey[j]:
                            for k in self.keywordsVerification[j] and not profileOk:
                                if k in description:
                                    profileOk = True

        except:
            profileOk = False

        # zamkniecie opisu
        exitDescription = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[1]/span/a[1]')))
        exitDescription.click()
        return profileOk

    # proba znalezienia trzeciego zdjecia, jesli nie ma -> swipe left
    def checkPhotos(self):
        wait = WebDriverWait(self.driver, 5)
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[3]/div[1]/div[2]/button[3]')))
            return True
        except:
            return False

    def findFace(self, photoPath):
        #pobieramy zdjęcie z adresu url
        cascPath = "data/haarcascades/haarcascade_frontalface_default.xml"
        faceDetector = cv2.CascadeClassifier(cascPath)
        photo = cv2.imread(photoPath)
        cv2.imshow('image', photo)
        photoGray = cv2.cvtColor(photo, cv2.COLOR_BGR2GRAY)
        #konwertujemy zdjęcie do skali szarości
        faces = faceDetector.detectMultiScale(
            photoGray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        #szukamy twarzy
        #nie znaleziono twarzy
        if(len(faces) == 0):
            return False
        else:
        #nie znaleziono twarzy
            return True






bot = TinderBot()
bot.launchTinder()
for a in range(0, 15):
    bot.swipe()
# a.chat()
