from selenium import webdriver

driver = webdriver.Chrome()
driver.get('http://localhost:8000')

try:
    assert 'Voice' in driver.title

finally:
    driver.quit()


# test user_type functionality
# user vs request.user i.e. visiting another users detail page as a mentor or candidate
# that pages have the right items according to the spec
