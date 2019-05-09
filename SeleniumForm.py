from selenium import webdriver
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup
import re

#Input courseID
courseIn = input("Enter course ID without space: ")
courseIn = re.match("(.*)(\d\d\d\d)", courseIn)
courseID = courseIn.groups()[0] + "*" + courseIn.groups()[1]

driver = '/Users/Ben/Drive/Files/GithubProjects/ScheduleMaker/env/bin/geckodriver'

term = '2019/FA'
level = 'UG'
subject = courseID.split("*")[0]
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
with open("page.html", "w") as f:
    f.write(browser.page_source)

soup = BeautifulSoup(browser.page_source, 'html.parser')

table = soup.find('table', id='course-list')
#print(table.prettify())

headings = table.find('thead').find_all('th')

# Find what index the CourseID is under
for i in range(len(headings)-1):
	if 'ID' in headings[i]:
		indID = i
	elif 'Course' in headings[i]:
		indCourse = i
	elif 'Section' in headings[i]:
		indSection = i
	elif 'Title' in headings[i]:
		indTitle = i
	elif 'Instructor' in headings[i]:
		indInstructor = i
	elif 'Days' in headings[i]:
		indDays = i
	elif 'Times' in headings[i]:
		indTimes = i
	elif 'Room' in headings[i]:
		indRoom = i

# Get all rows
rows = table.find('tbody').find_all('tr')
#print('\n')
#print(rows)

# Find the row containing the course specified
print('Finding times:')
# Not prepared for a course offered twice
for i in range(len(rows)-1):
	if courseID in rows[i].get_text():
		cols = rows[i].find_all('td')

		# Print first time slot
		print('Class\t', end='')
		print(cols[indDays].get_text() + '\t', end='')
		print(cols[indTimes].get_text() + '\t')

		# Print following time slots
		# Do while the current line has a time slot within it:
		j=i
		checkNext = True
		while checkNext:

			checkNext = False
			secCols = rows[j+1].find_all('td')
			for col in secCols:
				# If the row contains a time slot then read the row
				check = re.search('\d\d:\d\d..-\d\d:\d\d..', col.get_text())
				if check:
					# This row should be printed
					checkNext = True

					# Indices are consistent in secondary rows
					print(secCols[0].get_text() + '\t', end='')
					print(secCols[2].get_text() + '\t', end='')
					print(secCols[3].get_text())
			j = j + 1




browser.quit()