from bs4 import BeautifulSoup
import re
import requests
import json
import pprint

CLASS_API_ENDPOINT = 'https://pisa.ucsc.edu/class_search/'

payload = {
	'action': 'results',
	'binds[:term]': '2192',
	'binds[:reg_status]': 'all',
	'binds[:subject]': '',
	'binds[:catalog_nbr_op]': '=', 
	'binds[:catalog_nbr]': '',
	'binds[:title]': '',
	'binds[:instr_name_op]': '=',
	'binds[:instructor]': '',
	'binds[:ge]': '',
	'binds[:crse_units_op]': '=',
	'binds[:crse_units_from]': '',
	'binds[:crse_units_to]': '',
	'binds[:crse_units_exact]': '',
	'binds[:days]': '',
	'binds[:times]': '',
	'binds[:acad_career]': '',
	'rec_dur': 5
}

def main():

	class_list = scrape(2192)

# Returns json of all classes and class information
def scrape(term):

	pp = pprint.PrettyPrinter(indent=4)

	request = requests.post(CLASS_API_ENDPOINT, data=payload)

	class_list = BeautifulSoup(request.text, 'html.parser')
	classes = class_list.find_all(id=re.compile('class_nbr'))

	class_info_list = {
		'classes': {}
	}

	for class_element in classes:

		class_info = {
			'details': {},
			'meeting_info': {}
		}

		request2 = requests.get(class_element['href'])
		class_page = BeautifulSoup(request2.text, 'html.parser')

		class_title = class_page.find('h2')
		if class_title:
			print('\n*****', class_title.get_text().strip(), '*****\n')

		# Class details
		details_categories = ['career', 'grading', 'class_number', 'type', 'credits', 'general_education', 'status', 'available_seats', 'enrollment_capacity', 'enrolled', 'waitlist_capacity', 'waitlist_total']
		details = class_page.find_all('dd')
		detail_list = []
		if details:
			for detail in details:
				detail_list.append(detail.get_text().strip())
			for i in range(len(details_categories)):
				class_info['details'][details_categories[i]] = detail_list[i]

		# Description
		description = parse_panel(class_page, 'Description')
		if description:
			class_info['description'] = description.get_text().strip()

		# Meeting information
		meeting_info = parse_list(class_page, 'Meeting Information', 'td')
		if meeting_info:
			meeting_info_categories = ['days_times', 'room', 'instructor', 'meeting_dates']
			for i in range(len(meeting_info)):
				class_info['meeting_info'][meeting_info_categories[i]] = meeting_info[i]

		# Class notes
		class_notes = parse_panel(class_page, 'Class Notes')
		if class_notes:
			class_info['class_notes'] = class_notes.get_text().strip()

		# Associated discussion sections or labs
		discussions = parse_list(class_page, 'Associated Discussion Sections or Labs', 'div', class_='col-xs-6 col-sm-3')
		if discussions:
			discussions_list = [discussions[i:i+7] for i in range(0, len(discussions), 7)]
			class_info['sections_labs'] = discussions_list

		# Enrollment requirements
		requirements = parse_panel(class_page, 'Enrollment Requirements')
		if requirements:
			class_info['enrollment_requirements'] = requirements.get_text().strip()

		class_info_list['classes'][class_info['details']['class_number']] = class_info

	pp.pprint(class_info_list)
	with open('result.json', 'w') as fp:
		json.dump(class_info_list, fp, sort_keys=True, indent=4, separators=(',', ': '))

# Returns list with information in order found
def parse_list(page, heading, tag, **kargs):

	panel = parse_panel(page, heading)
	if panel:
		info_list = panel.find_all(tag, **kargs)
		if info_list:
			parsed = []
			for info in info_list:
				parsed.append(info.get_text())
			return parsed

# Returns contents of panel-body associated with given heading
def parse_panel(page, heading):
	panel_heading = page.find(string=re.compile(heading))
	if panel_heading:
		return panel_heading.find_parent().find_parent().find_next_sibling()
	else:
		print(heading, 'not found')
		return None

if __name__ == '__main__':
	main()