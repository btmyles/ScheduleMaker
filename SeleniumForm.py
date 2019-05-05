from selenium import webdriver
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup
import re

driver = '/Users/Ben/Drive/Files/GithubProjects/ScheduleMaker/env/bin/geckodriver'

term = '2019/FA'
level = 'UG'
subject = 'CS'
location = 'FR'

options = webdriver.FirefoxOptions()
options.add_argument('-headless')

browser = webdriver.Firefox(executable_path=driver, options=options)
browser.get('http://es.unb.ca/apps/timetable/')

select_term = Select(browser.find_element_by_id('term'))
select_term.select_by_value(term)

select_level = Select(browser.find_element_by_id('level'))
select_level.select_by_value(level)

select_subject = Select(browser.find_element_by_id('subject'))
select_subject.select_by_value(subject)

select_subject = Select(browser.find_element_by_id('location'))
select_subject.select_by_value(location)

submit = browser.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div/div[4]/form/input[4]')
submit.click()

#Save html to file
#with open("page.html", "w") as f:
#    f.write(browser.page_source)

soup = BeautifulSoup(browser.page_source, 'html.parser')

table = soup.find('table', id='course-list')
print(table)

#All text in table
#tabtext = table.text.strip()
#print(tabtext)

# if the row contans a section number, grab the 6th and 7th element in the row
# if the row does not, attempt to grab the 3rd and 4th. If this breaks dont worry



row = table.findAll('tr')[0]
print(row)


# Get list of all rows with the beginning of a course
# for row in table.find_all('tr'):
#     for col in row.find_all('td'):
#         if re.search('FR', col.text):
            




browser.quit()