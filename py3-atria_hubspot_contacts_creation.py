#  Code that ALWAYS get executed; either main, or imported as module from other script.
# print(__name__)

# #  LIBRARIES / PACKAGES MANUAL INSTALLATION, if not using devcontainers in VS Code, but single '.py' file stand-alone running.
# #  - NOTE: to manually run in a terminal:
# sudo apt update && sudo apt -y upgrade && sudo apt autoremove   #  Update distro.
# pip install --upgrade pip setuptools                            #  Keep pip, and complement updated: 'https://simpleaudio.readthedocs.io/en/latest/installation.html#installation', 'https://stackoverflow.com/questions/41216875/what-is-the-purpose-of-python-setuptools/41217568#41217568'.
# # pip install os                                                #  Usually built-in module within python; i.e. if so, no need to '$pip install ...'.
# pip install rich==14.1.0                                        #  See 'rich[jupyter]' comment.
# # pip install rich[jupyter]                                     #  Install this, if intended to use rich with Jupyter: 'https://rich.readthedocs.io/en/stable/introduction.html#installation'.
# # pip install warnings                                          #  Usually built-in module within python; i.e. if so, no need to '$pip install ...'.
# # pip install glob                                              #  Usually built-in module within python; i.e. if so, no need to '$pip install ...'.
# # pip install re                                                #  Usually built-in module within python; i.e. if so, no need to '$pip install ...'.
# pip install PyYAML==6.0.2
# # pip install datetime==5.5                                     #  Usually built-in module within python; i.e. if so, no need to '$pip install ...'.
# # pip install zoneinfo                                          #  Usually built-in module within python; i.e. if so, no need to '$pip install ...'.
# pip install requests==2.32.5
# # pip install tkinter                                           #  Usually built-in module within python; i.e. if so, no need to '$pip install ...'.

#  LIBRARIES / PACKAGES IMPORTS.

import os                                   #  To work with directories.
from rich import print as rprint            #  Rich text and beautiful formatting.
import warnings                             #  For showing warnings to developer.
import glob                                 #  For listing files, using UNIX REGEX.
import re                                   #  For REGEX, listing files, format validation of inputs, etc.
import yaml                                 #  For managing input files in YAML format.
import datetime                             #  To manage dates, times, and time durations.
import zoneinfo                             #  For timezones.
import requests                             #  To send HTTP requests.
import tkinter                              #  Simple GUI toolkit.
import tkinter.messagebox                   #  Requires EXPLICIT import: 'https://stackoverflow.com/questions/29774938/tkinter-messagebox-showinfo-doesnt-always-work/29780454#29780454'.

#  USER DEFINEND FUNCTIONS (UDFs).

#  Clear terminal / console output.
#  - Using lambda, anonymous / nameless functions. Ref. 'https://www.freecodecamp.org/news/lambda-expressions-in-python/', 'https://www.geeksforgeeks.org/python/python-lambda-anonymous-functions-filter-map-reduce/'.
UDFClearOutput = lambda: os.system('clear')

#  Validate if a DIRECTORY path exists, and creates it (optionally, True by default) if it doesn't exist.
def UDFValidateDirectoryExists(IPath: str, ICreateDir: bool = True) -> None:
    if (not os.path.exists(IPath)):
        warnings.warn(f"[WARNING] Directory '{IPath}' should exist in order for current script to run properly.")
        if (ICreateDir):
            rprint(f"[LOG] Creating directory: '{IPath}'.")
            os.mkdir(IPath)
    else:
        rprint(f"[LOG] Directory found: '{IPath}'.")
    
    return None

