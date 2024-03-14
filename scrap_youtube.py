from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

web = 'https://www.youtube.com/watch?v=lM23Y1XFd2Q'

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)


# chrome_driver_path = "C:\\Users\\dpere\\Downloads\\chromedriver-win64\\chromedriver.exe"
driver = webdriver.Chrome(options=options,service=Service(ChromeDriverManager().install()))    
# driver=webdriver.Chrome(executable_path=chrome_driver_path,options=options)
driver.get(web)

highlight = driver.find_element(By.CLASS_NAME,"highlight")

print(highlight)