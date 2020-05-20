import codecs

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import re
import time
import smtplib
from email.mime.text import MIMEText
import cv2
import sys
from io import BytesIO
from time import sleep
import dialogflow
import os
from fer import FER
from loginInfo import email, password, faceLibraryPath, savePicturesDirectory
server = smtplib.SMTP('smtp.gmail.com', 587)
DIALOGFLOW_PROJECT_ID = 'diana-eoqlsq'
DIALOGFLOW_LANGUAGE_CODE = 'pl'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = './diana-eoqlsq-98249f138627.json'
SESSION_ID = '118197476799899566966'


# server.login(email,password)


class TinderBot():
    keywords: []
    keywordsVerification: []
    keywordsVerificationKey: []
    paths: []

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(chrome_options=options)
        self.keywordsVerificationKey = []
        with open("keywords", "r") as keywordsFile, open("keywordsVerification", "r") as keywordsVerificationFile,\
                codecs.open("paths", "r", "utf-8") as pathsFile:
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

            # pobranie xpathow z pliku
            self.paths = pathsFile.readlines()
            for i in range(0, len(self.paths)):
                tmp = re.split("\n", self.paths[i])
                self.paths[i] = tmp[0]
                tmp = re.split(" \+ ", self.paths[i])
                self.paths[i] = tmp[1]

    def launchTinder(self):
        # uruchomienie aplikacji
        self.driver.get('https://tinder.com/')
        wait = WebDriverWait(self.driver, 5)

        # przyciskow szukamy zawsze w bloku try zeby nie wyrzucalo bledu
        # jak nie znajdzie bo nie zawsze znaczy to ze trzeba przerwac program

        # 0 -> privacyButton, 1 -> moreOptions, 2 -> loginByFB
        buttons = []
        for i in range(0, 3):
            try:
                buttons.append(wait.until(EC.element_to_be_clickable((By.XPATH, self.paths[i]))))
                buttons[len(buttons) - 1].click()
            except:
                pass

        baseWindow = self.driver.window_handles[0]
        self.driver.switch_to_window(self.driver.window_handles[1])

        emailInput = self.driver.find_element_by_xpath(self.paths[3])
        emailInput.send_keys(email)
        passwordInput = self.driver.find_element_by_xpath(self.paths[4])
        passwordInput.send_keys(password)
        confirmButton = self.driver.find_element_by_xpath(self.paths[5])
        confirmButton.click()

        self.driver.switch_to_window(baseWindow)

        # 6 -> localizationButton, 7 -> noNotificationsButton, 8 -> cookiesButton, 9 -> noLocalizationChangeButton
        for i in range(6, 10):
            try:
                buttons.append(wait.until(EC.element_to_be_clickable((By.XPATH, self.paths[i]))))
                buttons[len(buttons) - 1].click()
            except:
                pass

    def swipe(self, i):
        wait = WebDriverWait(self.driver, 5)

        # if self.checkPhotos() and self.checkDescription():
        p = self.checkPhotos()
        q = self.checkDescription()
        r = self.findFace(i)
        # photoElement = self.driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[3]/div[1]/div[1]/div/div[4]/div/div')
        # photoElement = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[3]/div[1]/div[1]/div/div[1]/div/div')))
        # photoPath = photoElement.get_attribute("src")
        # r = self.findFace(photoPath)

        # if p and q and r:
        if p and q:
            swipeRightButton = wait.until(EC.element_to_be_clickable((By.XPATH, self.paths[10])))
            swipeRightButton.click()
        else:
            continueSwiping = wait.until(EC.element_to_be_clickable((By.XPATH, self.paths[12])))
            continueSwiping.click()

        # zamkniecie ewentualnego powiadomienia o nowym matchu
        try:
            continueSwiping = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="modal-manager-canvas"]/div/div/div[1]/div/div[3]/a')))
            continueSwiping.click()
        except:
            pass

        # nie dodanie skrotu na pulpit
        try:
            dontAddShortcut = wait.until(EC.element_to_be_clickable((By.XPATH, self.paths[13])))
            dontAddShortcut.click()
        except:
            pass


    def chat_bot(self, xd, name_of_guy):

        session_client = dialogflow.SessionsClient()
        session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
        text_input = dialogflow.types.TextInput(text=xd, language_code=DIALOGFLOW_LANGUAGE_CODE)
        query_input = dialogflow.types.QueryInput(text=text_input)
        response = session_client.detect_intent(session=session, query_input=query_input)
        # sprawdzanie czy intent jest typu propozycja spotkania

        if response.query_result.intent.display_name == "meeting prop":
            # jesli intent wiadomości to meeting prop - w Dialogflow folder z propozycjami spotkania
            # wysyłamy email
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
        messagesButton = wait.until(EC.element_to_be_clickable((By.XPATH, self.paths[14])))
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
            # teraz sprawdzamy czy ostatnia wiadomość na czacie została napisana przez nas czy przez parę -
            # wiadomości napisane przez parę mają kolor #000
            if "C(#000)" in last_message.get_attribute('class').split():
                # Message might not have text, just emoji.
                last_message_text = last_message.find_element_by_xpath(".//span").text
                print(last_message_text)
                print(str(last_message_text))
                name_of_guy = self.driver.find_element_by_xpath(self.paths[15])
                response = self.chat_bot(last_message_text, name_of_guy)
                input_box = self.driver.find_element_by_class_name('sendMessageForm__input')
                input_box.send_keys(response)
                send_button = self.driver.find_element_by_xpath(self.paths[16])
                send_button.click()
            try:
                x_button = self.driver.find_element_by_xpath(self.paths[17])
                x_button.click()
            except:
                pass

    def checkDescription(self):
        wait = WebDriverWait(self.driver, 5)
        profileOk = True
        try:
            # rozwiniecie opisu
            descriptionButton = wait.until(EC.element_to_be_clickable((By.XPATH, self.paths[18])))
            descriptionButton.click()

            description = wait.until(EC.presence_of_element_located((By.XPATH, self.paths[19]))).text

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
        exitDescription = wait.until(EC.element_to_be_clickable((By.XPATH, self.paths[20])))
        exitDescription.click()
        return profileOk


    # proba znalezienia trzeciego zdjecia, jesli nie ma -> swipe left
    def checkPhotos(self):
        wait = WebDriverWait(self.driver, 3)
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, self.paths[21])))
            return True
        except:
            return False


    def findFace(self, i):
        flag = False
        wait = WebDriverWait(self.driver, 5)

        if not os.path.exists(savePicturesDirectory):
            os.makedirs(savePicturesDirectory)

        self.driver.get_screenshot_as_file('screenshot' + str(i) + '.png')
        img.append(cv2.imread('screenshot' + str(i) + '.png'))
        face_cascade = cv2.CascadeClassifier(faceLibraryPath)

        crop_img.append(img[i][100:230, 1000:1300])

        cv2.imwrite("cropp" + str(i) + ".png", crop_img[i])
        img1.append(cv2.imread('cropp' + str(i) + '.png'))
        photoGray.append(cv2.cvtColor(img1[i], cv2.COLOR_BGR2GRAY))
        faces.append(face_cascade.detectMultiScale(
            photoGray[i],
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        ))

        if (x == 0):
            print("no face detected")
            cv2.imwrite(savePicturesDirectory + str(i) + ".png", img1[i])
        else:
            detector = FER()
            emotion, score = detector.top_emotion(img1[i])
            print(emotion, score)

            if (emotion == 'angry' or emotion == 'sad') and score > 0.9:
                print('too angry for me')
                cv2.imwrite(savePicturesDirectory + str(i) + ".png", img1[i])

            else:
                print('Perfect')
                flag = True
        return flag


bot = TinderBot()
bot.launchTinder()
img1 = []
photoGray = []
crop_img = []
img = []
faces = []
for i in range(0, 15):
    bot.swipe(i)
    bot.chat()
