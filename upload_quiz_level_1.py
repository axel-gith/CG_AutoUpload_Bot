import os
import sys
sys.path.insert(1, os.getcwd() + "\\venv\\Lib\\site-packages")
import re
# import my_variables
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd





# ============================================================================================ FUNCTIONS ========
def getModuleStrings(module, Path):
    starting_column = -1
    df = pd.read_excel(Path + "StringheQuizLite.xlsx", header=None)
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
            if r[0].split("Q", 1)[0] == module:
                questions_answers_to_upload.append([r[starting_column], r[starting_column + 1], r[starting_column + 2], r[starting_column + 3], r[starting_column + 4]])
    else:
        print("Errore nella lettura del file excel... closing...")
        sys.exit()
    return

def checkIfModified(driver, url, QandA):
    driver.get(url)
    element = WebDriverWait(driver=driver, timeout=20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#id_generalheader")))
    question_textarea = re.sub('[^A-Za-z0-9\"\'<>=]+', '', driver.find_element(By.ID, "id_questiontexteditable").get_attribute('innerHTML').replace("&nbsp;", " "))
    answer0_textarea = re.sub('[^A-Za-z0-9\"\'<>=]+', '', driver.find_element(By.ID, "id_answer_0editable").get_attribute('innerHTML').replace("&nbsp;", " "))
    answer1_textarea = re.sub('[^A-Za-z0-9\"\'<>=]+', '', driver.find_element(By.ID, "id_answer_1editable").get_attribute('innerHTML').replace("&nbsp;", " "))
    answer2_textarea = re.sub('[^A-Za-z0-9\"\'<>=]+', '', driver.find_element(By.ID, "id_answer_2editable").get_attribute('innerHTML').replace("&nbsp;", " "))
    q = re.sub('[^A-Za-z0-9\"\'<>=]+', '', QandA[1])
    a1 = re.sub('[^A-Za-z0-9\"\'<>=]+', '', QandA[2])
    a2 = re.sub('[^A-Za-z0-9\"\'<>=]+', '', QandA[3])
    a3 = re.sub('[^A-Za-z0-9\"\'<>=]+', '', QandA[4])
    if q != question_textarea:
        print("ERROR" + QandA[0] + "diffrent question")
    if a1 != answer0_textarea:
        print("ERROR" + QandA[0] + "diffrent answer 1")
    if a2 != answer1_textarea:
        print("ERROR" + QandA[0] + "diffrent answer 2")
    if a3 != answer2_textarea:
        print("ERROR" + QandA[0] + "diffrent answer 3")
# ============================================================================================ GLOBAL VARIABLES ========
options = Options()
# options.add_argument('--headless') #Hide GUI
options.add_argument("--windows-size=1920, 1080")
options.add_argument("start-maximized")
options.add_experimental_option("prefs", {"profile.managed_default_content_setting.images": 2})
rawPath = os.getcwd()
Path = rawPath.replace("\\", "/") + "/"
questions_answers_to_upload = []

# Press the green button in the gutter to run the script.
def uploadQuizMain(instance, MY_USERNAME, MY_PASSWORD, module_number):
    modified_quiz_count = 0
    # ====================================================================================================== MENU ======
    module_number = module_number.upper()
    getModuleStrings(module_number, Path)
    # print (questions_answers_to_upload)
    if len(questions_answers_to_upload) == 0:
        print("No module found...closing...")
        sys.exit()

    if instance:

        # ================================================================================================= LOGIN ======
        driver = webdriver.Chrome(options=options)
        url = "https://" + instance
        driver.get(url)
        element = WebDriverWait(driver=driver, timeout=20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#username")))

        email = driver.find_element(By.ID, "username")
        password = driver.find_element(By.ID, "password")

        # email.send_keys(my_variables.MY_USERNAME)
        # password.send_keys(my_variables.MY_PASSWORD)

        email.send_keys(MY_USERNAME)
        password.send_keys(MY_PASSWORD)

        driver.find_element(By.ID, "loginbtn").click()
        element = WebDriverWait(driver=driver, timeout=20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#region-main-box")))
        # ============================================================================================== HOMEPAGE ======
        try:
            levels_buttons = driver.find_elements(By.XPATH, "//ul[@id='livelli']//li//div[@class='text-center']//a")
            lvlOne_url = levels_buttons[0].get_attribute("href")
        except IndexError:
            print("Wrong username or passoword...closing ")
            sys.exit()

        lvlOne_url = lvlOne_url.split("#", 1)[0]

        driver.get(lvlOne_url)
        # =========================================================================================== MODULE PAGE ======
        element = WebDriverWait(driver=driver, timeout=20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#section-0")))

        selected_module_elements = driver.find_elements(By.XPATH, "//span[contains(text(), '" + str(module_number) + "')]/../../a")
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
        # ============================================================================================= QUIZ PAGE ======
        for quiz in module_quizzes:
            driver.get(quiz)
            element = WebDriverWait(driver=driver, timeout=20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#action-menu-2-menubar")))
            edit_url = driver.find_element(By.XPATH, "//a[contains(@href,'/quiz/edit.php')]").get_attribute("href")
            driver.get(edit_url)
            # ==================================================================================== EDIT QUIZ PAGE ======
            element = WebDriverWait(driver=driver, timeout=20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#page-1")))
            question_elements = driver.find_elements(By.XPATH, "//a[contains(@title, '"+str(module_number)+"')]")
            question_urls = []
            for el in question_elements:
                question_urls.append(el.get_attribute("href"))
            for el_url in question_urls:
                driver.get(el_url)
                element = WebDriverWait(driver=driver, timeout=20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "#id_generalheader")))
                for test in questions_answers_to_upload:
                    if test[0] == driver.find_element(By.ID, "id_name").get_attribute('value'):
                        driver.implicitly_wait(5)
                        question_textarea = driver.find_element(By.ID, "id_questiontexteditable")
                        answer0_textarea = driver.find_element(By.ID, "id_answer_0editable")
                        answer1_textarea = driver.find_element(By.ID, "id_answer_1editable")
                        answer2_textarea = driver.find_element(By.ID, "id_answer_2editable")

                        driver.execute_script("arguments[0].innerHTML = arguments[1];", question_textarea, test[1])
                        driver.execute_script("arguments[0].focus()", question_textarea)
                        driver.implicitly_wait(0.4)
                        driver.execute_script('arguments[0].innerHTML = arguments[1];', answer0_textarea, test[2])
                        driver.execute_script("arguments[0].focus()", answer0_textarea)
                        driver.implicitly_wait(0.4)
                        driver.execute_script('arguments[0].innerHTML = arguments[1];', answer1_textarea, test[3])
                        driver.execute_script("arguments[0].focus()", answer1_textarea)
                        driver.implicitly_wait(0.4)
                        driver.execute_script('arguments[0].innerHTML = arguments[1];', answer2_textarea, test[4])
                        driver.execute_script("arguments[0].focus()", answer2_textarea)
                        driver.implicitly_wait(0.4)
                        print(test[0] + " finished")

                        modified_quiz_count += 1

                        driver.find_element(By.ID, "id_submitbutton").click()
                        element = WebDriverWait(driver=driver, timeout=20).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, "#page-1")))
                        if modified_quiz_count == len(questions_answers_to_upload):
                            print("Modified all quizzes present in file, closing...")
                            driver.quit()
                            sys.exit()
                        # driver.find_element(By.ID, "id_cancel").click()
                        # ============================================= CHECK IF UPLOAD IS CORRECT =============================
                        checkIfModified(driver, el_url, test)

                        break

        print("finished editing " + module_number + " on instance " + instance)
        driver.quit()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