#  Search for basename paths (i.e. files OR directories), starting from a given directory (CURRENT working directory, if not provided) in a RECURSIVELY manner.
def UDFSearchPaths(IBasename: str, IDirpath: str = '**') -> list:
    basename_regex = IBasename.encode('unicode-escape').decode('unicode-escape') + r'$'     #  Python raw strings and RegEx: 'https://www.digitalocean.com/community/tutorials/python-raw-string'.
    search_space_pattern = IDirpath if (IDirpath == '**') else (IDirpath + '/**')
    filepaths_list = [i for i in glob.iglob(search_space_pattern, recursive = True) if re.search(basename_regex, i, re.IGNORECASE)]     #  RegEx re.search() vs. re.match(): 'https://www.geeksforgeeks.org/python/python-re-search-vs-re-match/'.
    #  Throws an AssertionError, if no path found.
    assert len(filepaths_list) > 0, f"[ERROR] File or directory called '{basename_regex[:-1]}' (after unicode escaping) should exist in order for current script to run properly."
    
    return filepaths_list

#  Converts to basic* data types; it requires at MINIMUM: value to convert, and specify it's data type.
#  - *No-iterables: null, boolean, string, integer, decimal, complex, and numeric range (last one, returns a list).
#  - *Iterables: list, tuple, and set. These requiere additionally specification of the data subtype (i.e. type of their elements).
#  It returns the converted value, or 'None' if any mistake on the inputs like:
#  - The data type is not of any of the basic* data types.
def UDFConvertToBasicDataTypes(IValue, IDataType: str, IDataSubType = None):
    
    value_string                = str(IValue).strip()           #  It tries ALWAYS to convert value to string, as a starting point.
    data_type                   = str(IDataType).strip()        #  It tries ALWAYS to convert the input of data type to string, and clean it.
    data_subtype                = str(IDataSubType).strip() if (IDataSubType is not None) else (None)   #  By default is 'None'; otherwise, try to clean it.
    value_converted             = None
    DATA_TYPES                  = (
        'null', 'boolean', 'string', 'integer', 'decimal', 'complex', 'range'
        , 'date and/or time (with or without timezone)'
        , 'time duration'
        , 'list', 'tuple', 'set'
    )
    DATA_TYPES_FOR_ITERABLES    = (
        'null', 'boolean', 'string', 'integer', 'decimal', 'complex', 'range'
        , 'date and/or time (with or without timezone)'
        , 'time duration'
    )

    if data_type not in DATA_TYPES:
        value_converted = None
    else:
        if data_type == 'null':
            value_converted = None
        if data_type == 'boolean':
            value_converted = True if (value_string.lower().capitalize() == 'True') else (False)
        if data_type == 'string':
            value_converted = value_string
        if data_type == 'integer':
            value_converted = int(value_string)
        if data_type == 'decimal':
            value_converted = float(value_string)
        if data_type == 'complex':
            value_converted = complex(value_string)
        if data_type == 'range':
            value_converted = list(range(int(value_string)))
        if data_type == 'date and/or time (with or without timezone)':
            date_time_timezone_format = ''
            date_time = None
            date_time_timezone = None
            #  RegEx expression for searching matches:
            #+ YYYY/MM/DD HH:MM:SS.X[+/-]timezone(in HHMM),
            #+ where YYYY: [1900, 2099], MM: [01, 12], DD: [01, 31], HH: [00, 23], MM: [00, 59], SS: [00, 59], X: [0, 999999].
            #+ e.g. '2011/08/15 12:45:01.095673-0500'.
            #  Test at 'https://regex101.com'.
            date_time_timezone_regex = r'^(?P<date>(?P<year>(19|20)\d{2})/(?P<month>0[1-9]|1[0-2])/(?P<day>0[1-9]|[12][0-9]|3[0-1])\b)? ?(?P<time>\b(?P<hour>[01][0-9]|2[0-3]):(?P<min>[0-5][0-9]):(?P<sec>[0-5][0-9])(\.(?P<microsec>\d{1,6}))?(?P<timezone>(?P<timezone_sign>[+-])(?P<timezone_hour>[01][0-9]|2[0-3])(?P<timezone_min>[0-5][0-9]))?)?$'
            regex_match = re.search(date_time_timezone_regex, value_string)    #  If using re.match(), date_time_timezone_regex = r'...' DOESN'T require '^'; i.e. RegEx re.search() vs. re.match(): 'https://www.geeksforgeeks.org/python/python-re-search-vs-re-match/'.
            if regex_match is not None:
                #  e.g. '2011/08/15 12:45:01.095673-0500'.
                #  date_time_timezone_format = '%Y/%m/%d %H:%M:%S.%f%z'    :date+time+tz    : datetime.datetime.strptime(value_string, date_time_timezone_format) > datetime.datetime.
                #  date_time_timezone_format = '%Y/%m/%d %H:%M:%S.%f'      :date+time       : datetime.datetime.strptime(value_string, date_time_timezone_format) > datetime.datetime.
                #  date_time_timezone_format = '%Y/%m/%d %H:%M:%S'         :date+time       : datetime.datetime.strptime(value_string, date_time_timezone_format) > datetime.datetime.
                #  date_time_timezone_format = '%Y/%m/%d'                  :date            : datetime.datetime.strptime(value_string, date_time_timezone_format) > datetime.date.
                #  date_time_timezone_format = '%H:%M:%S'                  :time            : datetime.datetime.strptime(value_string, date_time_timezone_format) > datetime.time.
                #  date_time_timezone_format = '%H:%M:%S.%f'               :time            : datetime.datetime.strptime(value_string, date_time_timezone_format) > datetime.time.
                #  date_time_timezone_format = '%H:%M:%S.%f%z'             :time+tz         : datetime.datetime.strptime(value_string, date_time_timezone_format) > datetime.time.
                term = (regex_match.group('date') is not None, regex_match.group('time') is not None, regex_match.group('microsec') is not None, regex_match.group('timezone') is not None)
                match term:
                    case (True, True, True, True):          #  e.g. '2011/08/15 12:45:01.095673-0500'.
                        date_time_timezone_format           = '%Y/%m/%d %H:%M:%S.%f%z'
                        date_time                           = datetime.datetime.strptime(value_string, date_time_timezone_format)
                        date_time_timezone                  = date_time
                    case (True, True, True, False):         #  e.g. '2011/08/15 12:45:01.095673'.
                        date_time_timezone_format           = '%Y/%m/%d %H:%M:%S.%f'
                        date_time                           = datetime.datetime.strptime(value_string, date_time_timezone_format)
                        date_time_timezone                  = date_time
                    case (True, True, False, False):        #  e.g. '2011/08/15 12:45:01'.
                        date_time_timezone_format           = '%Y/%m/%d %H:%M:%S'
                        date_time                           = datetime.datetime.strptime(value_string, date_time_timezone_format)
                        date_time_timezone                  = date_time
                    case (True, False, False, False):       #  e.g. '2011/08/15'.
                        date_time_timezone_format           = '%Y/%m/%d'
                        date_time                           = datetime.datetime.strptime(value_string, date_time_timezone_format)
                        date_time_timezone                  = date_time.date()
                    case (False, True, False, False):       #  e.g. '12:45:01'.
                        date_time_timezone_format           = '%H:%M:%S'
                        date_time                           = datetime.datetime.strptime(value_string, date_time_timezone_format)
                        date_time_timezone                  = date_time.time()
                    case (False, True, True, False):        #  e.g. '12:45:01.095673'.
                        date_time_timezone_format           = '%H:%M:%S.%f'
                        date_time                           = datetime.datetime.strptime(value_string, date_time_timezone_format)
                        date_time_timezone                  = date_time.time()
                    case (False, True, True, True):         #  e.g. '12:45:01.095673-0500'. NOTE: timezone data will be lost, since only a 'datetime.datetime' object can store timezone data; not 'datetime.date' nor 'datetime.time' alone.
                        date_time_timezone_format           = '%H:%M:%S.%f%z'
                        date_time                           = datetime.datetime.strptime(value_string, date_time_timezone_format)
                        date_time_timezone                  = date_time.time()
                    case _:                                 #  'Default'.
                        warnings.warn(f"Entry: '{value_string}' doesn't match the format; entry won't be processed. Please review it follows the format: 'YYYY/MM/DD HH:MM:SS.X[+/-]timezone(in HHMM)', where YYYY: [1900, 2099], MM: [01, 12], DD: [01, 31], HH: [00, 23], MM: [00, 59], SS: [00, 59], X: [0, 999999]; e.g. '2011/08/15 12:45:01.095673-0500'.")
            else:
                warnings.warn(f"Entry: '{value_string}' doesn't match the format; entry won't be processed. Please review it follows the format: 'YYYY/MM/DD HH:MM:SS.X[+/-]timezone(in HHMM)', where YYYY: [1900, 2099], MM: [01, 12], DD: [01, 31], HH: [00, 23], MM: [00, 59], SS: [00, 59], X: [0, 999999]; e.g. '2011/08/15 12:45:01.095673-0500'.")
            value_converted = date_time_timezone
        if data_type == 'time duration':
            time_delta = None
            #  Format for time splitting:
            #+ HH:MM:SS,
            #+ where HH: number (integer or decimal), MM: number (integer or decimal), SS: number (integer or decimal).
            #+ e.g. 2 days > 24h*2 > '48:00:00'; 36 min and 2.56 sec > '36:2.56'.
            term = tuple(map(float, value_string.split(':')))
            match term:
                case (split_hours, split_minutes, split_seconds):
                    time_delta = datetime.timedelta(hours = split_hours, minutes = split_minutes, seconds = split_seconds)
                case (split_minutes, split_seconds):
                    time_delta = datetime.timedelta(minutes = split_minutes, seconds = split_seconds)
                case (split_seconds, ):
                    time_delta = datetime.timedelta(seconds = split_seconds)
                case _:                                     #  'Default'.
                    warnings.warn(f"Entry: '{value_string}' doesn't match the format; entry won't be processed. Please review it follows the format: 'HH:MM:SS', where HH: number (integer or decimal), MM: number (integer or decimal), SS: number (integer or decimal); e.g. 2 days > 24h*2 > '48:00:00'; 36 min and 2.56 sec > '36:2.56'")
                    # time_delta = datetime.timedelta()     # '0:00:00'. If ever required in a future, but right now, default return for no matches is 'None'.
            value_converted = time_delta
        if data_subtype in DATA_TYPES_FOR_ITERABLES:            #  To avoid INFINITE RECURSIVENESS; e.g. data_type: 'list', and data_subtype: 'tuple'.
            #  Use of 'map()' to apply a function to iterable(s): 'https://www.geeksforgeeks.org/python/python-map-function/', 'https://www.w3schools.com/python/ref_func_map.asp'.
            #  Repeat an element, several times in a list: 'https://stackoverflow.com/questions/3459098/create-list-of-single-item-repeated-n-times/3459131#3459131'.
            if data_type == 'list':
                value_converted = list(map(UDFConvertToBasicDataTypes, value_string.split('|'), [data_subtype] * len(value_string.split('|'))))
            if data_type == 'tuple':
                value_converted = tuple(map(UDFConvertToBasicDataTypes, value_string.split('|'), [data_subtype] * len(value_string.split('|'))))
            if data_type == 'set':
                value_converted = set(map(UDFConvertToBasicDataTypes, value_string.split('|'), [data_subtype] * len(value_string.split('|'))))

    return value_converted

