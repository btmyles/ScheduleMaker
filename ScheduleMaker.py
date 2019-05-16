from selenium import webdriver
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup
import re

#Functions

def remove_html_tags(string):
	return re.sub(r'<[^<]+?>', '', string)

# Place asterisk in course name and convert to upper
def prep_course(course):
	g = re.match(r"(\D+)(\d+)", course, re.IGNORECASE)
	ret = g.groups()[0].upper() + "*" + g.groups()[1]
	return ret

# get the schedule for a course
def get_schedule(term, lvl, course, loc):

	# Get website parameters
	term = '2019/FA'
	level = 'UG'
	subject = course.split("*")[0]
	location = 'FR'

	#Setup browser
	driver = './env/bin/geckodriver'
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
	#with open("page.html", "w") as f:
	#   f.write(source)

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
		if coursefound and course in rows[i].get_text():
			courseduplicate = True

		elif course in rows[i].get_text() and not coursefound:

			print('\nFinding times for ' + course + ':')

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
				if re.search(r'\d\d:\d\d..-\d\d:\d\d..', rows[j+1].get_text()) and not course in rows[j+1].get_text():
					# This row should be printed and the next should be checked
					checkNext = True

					# Column indices
					secCols = rows[j+1].find_all('td')

					# Place days and times into lists
					secdays = str(secCols[2]).split("<br/>")
					sectimes = str(secCols[3]).split("<br/>")

					# remove html tags
					for index in range(len(secdays)):
						secdays[index] = remove_html_tags(secdays[index])
					for index in range(len(sectimes)):
						sectimes[index] = remove_html_tags(sectimes[index])

					# Place days and times in list
					sessions = []
					for index in range(len(secdays)):
						sessions.append([secCols[0].get_text(), secdays[index], sectimes[index]])

					for session in sessions:
						print(session[0] + '\t', end='')
						print(session[1] + '\t', end='')
						print(session[2])

				j = j + 1

	if courseduplicate:
		print("This course is a duplicate")


#Input courseID
input_line = input("Enter course IDs: ")
# Separate input by each course
courses = input_line.split()

# Place asterisk betweene each course
for index in range(len(courses)):
	courses[index] = prep_course(courses[index])

# Testing loop 
for course in courses:
	get_schedule('','', course, '')