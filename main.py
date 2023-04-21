# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os
import csv
import sys

import my_variables
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


# ============================================================================================ FUNCTIONS ========
def getModuleStrings(module, Path):

    return

# ============================================================================================ GLOBAL VARIABLES ========
options = Options()
# options.add_argument('--headless') #Hide GUI
options.add_argument("--windows-size=1920, 1080")
options.add_argument("start-maximized")
options.add_experimental_option("prefs", {"profile.managed_default_content_setting.images": 2})
rawPath = os.getcwd()
Path = rawPath.replace("\\", "/") + "/"


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    modified_quiz_count = 0
    # ====================================================================================================== MENU ======
    print("0) Dev\n1) Enterprise\n2) Enterprise-ww\n3) Pirelli\n4) awareness\n5) international")
    choice = int(input("\nChoose an instance: "))
    print("\n")
    questions_answers_to_upload = []
    instance = ""
    match choice:
        case 0:
            instance = "dev.enterprise.cyberguru.it"
        case 1:
            instance = "enterprise.cyberguru.it"
        case 2:
            instance = "enterprise-ww.cyberguru.it"
        case 3:
            instance = "pirelli.cyberguru.it"
        case 4:
            instance = "awareness.cyberguru.it"
        case 5:
            instance = "international.cyberguru.it"
        case _:
            print("No instance selected....Closing application")
    if instance:
        rawPath = os.getcwd()
        Path = rawPath.replace("\\", "/") + "/"
        filelist = os.listdir(Path)
        for i in filelist:
            if i.endswith(".csv"):
                with open(Path + i, encoding="utf8", mode='r') as f:
                    reader = csv.reader(f, delimiter=';')
                    isFirstRow = True
                    for row in reader:
                        if isFirstRow:
                            isFirstRow = False
                            continue
                        questions_answers_to_upload.append(row)
                    f.close()

        module_number = questions_answers_to_upload[0][0].split("Q", 1)[0]


        # ================================================================================================= LOGIN ======
        driver = webdriver.Chrome(options=options)
        url = "https://" + instance
        driver.get(url)
        element = WebDriverWait(driver=driver, timeout=20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#username")))

        email = driver.find_element(By.ID, "username")
        password = driver.find_element(By.ID, "password")

        email.send_keys(my_variables.MY_USERNAME)
        password.send_keys(my_variables.MY_PASSWORD)

        driver.find_element(By.ID, "loginbtn").click()
        # ============================================================================================== HOMEPAGE ======
        element = WebDriverWait(driver=driver, timeout=20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#region-main-box")))

        levels_buttons = driver.find_elements(By.XPATH, "//ul[@id='livelli']//li//div[@class='text-center']//a")
        lvlOne_url = levels_buttons[0].get_attribute("href")
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
                        driver.implicitly_wait(2)
                        question_textarea = driver.find_element(By.ID, "id_questiontexteditable")
                        answer0_textarea = driver.find_element(By.ID, "id_answer_0editable")
                        answer1_textarea = driver.find_element(By.ID, "id_answer_1editable")
                        answer2_textarea = driver.find_element(By.ID, "id_answer_2editable")

                        driver.execute_script("arguments[0].innerHTML = arguments[1];", question_textarea, test[1])
                        driver.execute_script("arguments[0].focus()", question_textarea)
                        driver.implicitly_wait(0.2)
                        driver.execute_script('arguments[0].innerHTML = arguments[1];', answer0_textarea, test[2])
                        driver.execute_script("arguments[0].focus()", answer0_textarea)
                        driver.implicitly_wait(0.2)
                        driver.execute_script('arguments[0].innerHTML = arguments[1];', answer1_textarea, test[3])
                        driver.execute_script("arguments[0].focus()", answer1_textarea)
                        driver.implicitly_wait(0.2)
                        driver.execute_script('arguments[0].innerHTML = arguments[1];', answer2_textarea, test[4])
                        driver.execute_script("arguments[0].focus()", answer2_textarea)
                        driver.implicitly_wait(0.2)
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
                        break
        print("finished editing " + module_number + " on instance " + instance)
        driver.quit()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