#  Creates a dictionary of variables, with proper data conversion.
#  - IT REQUIRES CUSTOM FUNCTION UDFConvertToBasicDataTypes().
#  - Input is a LIST in proper format for each variable:
#+ [ { 'name': <variable_name>, 'type': <variable_type_from_UDFConvertToBasicDataTypes()>, 'subtype': <variable_subtype_from_UDFConvertToBasicDataTypes()>,
#+ 'comment': <variable_comment>, 'value': <variable_value> }, { ... } ].
#  - Output format: { <variable1_name> : <variable1_value>, <variable2_name> : <variable2_value>, ...}.
def UDFCreateVariablesDictionaryFromFormattedList(IList: list) -> dict:
    variables_dictionary  = {}
    
    for index, variable in enumerate(IList):                                                        #  Get index of a list iterator: 'https://www.stellargrove.com/how-to-blog/find-the-index-of-the-iterator-of-a-list'.
        (variable_name, variable_type, variable_subtype, variable_comment, variable_value)          = \
        (variable['name'], variable['type'], variable['subtype'], variable['comment'], variable['value'])
        #  Validates MINIMUM fields for a variable to be valid; e.g. 'name', and 'type'. Ref. 'https://ellibrodepython.com/assert-python'.
        assert all([
            variable_name is not None, variable_type is not None
            ]), f"[Variable number '{index + 1}'] In order for a variable to be processed, it requires at MINIMUM: a 'name', and 'type' defined; at least 1 is missing."
        
        variable_name_clean                         = str(variable_name).strip()
        variable_type_clean                         = str(variable_type).strip()
        variable_subtype_clean                      = str(variable_subtype).strip() if (variable_subtype is not None) else (None)

        #  Data transformation.
        variables_dictionary[variable_name_clean]   = UDFConvertToBasicDataTypes(variable_value, variable_type_clean, variable_subtype_clean)

    return variables_dictionary

