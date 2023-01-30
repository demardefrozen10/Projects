from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_courses(program, module):

    # driver = webdriver.Chrome(ChromeDriverManager().install())
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)

    url = "https://www.westerncalendar.uwo.ca/Modules.cfm"
    driver.get(url)

    courseList = []
    #program = "Computer Science"  # For testing purposes. Will have to delete later
    #module = "Honours Specialization"  # For testing purposes. Will have to delete later
    st = module + " in " + program
    st = st.upper()

    # Find the search bar and clicks on it
    search_bar = driver.find_element(
        By.CSS_SELECTOR, "input[type='search'][class='form-control input-sm']")
    search_bar.send_keys(program)

    # Click on the module
    driver.find_element(By.CLASS_NAME, "moduleDeptName").click()

    # Finds the collapse interative thing to open the lists of courses:
    driver.find_element(
        By.CSS_SELECTOR, "a[role='button'][data-toggle='collapse']").click()

    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'moduleDept')))

    # Click on the specific module on the collapse window
    dir_mod = driver.find_elements(By.XPATH, "//*[@id='collapseOne']/div/div/a")
    for s in dir_mod:
        #print(s.text)
        if s.text == st:
            s.click()
            break

    # Click on the course:
    dir_course = driver.find_elements(
        By.XPATH, "//*[@id='AdmissionRequirements']/div/span/a")
    # print(dir_course)
    for s in dir_course:
        courseList.append(s.text.strip(","))
        #print(s.text)

    dir_module = driver.find_elements(
        By.XPATH, "//*[@id='ModuleInformationDiv']/div[1]/div[9]/div/p/a")
    # print(dir_module
    for s in dir_module:
        courseList.append(s.text.strip(","))
        #print(s.text)


    # for n in courseList:
    #     print(n)
    # print(courseList)
    
    return courseList

get_courses("Computer Science", "Honours Specialization")
