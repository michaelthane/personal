from selenium import webdriver

browser = webdriver.Chrome()
type(browser)
browser = webdriver.Chrome()
browser.get('https://mail.google.com')

emailElem = browser.find_element_by_id('identifierId')
emailInput = input('Enter email: ')
emailElem.send_keys(emailInput)
buttonElem1 = browser.find_element_by_id('identifierNext')
buttonElem1.click()

passwordElem = browser.find_element_by_name('password')
passwordInput = input('Enter password: ')
passwordElem.send_keys(passwordInput)
buttonElem2 = browser.find_element_by_id('passwordNext')
buttonElem2.click()