#  Load variables from formatted dictionary into globals().
def UDFLoadVariablesToGlobals(IDictionary: dict) -> None:
    for variable_name, variable_value in IDictionary.items():
        globals()[variable_name] = variable_value
    rprint(f"[LOG] Variables loaded to 'globals()' (x{len(IDictionary)}): '{"' | '".join([*IDictionary.keys()])}'.")

    return None

#  Function to make calls to HubStop API, for either: a. get contacts, b. create a batch of contacts.
#  - Function depends on API URL node passed as parameter; i.e. 'IApiUrlNode'.
#    - e.g. IApiUrlNode = 'crm/v3/objects/contacts', is for getting HubSpot account contacts.
#    - e.g. IApiUrlNode = 'crm/v3/objects/contacts/batch/create', is for creating a batch of contacts; it requires a JSON payload; i.e. 'IApiPayload'.
#  - Function only returns if there are no errors in API connection, and returns a dictionary with JSON response.
def UDFHubSpotSendAPIRequest(IApiUrl: str, IApiUrlNode: str, IApiToken: str, IApiPayload: dict = {}) -> dict:
    api_results = {}
    api_headers = {}

    #  HTTP Request: url.
    api_url = IApiUrl + IApiUrlNode

    #  HTTP Request: headers.
    api_token = "Bearer " + IApiToken

    #  Validate if payload (as dictionary) is empty.
    if not bool(IApiPayload):
        
        #  If no payload, it's for requesting contacts.
        api_headers = {
            "Authorization": api_token
        }

        rprint(f"[LOG] Making HTTP request to API... URL node: '{api_url}'.")
        #  HTTP Request - GET.
        api_response = requests.get(api_url, headers = api_headers)

    else:
        
        #  If payload, it's for creating contacts.
        api_headers = {
            "Authorization": api_token,
            "Content-Type": "application/json"
        }
        api_payload = IApiPayload

        rprint(f"[LOG] Making HTTP request to API... URL node: '{api_url}'.")
        #  HTTP Request - POST.
        api_response = requests.post(api_url, headers = api_headers, json = api_payload)
    
    #  Validate if there were any errors: 'https://www.w3schools.com/python/ref_requests_response.asp'.
    if not api_response.ok:
        rprint(f"[LOG] Error connecting to API... Reason: [{api_response.status_code}] '{api_response.reason}'. Error message: {api_response.text}")
        #  Raise an exception if connection wasn't possible: 'https://requests.readthedocs.io/en/latest/user/quickstart/#response-status-codes'.
        # api_response.raise_for_status()
    else:
        rprint(f"[LOG] HTTP request to API successful. Reason: [{api_response.status_code}] '{api_response.reason}'.")
        
        if bool(IApiPayload):
            rprint(f"[LOG] Please validate contacts creation in your personal HubStop account at 'https://app.hubspot.com/contacts/<account_id>'.")
    
    #  HTTP Request - Result (as dictionary).
    api_results = api_response.json()
    return api_results

