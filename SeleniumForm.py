from selenium import webdriver
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup
import re

#Functions
def remove_html_tags(string):
	return re.sub(r'<[^<]+?>', '', string)

#Input courseID
input_line = input("Enter course IDs: ")

# Separate input by each course
courses = input_line.split()

# Place asterisk betweene each course
for index in range(1):
	temp = re.match(r"(\D+)(\d+)", courses[index], re.IGNORECASE)
	courseID = temp.groups()[0].upper() + "*" + temp.groups()[1]

# Loop on this setup
k = 0

# Get website parameters
term = '2019/FA'
level = 'UG'
subject = courseID.split("*")[0]
location = 'FR'

#Setup browser
driver = '/Users/Ben/Drive/Files/GithubProjects/ScheduleMaker/env/bin/geckodriver'
options = webdriver.FirefoxOptions()
options.add_argument('-headless')
browser = webdriver.Firefox(executable_path=driver, options=options)
browser.get('http://es.unb.ca/apps/timetable/')

# Select website parameters
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

# Get page source
source = browser.page_source

#Save html to file
with open("page.html", "w") as f:
    f.write(source)

browser.quit()

# Get main table
soup = BeautifulSoup(source, 'html.parser')
table = soup.find('table', id='course-list')

# Find what index the CourseID is under
headings = table.find('thead').find_all('th')

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

# Find the row containing the course specified
coursefound = False
courseduplicate = False
for i in range(len(rows)-1):

	# if this course if offered multiple times
	if coursefound and courseID in rows[i].get_text():
		courseduplicate = True

	elif courseID in rows[i].get_text() and not coursefound:

		print('Finding times for ' + courseID + ':')

		coursefound = True
		cols = rows[i].find_all('td')

		# Place days and times into lists
		days = str(cols[indDays]).split("<br/>")
		times = str(cols[indTimes]).split("<br/>")

		# remove html tags
		for index in range(len(days)):
			days[index] = remove_html_tags(days[index])
		for index in range(len(times)):
			times[index] = remove_html_tags(times[index])

		# Place days and times in list
		sessions = []
		for index in range(len(days)):
			sessions.append([days[index], times[index]])

		# Print class time slots
		print('Lecture', end='')
		for session in sessions:
			print('\t' + session[0], end='')
			print('\t' + session[1])

		# Print following time slots
		# Do while the current line has a time slot within it:
		j=i
		checkNext = True
		while checkNext:

			checkNext = False

			# If the row contains a time slot BUT not a courseCode then read the row
			if re.search(r'\d\d:\d\d..-\d\d:\d\d..', rows[j+1].get_text()) and not courseID in rows[j+1].get_text():
				# This row should be printed and the next should be checked
				checkNext = True

				# Column indices
				secCols = rows[i+1].find_all('td')
				# Indices are consistent in secondary rows
				print(secCols[0].get_text() + '\t', end='')
				print(secCols[2].get_text() + '\t', end='')
				print(secCols[3].get_text())
			j = j + 1

if courseduplicate:
	print("This course is a duplicate")