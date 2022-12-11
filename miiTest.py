import time
import string
from random import randint
from random import random
from random import choice
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

def main():
    letters = string.ascii_lowercase
    mail = ''.join(choice(letters) for i in range(5)) + '@xyz.pl'
    print(mail)
    url = "https://www.gryfsklep.pl/index.php"
    options = Options()
    options.binary_location = r"C:/Program Files/Mozilla Firefox/firefox.exe"
    firefox_driver_path = 'geckodriver.exe'
    driver = webdriver.Firefox(options=options, executable_path=firefox_driver_path)
    driver.get(url)
    time.sleep(1)
    #dodawanie produktów do koszyka
    for i in range(10):
        driver.find_element(By.CLASS_NAME, 'all-product-link').click()
        time.sleep(1)
        elements = driver.find_elements(By.CLASS_NAME,'subcategory-image')
        elements[randint(0,len(elements)-1)].click()
        elements = driver.find_elements(By.CLASS_NAME, 'thumbnail-top')
        elements[randint(0,len(elements)-1)].find_element(By.CLASS_NAME,'highlighted-informations').click()
        time.sleep(1)
        if len(driver.find_elements(By.CLASS_NAME,'input-color')) != 0:
            elements = driver.find_elements(By.CLASS_NAME, 'input-color')
            elements[randint(0,len(elements)-1)].click()
            time.sleep(1)
            
        if len(driver.find_elements(By.CLASS_NAME,'form-control-select')) != 0:
            elements = driver.find_element(By.CLASS_NAME, 'form-control-select')
            select = Select(elements)
            select.select_by_index(randint(0,2))
            time.sleep(1)
        
        if len(driver.find_elements(By.CLASS_NAME,'product-message')) != 0:
            driver.find_element(By.CLASS_NAME, 'product-message').send_keys('xx')
            driver.find_element(By.CLASS_NAME, 'card').find_element(By.TAG_NAME, 'button').click()
            time.sleep(1)

        driver.find_element(By.NAME,'qty').send_keys(Keys.DELETE)
        driver.find_element(By.NAME,'qty').send_keys(randint(1,10))
        driver.find_element(By.CLASS_NAME, 'add-to-cart').click()
        time.sleep(4)
        driver.find_element(By.XPATH,"//*[contains(text(), 'Kontynuuj')]").click()
        time.sleep(1)
        driver.find_element(By.CLASS_NAME, 'logo').click()
        time.sleep(1)

    #usuwanie pozycji z koszyka 
    driver.find_element(By.CLASS_NAME,'cart-preview').click()
    elements = driver.find_elements(By.CLASS_NAME, 'remove-from-cart')
    elements[randint(0,len(elements)-1)].click()
    time.sleep(4)
    driver.find_element(By.CLASS_NAME,'checkout').find_element(By.TAG_NAME,'a').click()
    

    #dane zamawiajacego
    form = driver.find_element(By.CLASS_NAME,'js-customer-form')
    gender = form.find_elements(By.CLASS_NAME,'custom-radio')
    gender[randint(0,len(gender)-1)].click()
    form.find_element(By.ID,'field-firstname').send_keys('Grzegorz')
    form.find_element(By.ID,'field-lastname').send_keys('Brzęczyszczykiewicz')
    form.find_element(By.ID,'field-email').send_keys(mail)
    form.find_element(By.ID,'field-password').send_keys('password123')
    form.find_element(By.ID,'field-birthday').send_keys('1970-06-12')
    form.find_element(By.NAME,'customer_privacy').click()
    form.find_element(By.NAME,'psgdpr').click()
    form.find_element(By.NAME,'continue').click()

    time.sleep(1)

    #Dane adresowe
    driver.find_element(By.ID,'field-address1').send_keys('ciastko1')
    driver.find_element(By.ID,'field-postcode').send_keys('21-370')
    driver.find_element(By.ID,'field-city').send_keys('Chrząszczyżewoszyce')
    driver.find_element(By.NAME,'confirm-addresses').click()
    time.sleep(1)

    #opcja dostawy
    driver.find_element(By.NAME,'confirmDeliveryOption').click()
    time.sleep(1)

    #opcja platnosci
    driver.find_element(By.ID,'payment-option-2-container').find_element(By.TAG_NAME,'input').click()
    driver.find_element(By.ID,'conditions_to_approve[terms-and-conditions]').click()
    driver.find_element(By.ID,'payment-confirmation').find_element(By.TAG_NAME,'button').click()
    time.sleep(1)

    #sprawdzanie statusu zamowienia
    driver.find_element(By.CLASS_NAME,'user-info').find_element(By.TAG_NAME,'span').click()
    driver.find_element(By.ID,'history-link').find_element(By.TAG_NAME,'span').click()
    time.sleep(1)
    driver.find_element(By.XPATH,"//*[contains(text(), 'Szczegóły')]").click()
    time.sleep(20)
    #driver.close()

if __name__ == "__main__":
    main()