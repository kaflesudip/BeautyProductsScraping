from selenium import webdriver
# from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox()
driver.get("http://www.beautybay.com/cosmetics/_/N-23Z1xZ1wZ1vZ1uZ1tZo/")
# assert "Python" in driver.title
# elem = driver.find_element_by_name("q")
# elem.send_keys("pycon")
# elem.send_keys(Keys.RETURN)
print (driver.page_source)
# assert "No results found." not in driver.page_source
# driver.close()
