from requests_html import HTMLSession
session = HTMLSession()

payload = {
	'action': 'results',
	'binds[:term]': '2190',
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
}

request = session.post('https://pisa.ucsc.edu/class_search/index.php', data=payload)

classes = request.html.find('.panel.panel-default.row');

for class_element in classes:
	class_title = class_element.find('a')
	print(class_title[0].text)