#  [FORM] Validate first name format.
def UDFFormRegisterValidateFirstName(IValue: str) -> bool:
    validation = False
    value_string = IValue.strip()

    if value_string == '':
        first_name_entry.delete(0, tkinter.END) # pyright: ignore[reportUndefinedVariable]
    else:
        validation = True
        
    return validation

#  [FORM] Validate last name format.
def UDFFormRegisterValidateLastName(IValue: str) -> bool:
    validation = True
    value_string = IValue.strip()

    if value_string == '':
        last_name_entry.delete(0, tkinter.END) # pyright: ignore[reportUndefinedVariable]
        
    return validation

#  [FORM] Validate email format.
def UDFFormRegisterValidateEmail(IValue: str) -> bool:
    validation = False
    value_string = IValue.strip()

    if value_string == '':
        email_entry.delete(0, tkinter.END) # pyright: ignore[reportUndefinedVariable]
    
    re_pattern = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')        #  Email regex pattern: 'https://www.w3resource.com/python-exercises/pandas/pandas-validate-email-format-in-a-column-using-regex.php'.
    if re_pattern.match(value_string) is not None:
        validation = True

    return validation

#  [FORM] Create a function to get data from Entry fields.
def UDFFormRegister():
    
    #  Get user input from the form.
    first_name                  = first_name_entry.get() # pyright: ignore[reportUndefinedVariable]
    # print(type(first_name), "'",first_name, "'", sep='')
    #  Validate inputs: 'https://www.geeksforgeeks.org/python/validating-entry-widget-in-python-tkinter/'.
    first_name_validation       = UDFFormRegisterValidateFirstName(first_name)
    last_name                   = last_name_entry.get() # pyright: ignore[reportUndefinedVariable]
    last_name_validation        = UDFFormRegisterValidateLastName(last_name)
    email                       = email_entry.get() # pyright: ignore[reportUndefinedVariable]
    email_validation            = UDFFormRegisterValidateEmail(email)
    
    # print(first_name_validation, last_name_validation, email_validation)
    #  Validate if all validations are 'True': 'https://www.w3schools.com/python/ref_func_all.asp'.
    if all([first_name_validation, last_name_validation, email_validation]):

        new_contact_payload = {
            "properties": {
                "email": email,
                "firstname": first_name,
                "lastname": last_name # TODO: it can be 'empty'; review how to dynamically adjust dictionary, to not include it in those cases.
            }
        }

        api_results_create_contacts = UDFHubSpotSendAPIRequest(
            IApiUrl = _HUBSPOT_API_URL, # pyright: ignore[reportUndefinedVariable]
            IApiUrlNode = _HUBSPOT_API_URL_NODE_CONTACTS, # pyright: ignore[reportUndefinedVariable]
            IApiToken = _HUBSPOT_API_TOKEN, # pyright: ignore[reportUndefinedVariable]
            IApiPayload = new_contact_payload
        )
        # rprint(api_results_create_contacts)
        tkinter.messagebox.showinfo('Information', 'Please validate execution results with LOG messages in the console / terminal.')
    
    else:

        #  Show warning message: 'https://www.geeksforgeeks.org/python/python-tkinter-messagebox-widget/'.
        tkinter.messagebox.showwarning('Warning', "At least one field is not valid. Please make sure all fields are valid; i.e. 'First name' is not empty, 'Email' is not empty and it has a valid email format.")

    #  Clean entries: 'https://web.archive.org/web/20201111190045id_/https://effbot.org/tkinterbook/entry.htm'.
    first_name_entry.delete(0, tkinter.END) # pyright: ignore[reportUndefinedVariable]
    last_name_entry.delete(0, tkinter.END) # pyright: ignore[reportUndefinedVariable]
    email_entry.delete(0, tkinter.END) # pyright: ignore[reportUndefinedVariable]

    #  Set 1st entry as focus: 'https://stackoverflow.com/questions/13626406/setting-focus-to-specific-tkinter-entry-widget/13626607#13626607'.
    first_name_entry.focus() # pyright: ignore[reportUndefinedVariable]

