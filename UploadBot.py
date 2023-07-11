import os
import sys
import time
import re
import my_variables
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import selenium.common.exceptions as sexp
import pandas as pd
import logging

sys.path.insert(1, os.getcwd() + "\\venv\\Lib\\site-packages")


class UploadBot:
    def __init__(self, action, id_elem_to_modify, instance, username, password, level):
        # ============ Data from GUI
        self.action = action
        self.idElements = id_elem_to_modify.split(",")
        self.instance = instance
        self.username = username
        self.password = password
        self.level = level

        # ============== Driver options
        self.options = Options()
        # options.add_argument('--headless') #Hide GUI
        self.options.add_argument("--windows-size=1920, 1080")
        self.options.add_argument("start-maximized")
        self.options.add_experimental_option("prefs", {"profile.managed_default_content_setting.images": 2})
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.rawPath = os.getcwd()
        self.Path = self.rawPath.replace("\\", "/") + "/"

        self.driver = None
        # ================ Logging
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        logging.basicConfig(format='%(asctime)s - %(message)s', filename=f"log_{instance}.log", level=logging.INFO)
        self.logger = logging.getLogger(f"Bot{id_elem_to_modify}")
        # =============== Other
        self.modified_quiz_count = 0
        self.questions_answers_to_upload = []
        self.trophy_string = {}
        self.isTrophy = False
        self.isInternational = False
        self.idElement = ''

    def start_bot(self):
        self.driver = webdriver.Chrome(options=self.options)
        url = "https://" + self.instance
        self.driver.get(url)
        element = WebDriverWait(driver=self.driver, timeout=20).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, "#username")))
        self.login()

    def login(self):
        email = self.driver.find_element(By.ID, "username")
        password = self.driver.find_element(By.ID, "password")

        email.send_keys(self.username)
        password.send_keys(self.password)

        self.driver.find_element(By.ID, "loginbtn").click()
        element = WebDriverWait(driver=self.driver, timeout=20).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, "#region-main-box")))
        print(f"LOGIN as {self.username}, instance: {self.instance}, element: {self.idElements}, action: {self.action}")
        self.logger.info(
            f"LOGIN as {self.username}, instance: {self.instance}, element: {self.idElements}, action: {self.action}")
        self.goto_level_page()

    def goto_level_page(self):
        try:
            levels_buttons = self.driver.find_elements(By.XPATH,
                                                       "//ul[@id='livelli']//li//div[@class='text-center']//a")
            lvl_url = levels_buttons[int(self.level) - 1].get_attribute("href")
        except IndexError:
            self.logger.warning("Wrong username or passoword...closing browser")
            print("Wrong username or passoword...closing browser")
            self.driver.quit()
        lvl_url = lvl_url.split("#", 1)[0]
        for el_id in self.idElements:
            self.idElement = el_id.upper()
            print(f"start upload {self.idElement}")
            self.logger.info(f"start upload {self.idElement}")
            if self.idElement.startswith("C"):
                self.isTrophy = True
                self.trophy_number_to_string()
            if self.instance == "international.cyberguru.it":  # International id = 5
                self.isInternational = True
            if self.action == "Upload video":
                self.get_video_strings()
            else:
                self.get_element_strings()
            self.driver.get(lvl_url)
            # =========================================================================================== MODULE PAGE ======
            element = WebDriverWait(driver=self.driver, timeout=20).until(
                ec.presence_of_element_located((By.CSS_SELECTOR, "#section-0")))
            if self.isTrophy:
                self.get_trophy_url_overview_page()
            else:
                self.get_quiz_url_overview_page()

    def get_quiz_url_overview_page(self):
        selected_module_elements = self.driver.find_elements(By.XPATH, "//span[contains(text(), '" + str(
            self.idElement) + "')]/../../a")
        module_links = []
        module_lessons = []
        module_quizzes = []
        for modl in selected_module_elements:
            url_buffer = modl.get_attribute("href")
            module_links.append(url_buffer)
            if "lesson" in url_buffer:
                module_lessons.append(url_buffer)
            if "quiz" in url_buffer:
                module_quizzes.append(url_buffer)
        if self.action == "Upload quiz":
            for quiz in module_quizzes:
                self.logger.info(f"quiz_url: {quiz}")
                print(f"quiz_url: {quiz}")
                self.driver.get(quiz)
                element = WebDriverWait(driver=self.driver, timeout=20).until(
                    ec.presence_of_element_located((By.CSS_SELECTOR, "#action-menu-2-menubar")))
                edit_url = self.driver.find_element(By.XPATH, "//a[contains(@href,'/quiz/edit.php')]").get_attribute(
                    "href")
                self.driver.get(edit_url)
                element = WebDriverWait(driver=self.driver, timeout=20).until(
                    ec.presence_of_element_located((By.CSS_SELECTOR, "#page-1")))
                if self.level == "1":
                    self.get_quiz_to_edit_level_1()
                else:
                    self.get_quiz_to_edit_level_2_3()
        else:
            for video in module_lessons:
                self.edit_video(video)

    def get_video_url(self, language):
        if language == "ITA":
            try:
                edit_v_url = WebDriverWait(driver=self.driver, timeout=3).until(
                    ec.presence_of_element_located(
                        (By.XPATH, "//a[contains(@title, 'Aggiorna pagina: Lezione video')]"))).get_attribute(
                    "href")
            except sexp.TimeoutException:
                try:
                    edit_v_url = WebDriverWait(driver=self.driver, timeout=1).until(
                        ec.presence_of_element_located(
                            (By.XPATH, "//a[contains(@title, 'Aggiorna pagina: video')]"))).get_attribute(
                        "href")
                except sexp.TimeoutException:
                    edit_v_url = WebDriverWait(driver=self.driver, timeout=1).until(
                        ec.presence_of_element_located(
                            (By.XPATH, "//a[contains(@title, 'Aggiorna pagina: Video')]"))).get_attribute(
                        "href")
        else:
            try:
                edit_v_url = WebDriverWait(driver=self.driver, timeout=3).until(
                    ec.presence_of_element_located(
                        (By.XPATH, "//a[contains(@title, 'Update page: Video lesson')]"))).get_attribute(
                    "href")
            except sexp.TimeoutException:
                try:
                    edit_v_url = WebDriverWait(driver=self.driver, timeout=1).until(
                        ec.presence_of_element_located(
                            (By.XPATH, "//a[contains(@title, 'Update page: Video')]"))).get_attribute(
                        "href")
                except sexp.TimeoutException:
                    edit_v_url = WebDriverWait(driver=self.driver, timeout=1).until(
                        ec.presence_of_element_located(
                            (By.XPATH, "//a[contains(@title, 'Update page: video')]"))).get_attribute(
                        "href")
        return edit_v_url

    def edit_video(self, video_url):
        self.logger.info(f"video_url: {video_url}")
        print(f"video_url: {video_url}")
        self.driver.get(video_url)
        element = WebDriverWait(driver=self.driver, timeout=20).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, "#action-menu-2-menubar")))
        edit_urls = self.driver.find_elements(By.XPATH, "//a[contains(@href,'/lesson/edit.php')]")
        self.driver.get(edit_urls[1].get_attribute("href"))
        title = self.driver.find_element(By.XPATH, "//h2").text
        lesson_id = "L" + title.split(" ")[3]
        if title.split(" ")[2] == "Lezione":
            edit_v_url = self.get_video_url("ITA")
        else:
            edit_v_url = self.get_video_url("ENG")
        self.driver.get(edit_v_url)
        element = WebDriverWait(driver=self.driver, timeout=20).until(
            ec.visibility_of_element_located((By.XPATH, "//button[contains(@id, 'yui_')]")))

        for test in self.questions_answers_to_upload:
            if test[0] == lesson_id:
                self.custom_time_waster()
                question_textarea = self.driver.find_element(By.ID, "id_contents_editoreditable")

                self.driver.execute_script("arguments[0].innerHTML = arguments[1];", question_textarea, test[1])
                self.driver.execute_script("arguments[0].focus()", question_textarea)
                self.custom_time_waster(0.8)
                self.driver.find_element(By.ID, "id_submitbutton").click()
                if title.split(" ")[2] == "Lezione":
                    edit_v_url = self.get_video_url("ITA")
                else:
                    edit_v_url = self.get_video_url("ENG")
                if not self.check_if_element_modified(edit_v_url, test):
                    self.logger.info("Video modiefied with success")
                    print("Video modiefied with success")
                break

    def get_quiz_to_edit_level_2_3(self):
        edit_elements = self.driver.find_elements(By.XPATH, "//a[contains(text(), '(See questions)')]")
        if not edit_elements:
            edit_elements = self.driver.find_elements(By.XPATH, "//a[contains(text(), '(Visualizza domande)')]")

        self.driver.get(edit_elements[0].get_attribute("href"))
        element = self.wait_for_element_css(20, "#categoryquestions")

        # //table[@id='categoryquestions']//div[@class='dropdown']//span[contains(text(), 'Modifica domanda')]/..
        question_elements = self.driver.find_elements(By.XPATH,
                                                      "//table[@id='categoryquestions']//div[@class='dropdown']//"
                                                      "span[contains(text(), 'Edit question')]/..")
        if not question_elements:
            question_elements = self.driver.find_elements(By.XPATH,
                                                          "//table[@id='categoryquestions']//div[@class='dropdown']//"
                                                          "span[contains(text(), 'Modifica domanda')]/..")
        question_urls = []
        for el in question_elements:
            question_urls.append(el.get_attribute("href"))
        self.upload_quiz(question_urls)

    def get_quiz_to_edit_level_1(self):
        question_elements = self.driver.find_elements(By.XPATH, f"//a[contains(@title, '{str(self.idElement)}')]")
        question_urls = []
        for el in question_elements:
            question_urls.append(el.get_attribute("href"))
        self.upload_quiz(question_urls)

    def make_textarea_visable(self):
        self.driver.execute_script('document.getElementById("id_questiontext").removeAttribute("hidden")')
        self.driver.execute_script('document.getElementById("id_questiontext").removeAttribute("style")')
        self.driver.execute_script('document.getElementById("id_answer_0").removeAttribute("hidden")')
        self.driver.execute_script('document.getElementById("id_answer_0").removeAttribute("style")')
        self.driver.execute_script('document.getElementById("id_answer_1").removeAttribute("hidden")')
        self.driver.execute_script('document.getElementById("id_answer_1").removeAttribute("style")')
        self.driver.execute_script('document.getElementById("id_answer_2").removeAttribute("hidden")')
        self.driver.execute_script('document.getElementById("id_answer_2").removeAttribute("style")')

    def upload_quiz(self, question_urls):
        for el_url in question_urls:
            self.driver.get(el_url)
            element = WebDriverWait(driver=self.driver, timeout=20).until(
                ec.presence_of_element_located((By.CSS_SELECTOR, "#id_generalheader")))
            for test in self.questions_answers_to_upload:
                quiz_id = self.driver.find_element(By.ID, "id_name").get_attribute('value')
                if test[0] == quiz_id or (test[0][:4]+test[0][5:]) == quiz_id:
                    if (test[0][:4]+test[0][5:]) == quiz_id:
                        self.driver.find_element(By.ID, "id_name").clear()
                        self.driver.find_element(By.ID, "id_name").send_keys(test[0])
                    self.custom_time_waster(2)
                    retry_attempts = 0
                    while retry_attempts < 3:
                        retry_attempts += 1
                        element = WebDriverWait(driver=self.driver, timeout=20).until(
                            ec.visibility_of_element_located((By.XPATH, "//button[contains(@id, 'yui_')]")))
                        self.make_textarea_visable()
                        question_textarea = self.driver.find_element(By.ID, "id_questiontexteditable")
                        question_real_textarea = self.driver.find_element(By.ID, "id_questiontext")
                        question_real_textarea.send_keys(test[1])

                        answer0_textarea = self.driver.find_element(By.ID, "id_answer_0editable")
                        question_real_answer0_textarea = self.driver.find_element(By.ID, "id_answer_0")
                        question_real_answer0_textarea.send_keys(test[2])

                        answer1_textarea = self.driver.find_element(By.ID, "id_answer_1editable")
                        question_real_answer1_textarea = self.driver.find_element(By.ID, "id_answer_1")
                        question_real_answer1_textarea.send_keys(test[3])

                        answer2_textarea = self.driver.find_element(By.ID, "id_answer_2editable")
                        question_real_answer2_textarea = self.driver.find_element(By.ID, "id_answer_2")
                        question_real_answer2_textarea.send_keys(test[4])

                        self.driver.execute_script("arguments[0].focus()", question_textarea)
                        self.driver.execute_script("arguments[0].innerHTML = arguments[1];", question_textarea, test[1])
                        self.driver.execute_script("arguments[0].focus()", question_textarea)
                        self.custom_time_waster(0.1)
                        self.driver.execute_script("arguments[0].focus()", answer0_textarea)
                        self.driver.execute_script('arguments[0].innerHTML = arguments[1];', answer0_textarea, test[2])
                        self.driver.execute_script("arguments[0].focus()", answer0_textarea)
                        self.custom_time_waster(0.1)
                        self.driver.execute_script("arguments[0].focus()", answer1_textarea)
                        self.driver.execute_script('arguments[0].innerHTML = arguments[1];', answer1_textarea, test[3])
                        self.driver.execute_script("arguments[0].focus()", answer1_textarea)
                        self.custom_time_waster(0.1)
                        self.driver.execute_script("arguments[0].focus()", answer2_textarea)
                        self.driver.execute_script('arguments[0].innerHTML = arguments[1];', answer2_textarea, test[4])
                        self.driver.execute_script("arguments[0].focus()", answer2_textarea)
                        self.custom_time_waster(0.1)

                        self.modified_quiz_count += 1

                        self.driver.find_element(By.ID, "id_submitbutton").click()
                        if self.level == "1":
                            element = WebDriverWait(driver=self.driver, timeout=20).until(
                                ec.presence_of_element_located((By.CSS_SELECTOR, "#page-1")))
                        else:
                            element = WebDriverWait(driver=self.driver, timeout=20).until(
                                ec.presence_of_element_located((By.CSS_SELECTOR, "#maincontent")))
                        self.logger.debug(f"saved modified quiz: {test[0]}")
                        # sys.exit()
                        # driver.find_element(By.ID, "id_cancel").click()
                        # ============================================= CHECK IF UPLOAD IS CORRECT ====================
                        if not self.check_if_element_modified(el_url, test): # returns false if no missmatch was found, so string are correct
                            self.logger.info(f"{test[0]} was modified with success")
                            print(f"{test[0]} was modified with success")
                            break
                        else:
                            self.logger.info(f"{test[0]} retry attempts {retry_attempts}/3")
                            print(f"{test[0]} retry attempts {retry_attempts}/3")
                            if retry_attempts == 3:
                                self.logger.warning(f"ALL ATTEMPTS FAILED FOR {test[0]} - skipping")
                                print(f"ALL ATTEMPTS FAILED FOR {test[0]} - skipping")
                        if self.modified_quiz_count == len(self.questions_answers_to_upload):
                            print("Modified all quizzes present in file, closing...")
                            self.driver.quit()
                            break
                    break

    def check_if_element_modified(self, url, QandA):
        missmatch = False
        self.driver.get(url)
        if not self.action == "Upload video":
            element = WebDriverWait(driver=self.driver, timeout=20).until(
                ec.presence_of_element_located((By.CSS_SELECTOR, "#id_generalheader")))
            question_textarea = re.sub('[^A-Za-z0-9\"\'<>=]+', '',
                                       self.driver.find_element(By.ID, "id_questiontexteditable").get_attribute(
                                           'innerHTML').replace("&nbsp;", " ").replace("&amp;", "&"))
            answer0_textarea = re.sub('[^A-Za-z0-9\"\'<>=]+', '',
                                      self.driver.find_element(By.ID, "id_answer_0editable").get_attribute(
                                          'innerHTML').replace(
                                          "&nbsp;", " ").replace("&amp;", "&"))
            answer1_textarea = re.sub('[^A-Za-z0-9\"\'<>=]+', '',
                                      self.driver.find_element(By.ID, "id_answer_1editable").get_attribute(
                                          'innerHTML').replace(
                                          "&nbsp;", " ").replace("&amp;", "&"))
            answer2_textarea = re.sub('[^A-Za-z0-9\"\'<>=]+', '',
                                      self.driver.find_element(By.ID, "id_answer_2editable").get_attribute(
                                          'innerHTML').replace(
                                          "&nbsp;", " ").replace("&amp;", "&"))
            q = re.sub('[^A-Za-z0-9\"\'<>=]+', '', QandA[1])
            a1 = re.sub('[^A-Za-z0-9\"\'<>=]+', '', QandA[2])
            a2 = re.sub('[^A-Za-z0-9\"\'<>=]+', '', QandA[3])
            a3 = re.sub('[^A-Za-z0-9\"\'<>=]+', '', QandA[4])
            if q != question_textarea:
                missmatch = True
                print(f"element: {QandA[0]}, wrong question")
            if a1 != answer0_textarea:
                missmatch = True
                print(f"element: {QandA[0]}, wrong answer 1")
            if a2 != answer1_textarea:
                missmatch = True
                print(f"element: {QandA[0]}, wrong answer 2")
            if a3 != answer2_textarea:
                missmatch = True
                print(f"element: {QandA[0]}, wrong answer 3")
        else:
            element = self.wait_for_element_xpath(20, "//button[contains(@id, 'yui_')]")
            video_textarea = re.sub('[^A-Za-z0-9\"\'<>=]+', '',
                                    self.driver.find_element(By.ID, "id_contents_editoreditable").get_attribute(
                                        'innerHTML').replace("&nbsp;", " "))
            v = re.sub('[^A-Za-z0-9\"\'<>=]+', '', QandA[1])
            if v != video_textarea:
                missmatch = True
                print(f"element: {QandA[0]}, wrong string")
        if missmatch:
            self.logger.warning(f"element: {QandA[0]}, wrong string")
        return missmatch

    def get_trophy_url_overview_page(self):
        try:
            trophy_url = self.driver.find_element(By.XPATH, "//span[contains(text(), '" +
                                                  self.trophy_string[int(self.idElement.replace("C", "")) % 4]
                                                  [0] + "')]/../../a").get_attribute("href")
        except sexp.NoSuchElementException:
            trophy_url = self.driver.find_element(By.XPATH, "//span[contains(text(), '" +
                                                  self.trophy_string[int(self.idElement.replace("C", "")) % 4]
                                                  [1] + "')]/../../a").get_attribute("href")
            # ============================================================================ QUIZ PAGE ======
        print(f"trophy_url: {trophy_url}")
        self.logger.info(f"trophy_url: {trophy_url}")
        self.driver.get(trophy_url)
        element = WebDriverWait(driver=self.driver, timeout=20).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, "#action-menu-2-menubar")))
        edit_url = self.driver.find_element(By.XPATH, "//a[contains(@href,'/quiz/edit.php')]").get_attribute("href")
        self.driver.get(edit_url)
        element = WebDriverWait(driver=self.driver, timeout=20).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, "#page-1")))
        if self.level == "1":
            self.get_quiz_to_edit_level_1()
        else:
            self.get_quiz_to_edit_level_2_3()

    def get_element_strings(self):
        starting_column = -1
        # when making an exe remember to add ../ before xlsx file
        not_read = True
        while not_read:
            try:
                if self.idElement.startswith('C'):
                    df = pd.read_excel(f"{self.Path}{my_variables.excel_path}StringheQuizLite.xlsx", sheet_name="quiz coppe",
                                       header=None)
                    self.logger.info("Opening excel file trophy sheet")
                else:
                    df = pd.read_excel(f"{self.Path}{my_variables.excel_path}StringheQuizLite.xlsx", header=None)
                    self.logger.info("Opening excel file quiz sheet")
                not_read = False
            except PermissionError:
                answer = input("File Stringhequizlite.xlsx is open, please close - Continue (Y/n)")
                if answer.upper() != "Y":
                    sys.exit("Closing uploadbot. Bye!!")
        rows = list(df.values.tolist())
        for j, h in enumerate(rows[0]):
            if h == "ID":
                starting_column = j
        isFirstRow = True
        if starting_column != -1:
            for r in rows:
                if isFirstRow:
                    isFirstRow = False
                    continue
                if r[0].split("#", 1)[0] == self.idElement:
                    self.questions_answers_to_upload.append(
                        [r[starting_column], r[starting_column + 1], r[starting_column + 2], r[starting_column + 3],
                         r[starting_column + 4]])
        else:
            self.logger.error("Impossible to read excel file")
            print("Errore nella lettura del file excel... closing...")
            sys.exit()
        if not self.questions_answers_to_upload:
            self.logger.error(f"No corresponding ID={self.idElement} found")
            print("No trophy found...closing...")
            sys.exit()
        return

    def trophy_number_to_string(self):
        idNum = int(self.idElement.replace("C", ""))
        if idNum > 4:
            idNum = idNum % 4
        match idNum:
            case 1:
                self.trophy_string[1] = ["First", "Prima"]
            case 2:
                self.trophy_string[2] = ["Second", "Seconda"]
            case 3:
                self.trophy_string[3] = ["Third", "Terza"]
            case 4 | 0:
                self.trophy_string[4] = ["Fourth", "Quarta"]
                self.trophy_string[0] = ["Fourth", "Quarta"]
        return

    def get_video_strings(self):
        starting_column = -1
        not_read = True
        while not_read:
            try:
                if self.isInternational:
                    df = pd.read_excel(f"{self.Path}{my_variables.excel_path}StringheQuizLite.xlsx",
                                       sheet_name="video international",
                                       header=None)
                else:
                    df = pd.read_excel(f"{self.Path}{my_variables.excel_path}StringheQuizLite.xlsx",
                                       sheet_name="video awareness",
                                       header=None)
                not_read = False
            except PermissionError:
                answer = input("File Stringhequizlite.xlsx is open, please close - Continue (Y/n)")
                if answer.upper() != "Y":
                    sys.exit("Closing uploadbot. Bye!!")
        rows = list(df.values.tolist())
        for j, h in enumerate(rows[0]):
            if h == "Codice HTML video":
                starting_column = j
        isFirstRow = True
        if starting_column != -1:
            for r in rows:
                if isFirstRow:
                    isFirstRow = False
                    continue
                if r[0] == self.idElement:
                    self.questions_answers_to_upload.append([r[1], r[starting_column]])
        else:
            self.logger.error("Impossible to read excel file")
            print("Errore nella lettura del file excel... closing...")
            sys.exit()
        if not self.questions_answers_to_upload:
            self.logger.error(f"No corresponding ID={self.idElement} found")
            print("No video found...closing...")
            sys.exit()
        return

    # WAITERS
    def custom_time_waster(self, time_value=my_variables.edit_page_wait):
        try:
            element = self.wait_for_element_xpath(time_value, "//button[contains(@id, 'non_existant_id')]")
        except sexp.TimeoutException:
            return 0

    def wait_for_element_xpath(self, timeout_value, xpath):
        return WebDriverWait(driver=self.driver, timeout=timeout_value).until(
            ec.presence_of_element_located((By.XPATH, xpath)))

    def wait_for_element_css(self, timeout_value, css_selector):
        return WebDriverWait(driver=self.driver, timeout=timeout_value).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
