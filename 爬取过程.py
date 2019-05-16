
# 打印网页源码

from bs4 import BeautifulSoup
from selenium import webdriver

urls = ('https://www.icourse163.org/category/computer')


driver = webdriver.Chrome()

driver.maximize_window()

driver.get(urls)
data = driver.page_source
soup = BeautifulSoup(data, 'lxml')
print(soup)