#  [FORM] Function to launch form for data collection.
def UDFFormLaunch():

    #  Create main tkinter window.

    root                    = tkinter.Tk()
    root.title('Registration form')
    root.geometry('300x200')            #  Width x height.

    #  Create labels and entry fields, for each input.

    first_name_label        = tkinter.Label(root, text = "First name")
    first_name_label.pack()     #  Positions widgets in horizontal and vertical boxes that are limited to left, right, top, and bottom positions. Each box is offset and relative to each other.
    global first_name_entry     #  Declare entry as global, fro 'UDFFormRegister' to access it: 'https://www.w3schools.com/python/python_variables_global.asp'.
    first_name_entry        = tkinter.Entry(root)
    first_name_entry.pack()

    last_name_label         = tkinter.Label(root, text = "Last name")
    last_name_label.pack()
    global last_name_entry
    last_name_entry         = tkinter.Entry(root)
    last_name_entry.pack()

    email_label             = tkinter.Label(root, text = "Email")
    email_label.pack()
    global email_entry
    email_entry             = tkinter.Entry(root)
    email_entry.pack()

    #  Create Submit Button.

    register_button         = tkinter.Button(root, text = 'Register', command = UDFFormRegister)
    register_button.pack()

    #  Run the main loop.

    root.mainloop()

