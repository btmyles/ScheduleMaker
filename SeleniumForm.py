from selenium import webdriver
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup
import re

#Input courseID
courseID = 'ME*2111'

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
#print(table.prettify())

headings = table.find('thead').find_all('th')

# Find what index the CourseID is under
for i in range(len(headings)-1):
    print(headings[i])
    if 'ID' in headings[i]:
        indID = i
# More code needed here to improve robustness
# Add if statements similar to the 'ID' one.
indCourse = 1
indSection = 2
indTitle = 3
indInstructor = 4
indDays = 5
indTimes = 6
indRoom = 7

# Get all rows
rows = table.find('tbody').find_all('tr')

# Find the row containing the course specified
for i in range(len(rows)-1):
    if courseID in rows[i].get_text():
        print(rows[i].find_all('td')[indTimes])



browser.quit()