from bs4 import BeautifulSoup
import re
import requests
import json
import pprint

import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

CLASS_API_ENDPOINT = 'https://pisa.ucsc.edu/class_search/'

payload = {
	'action': 'results',
	'binds[:term]': '2198',
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
	'rec_dur': 10
}

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

SPREADSHEET_ID = '1cF9wFa9xuMATQUPUqKrkoUDTywZXqhijWaEuHywIu0w'

def main():

	class_list = scrape(2198)

	sheet = getSheetsInstance()

	add_sheet_obj = {
	    'requests': [
	        {
	            'addSheet': {
	                'properties': {
	                    'title': quarter
	                }
	            }
	        }
	    ]
	}

	sheet.batchUpdate(spreadsheetId=SPREADSHEET_ID, body=add_sheet_obj).execute()

	class_list.insert(0, ['Course Title', 'Description', 'Prerequisites', 'Instructor', 'GE', 'Link'])
	class_obj = {
		'valueInputOption': 'USER_ENTERED',
		'data': [
			{
				'range': quarter + '!A:F',
				'majorDimension': 'ROWS',
				'values': class_list
			}
		],
		'includeValuesInResponse': False
	}

	sheet.values().batchUpdate(spreadsheetId=SPREADSHEET_ID, body=class_obj).execute()

# Returns tuple with scraped quarter and list of lists of each class' information
def scrape(term):	

	request = requests.post(CLASS_API_ENDPOINT, data=payload)

	class_list = BeautifulSoup(request.text, 'html.parser')
	classes = class_list.find_all(id=re.compile('class_nbr'))

	class_info_list = []

	for class_element in classes:

		class_info = []

		request2 = requests.get(class_element['href'])
		class_page = BeautifulSoup(request2.text, 'html.parser')

		# Class title / department
		class_title = class_page.find('h2')

		print('*****', class_title.get_text().strip(), '*****')
		class_info.append(class_title.get_text().strip().replace('\u00a0\u00a0', ''))

		#class_info['department'] = aliases[class_info['title'].split(' ', 1)[0]]

		# Description
		description = parse_panel(class_page, 'Description')
		class_info.append(description.get_text().strip())

		# Enrollment requirements
		requirements = parse_panel(class_page, 'Enrollment Requirements')
		if requirements:
			class_info.append(requirements.get_text().strip())
		else:
			class_info.append('Prerequisite(s): N/A')

		# Instructor
		meeting_info = parse_list(class_page, 'Meeting Information', 'td')
		if meeting_info:
			class_info.append(meeting_info[2])
		else:
			class_info.append('N/A')

		# GE
		details = class_page.find_all('dd')
		class_info.append(details[5].get_text().strip())

		# Link
		class_info.append(class_element['href'])

		class_info_list.append(class_info)

	return class_info_list

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

# Handles credentials and token if not found (from GSheets API docs)
def getSheetsInstance():

	creds = None
	# The file token.pickle stores the user's access and refresh tokens, and is
	# created automatically when the authorization flow completes for the first
	# time.
	if os.path.exists('token.pickle'):
		with open('token.pickle', 'rb') as token:
			creds = pickle.load(token)
	# If there are no (valid) credentials available, let the user log in.
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(
				'credentials.json', SCOPES)
			creds = flow.run_local_server(port=0)
		# Save the credentials for the next run
		with open('token.pickle', 'wb') as token:
			pickle.dump(creds, token)

	service = build('sheets', 'v4', credentials=creds)

	# Call the Sheets API
	return service.spreadsheets()

if __name__ == '__main__':
	main()