#  MAIN FUNCTION.
def main():
    
    #  'main()' INITIALIZATION.

    UDFClearOutput()        #  Clear screen.

    #  INPUTS.

    #  Main directory.

    _PROJECT_BASE_FILENAME       = 'py3-atria_hubspot_contacts_creation'

    home_dirpath = None
    #  How to get a python filepath: 'https://note.nkmk.me/en/python-script-file-path/'.
    #  How to get a python filepath, considering Jupyter Notebooks: 'https://medium.com/@jennycoreholt/how-to-professionally-import-external-files-in-jupyter-notebooks-4000f1ce16f7'.
    if '__file__' in globals():
        file_filepath   = None
        #  If it's a regular python file / module: 'https://stackoverflow.com/questions/38412495/difference-between-os-path-dirnameos-path-abspath-file-and-os-path-dirnam/38412504#38412504', 'https://community.esri.com/t5/python-blog/finding-python-script-home-folder/bc-p/884009/highlight/true'.
        #  Alternative: 'https://saturncloud.io/blog/how-to-obtain-jupyter-notebooks-path/'.
        file_filepath   = os.path.abspath(__file__)
        home_dirpath    = os.path.dirname(file_filepath)
    else:
        #  If it's a Jupyter Notebook: 'https://stackoverflow.com/questions/39125532/file-does-not-exist-in-jupyter-notebook/53958599#53958599', 'https://forums.fast.ai/t/file-dunder-attribute-works-in-py-not-in-notebook/102400/7'.
        home_dirpath    = str(globals()['_dh'][0])

    #  Input: data.
    input_dirpath_relative_to_home                      = 'io_dir-input'        #  Dirpath relative to home directory.
    input_configuration_dirpath_relative_to_home        = os.path.join(input_dirpath_relative_to_home, 'config')        #  Directory for configuration files.
    input_user_parameters_dirpath_relative_to_home      = os.path.join(input_dirpath_relative_to_home, 'user_params')   #  Directory for input user instructions, if required.
    input_user_files_dirpath_relative_to_home           = os.path.join(input_dirpath_relative_to_home, 'user_files')    #  Directory for user files, if input required.

    input_configuration_filenames_regex     = _PROJECT_BASE_FILENAME + r'-input_.*(?<!-TEMPLATE)\.yaml'                 #  String literal for RegEx expresion of configuration filenames patterns; e.g. '...-input-<...>.yaml': 'https://www.w3schools.com/python/python_regex.asp', 'https://regex101.com'. Files listing base variables and their structure; e.g. user timezone, column names for dataframes, etc. NOTE: it excludes files with text '-TEMPLATE' at the end, before the extension. NOTE: all matching files will be processed the SAME WAY.

    #  Output.
    output_dirpath_relative_to_home         = 'io_dir-output'                   #  Dirpath relative to home directory.

    #  INITIALIZATION.

    #  Print current working directory.
    working_directory = os.getcwd()
    rprint(f"[LOG] Current working directory: '{working_directory}'.")
    
    #  Set working directory to 'home'.
    rprint(f"[LOG] Changing current working directory to: '{home_dirpath}'.")
    os.chdir(home_dirpath)
    working_directory = os.getcwd()
    rprint(f"[LOG] Current working directory: '{working_directory}'.")

    #  [INITIALIZATION] PROJECT BASE STRUCTURE VALIDATION.

    #  Inputs validations: wheter or not exists input directory.
    UDFValidateDirectoryExists(input_dirpath_relative_to_home)

    #  Inputs validations: wheter or not exists configuration sub-directory (of input directory).
    #  NOTE: it REQUIRES parent directory (input directory) to exist.
    UDFValidateDirectoryExists(input_configuration_dirpath_relative_to_home)

    #  Inputs validations: wheter or not exists user parameters sub-directory (of input directory).
    #  NOTE: it REQUIRES parent directory (input directory) to exist.
    UDFValidateDirectoryExists(input_user_parameters_dirpath_relative_to_home)

    #  Inputs validations: wheter or not exists user files sub-directory (of input directory).
    #  NOTE: it REQUIRES parent directory (input directory) to exist.
    UDFValidateDirectoryExists(input_user_files_dirpath_relative_to_home)

    #  Outputs validations: wheter or not exists output directory.
    UDFValidateDirectoryExists(output_dirpath_relative_to_home)

    #  Inputs validations: searches for configuration of base variables.
    input_configuration_filepaths_relative_to_home          = UDFSearchPaths(input_configuration_filenames_regex, input_configuration_dirpath_relative_to_home)
    rprint(f"[LOG] Configuration files found (x{len(input_configuration_filepaths_relative_to_home)}): '{"' | '".join(input_configuration_filepaths_relative_to_home)}'.")
    
    #  [INITIALIZATION] INPUT: CONFIGURATION FILE(S) LOAD.

    #  Load configuration YAML file.
    #  - Load '.yaml' file: 'https://www.geeksforgeeks.org/python/parse-a-yaml-file-in-python/'.
    yaml_variables_data = None
    yaml_variables_list = []

    for yaml_filepath in input_configuration_filepaths_relative_to_home:
        with open(yaml_filepath, 'r') as file:
            yaml_variables_data = yaml.load(file, Loader = yaml.SafeLoader)
        if yaml_variables_data is not None:                              #  1st check YAML file is not empty.
            if yaml_variables_data['parameters'] is not None:            #  2nd check if there is a 'parameters' section.
                yaml_variables_list += yaml_variables_data['parameters']      #  Or also could use '<list>.extend(<other_list>)': 'https://sparkbyexamples.com/python/python-append-list-to-a-list/'.
                # rprint(f"[LOG] Variables imported (x{len(yaml_variables_data['parameters'])}), from '{yaml_filepath}'.")

    rprint(f"[LOG] Variables imported in total (x{len(yaml_variables_list)}), from: '{"' | '".join(input_configuration_filepaths_relative_to_home)}'.")

    #  Get a dictionary of variables from YAML file, with proper data conversion.
    yaml_variables_dictionary = UDFCreateVariablesDictionaryFromFormattedList(yaml_variables_list)

    #  Load variables YAML file into globals().
    UDFLoadVariablesToGlobals(yaml_variables_dictionary)

    #  Set execution timezone.
    _TIME_ZONE = zoneinfo.ZoneInfo(_USER_GEOGRAPHIC_TIMEZONE) # pyright: ignore[reportUndefinedVariable]

    #  [MAIN] FORM LAUNCH.
    UDFFormLaunch()

#  CODE EXECUTION.

#  Code executed ONLY when script is called directly; NOT IMPORTED from other script.
if __name__ == '__main__':
    main()
