from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from googleapiclient.errors import HttpError
""" try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None
"""
import argparse

from .config import CLIENT_SECRET_FILE, SCOPES, APPLICATION_NAME
from .params import GET_NOTES_API, SPREADSHEET_ID, EVALUATION_NAME, SHEET_ID
from itertools import zip_longest
import time
import json
from log import cool_print_decoration
import sys

STUDENTS_FILE_NAME = 'students_and_qr.txt'

def get_credentials():
    """
    Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Same example code from Google.
    :return: Credentials, the obtained credential.
    """

    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'sheets.googleapis.com-python-quickstart.json')
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        cool_print_decoration('Storing credentials to ' + credential_path, style = 'info')
    return credentials

def create_service(http, _type):
    """
    Creates callable Google service.
    :param http: authorization
    :param _type: SHEETS o SCRIPT.
    :return: function that calls google's correponding api.
    """
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?version=v4')
    if _type == 'SHEETS':
        service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl).spreadsheets().values()

        def __service_sheets(range, extract=True):
            """
            Calls Google's service and returns array result from an api call
            :param range: Cell range to look for
            :param extract: Boolean that indicates top level extraction
            :return: array of elements resulting from api call
            """
            try:
                result = service.get(spreadsheetId=SPREADSHEET_ID, range=range).execute()['values']
            except HttpError as e:
                cool_print_decoration("Request limit reached. Try again later (>100s)\n{}".format(e), style = 'alert')
                sys.exit(0)
            else:
                return result[0] if extract else result

        return __service_sheets
    else:
        service = discovery.build('script', 'v1', http=http).scripts()

        def __service_scripts(range):
            """
            Calls Google's service and returns array result from an api call
            :param range: Cell range to look for
            :return: array of elements resulting from api call
            """
            script_name = 'getNotes'  # spreadsheet script function name
            return service.run(body={"function": script_name, "parameters": [SPREADSHEET_ID, range]}
                               , scriptId=GET_NOTES_API).execute()['response']['result'][0]

        return __service_scripts

def get_headers(service, _info="A1"):
    """
    Gets header from spreadsheet
    :param service: Google sheets function service
    :param _info: Cell where starting and ending range is placed
    :return: string that represents start and end range from spreadsheet
    """

    header_range = service(_info)[0]
    return header_range

def range_row_modifier(header_range):
    """
    Yields next range to look for
    :param header_range: String that represents start and end range from spreadsheet
    :return: Yields next range
    """
    start, end = header_range.split(':')
    next_num = int(start[-1]) + 1
    start = start[:1]
    end = end[:1]
    while True:
        yield ':'.join(['{0}{1}'.format(start, next_num), '{0}{1}'.format(end, next_num)])
        next_num += 1

def column_letter_to_number(column_letter):
    """
    Converts letter to integer
    :param column_letter: String that represents a column in spreadsheet/Excel styling
    :return: Integer that represents column_letter
    """

    # https://stackoverflow.com/questions/7261936/convert-an-excel-or-spreadsheet-
    # column-letter-to-its-number-in-pythonic-fashion
    expn = 0
    col_num = 0
    for char in reversed(column_letter):
        col_num += (ord(char) - ord('A') + 1) * (26 ** expn)
        expn += 1

    return col_num

def column_number_to_letter(number):
    """
    Converts integer to letter
    :param number: Integer that represents a column
    :return: String that represents a letter in spreadsheet/Excel styling
    """

    # https://stackoverflow.com/questions/23861680/convert-spreadsheet-number-to-column-letter
    string = ""
    while number > 0:
        number, remainder = divmod(number - 1, 26)
        string = chr(65 + remainder) + string
    return string

def sheet_id(credentials):
    service = discovery.build('sheets', 'v4', credentials=credentials)
    try:
        request = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
    except HttpError as e:
        cool_print_decoration("Request limit reached. Try again later (>100s)\n{}".format(e), style = 'alert')
        sys.exit(0)
    else:
        return request['sheets'][0]['properties']['sheetId']

def get_row_number(column_row_range):
    index = 0
    column_row_range = column_row_range.split(':')[0]
    while column_row_range[index:][0].isalpha():
        index += 1
    return column_row_range[index:]

def add_data(students_dict, data_array):
    student_name = data_array[0]
    student_qr_array = data_array[1:]
    for qr_number in student_qr_array:
        students_dict[qr_number] = student_name
    return students_dict

def main(path, evaluation_name, *args, **kwargs):
    students_qr = {}
    print(SPREADSHEET_ID)
    cool_print_decoration('Starting connection with API.', style = 'info')
    # initialize conections
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service_sheets = create_service(http, "SHEETS")
    SHEET_ID = sheet_id(credentials)
    cool_print_decoration('Connection with API successful.', style = 'result')

    # initialize data
    header_range = get_headers(service_sheets)
    header = service_sheets(header_range)
    range_generator = range_row_modifier(header_range)

    new_path = os.path.abspath(path)
    if os.path.exists("{}/{}/{}".format(new_path, evaluation_name, STUDENTS_FILE_NAME)):
        cool_print_decoration('Information already stored in {}/{}/{}\n\nTo update data, delete previous file.'.format(new_path, evaluation_name, STUDENTS_FILE_NAME), style = 'info')
        return 1

    cool_print_decoration('Starting data recolection.', style = 'info')
    # start
    while True:
        nxt = next(range_generator)
        row = get_row_number(nxt)
        if (int(row) % 90 == 0):
            # API limit requests: 100 requests per 100s per user
            cool_print_decoration('Too many requests. Going to sleep...', style = 'info')
            time.sleep(100)
            cool_print_decoration('Ready to work again!', style = 'result')
        try:
            data = service_sheets(nxt)
            if len(data) > 1:
                student_name = data[0]
                student_qr_array = data[1:]
                students_qr[student_name] = student_qr_array
                # for qr_number in student_qr_array:
                #    students_qr[qr_number] = student_name
        except KeyError:
            cool_print_decoration('Done with API.', style = 'result')
            # print('I\'m out of range')
            break


    # Create directory
    if not os.path.exists("{}/{}".format(new_path, evaluation_name)):
        cool_print_decoration('Creating directory {} in: {} path.'.format(evaluation_name, new_path), style = 'info')
        os.mkdir("{}/{}".format(new_path, evaluation_name))
        print("\n{}: {}".format(new_path + evaluation_name, os.path.exists(new_path + evaluation_name)))

    if not os.path.exists("{}/{}/{}".format(new_path, evaluation_name, STUDENTS_FILE_NAME)):
        cool_print_decoration('Storing information in {}/{}/{}'.format(new_path, evaluation_name, STUDENTS_FILE_NAME), style = 'info')
        try:
            with open("{}/{}/{}".format(path, evaluation_name, STUDENTS_FILE_NAME), 'w') as file:
                json.dump(students_qr, file, indent=4)
            cool_print_decoration('Information stored!', style = 'result')
        except FileNotFoundError as e:
            cool_print_decoration('FileNotFoundError', style = 'alert')
if __name__ == '__main__':
    main('./', 'i1')
