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
	'binds[:ge]': 'AnyGE',
	'binds[:crse_units_op]': '=',
	'binds[:crse_units_from]': '',
	'binds[:crse_units_to]': '',
	'binds[:crse_units_exact]': '',
	'binds[:days]': '',
	'binds[:times]': '',
	'binds[:acad_career]': '',
	'rec_dur': 346
}

def main():

	class_list = scrape(2192)

# Returns json of all classes and class information
def scrape(term):

	pp = pprint.PrettyPrinter(indent=4)

	request = requests.post(CLASS_API_ENDPOINT, data=payload)

	class_list = BeautifulSoup(request.text, 'html.parser')
	classes = class_list.find_all(id=re.compile('class_nbr'))

	class_info_list = {}

	for class_element in classes:

		class_info = {
			'title': None,
			'ge': None,
			'description': None,
			'instructors': None,
			'link': None
		}

		request2 = requests.get(class_element['href'])
		class_page = BeautifulSoup(request2.text, 'html.parser')

		class_info['link'] = class_element['href']

		# Class title
		class_title = class_page.find('h2')

		if class_title:

			print('*****', class_title.get_text().strip(), '*****')
			class_info['title'] = class_title.get_text().strip().replace('\u00a0\u00a0', '')

		# GE
		details = class_page.find_all('dd')

		if details:

			class_info['ge'] = details[5].get_text().strip()

		# Description
		description = parse_panel(class_page, 'Description')

		if description:

			class_info['description'] = description.get_text().strip()

		# Instructor
		meeting_info = parse_list(class_page, 'Meeting Information', 'td')
		
		if meeting_info:

			class_info['instructors'] = meeting_info[2]

		class_info_list[class_info['title']] = class_info

	#pp.pprint(class_info_list)
	with open('classes.json', 'w') as fp:
		json.dump(class_info_list, fp, sort_keys=True)

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