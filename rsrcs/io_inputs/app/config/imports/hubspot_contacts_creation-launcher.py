# #  Code that ALWAYS get executed; either main, or imported as module from other script.
# print(__name__, "---", sep = "\n")

#  LIBRARIES / PACKAGES IMPORTS.

from js import console                  #  [PKG INSTALLATION - PYSCRIPT] DO NOT add to config. file (TOML | JSON).          #  Allows usage of 'console.log()' function from JavaScript (JS).
import os                               #  [PKG INSTALLATION - PYSCRIPT] DO NOT add to config. file (TOML | JSON).          #  To work with directories.
import warnings                         #  [PKG INSTALLATION - PYSCRIPT] DO NOT add to config. file (TOML | JSON).          #  For showing warnings to developer.
import glob                             #  [PKG INSTALLATION - PYSCRIPT] DO NOT add to config. file (TOML | JSON).          #  For listing files, using UNIX REGEX.
import re                               #  [PKG INSTALLATION - PYSCRIPT] DO NOT add to config. file (TOML | JSON).          #  For REGEX, listing files, format validation of inputs, etc.
import json                             #  [PKG INSTALLATION - PYSCRIPT] DO NOT add to config. file (TOML | JSON).          #  To convert Python objects (generally lists and dictionaries with appropiate structure) to JSONs strings (a.k.a. 'dumps'), and viceversa (a.k.a. 'loads').
import yaml                             #  [PKG INSTALLATION - PYSCRIPT] Added to config. file (TOML | JSON).               #  For managing input files in YAML format.
import datetime                         #  [PKG INSTALLATION - PYSCRIPT] DO NOT add to config. file (TOML | JSON).          #  To manage dates, times, and time durations.
import tzdata                           #  [PKG INSTALLATION - PYSCRIPT] Added to config. file (TOML | JSON).               #  NOTE: PRE-REQUISITE for 'zoneinfo'.
import zoneinfo                         #  [PKG INSTALLATION - PYSCRIPT] DO NOT add to config. file (TOML | JSON).          #  For timezones.
# import requests                         #  [PKG INSTALLATION - PYSCRIPT] Added to config. file (TOML | JSON).               #  To send HTTP requests. NOTE: not using YET, since when using it with PyScript from a client / web-browser, depending on the API (e.g. HubSpot), it could block requests and throw CORS error: 'https://developers.hubspot.com/docs/cms/reference/serverless-functions/serverless-functions#cors', 'https://www.kelp.agency/blog/how-to-enable-cors-ajax-requests-for-any-hubspot-api/'.
from pyscript import when               #  [PKG INSTALLATION - PYSCRIPT] DO NOT add to config. file (TOML | JSON).          #  [PyScript] Allows usage of 'pyscript.when' decorator for Python functions, to handle events: 'https://docs.pyscript.net/2024.8.1/api/#pyscriptwhen'.
from pyscript import document           #  [PKG INSTALLATION - PYSCRIPT] DO NOT add to config. file (TOML | JSON).          #  [PyScript] To manage html elements, via DOM: 'https://docs.pyscript.net/2024.8.1/api/#pyscriptdocument'.
# from pyscript import display            #  [PKG INSTALLATION - PYSCRIPT] DO NOT add to config. file (TOML | JSON).          #  [PyScript] Displays content, using in-function intelligence for proper display: 'https://docs.pyscript.net/2024.8.1/api/#pyscriptdisplay'.

#  USER DEFINEND FUNCTIONS (UDFs).

#  Function to print LOG in both environments: Python, and browser console, via JS.
#  - NOTE: requires import package 'js' ('console' module), to print in console.
def UDFPrintLog(IMessage: str) -> None:
    
    #  Prints log in Python console.
    print(IMessage)
    #  Prints log in JS console.
    console.log(IMessage)

    return None

# #  NOTE: doesn't work with PyScript in a browser.
# #  Clear terminal / console output.
# #  [OP01] Traditional way.
# # def UDFClearOutput() -> None:
# #     os.system('clear')      #  Executes os function called 'clear'. Either in Linux or Windows, clear() clears terminal / console / CLI output.
# #     return None
# #  [OP02] Using lambda, anonymous / nameless functions. Ref. 'https://www.freecodecamp.org/news/lambda-expressions-in-python/', 'https://www.geeksforgeeks.org/python/python-lambda-anonymous-functions-filter-map-reduce/'.
# UDFClearOutput = lambda: os.system('clear')

# #  NOTE: not used in working with PyScript in a browser, since config. file (TOML | JSON) is used to create specific folders and files in the'in-browser' filesystem.
# #  Validate if a DIRECTORY path exists, and creates it (optionally, True by default) if it doesn't exist.
# def UDFValidateDirectoryExists(IPath: str, ICreateDir: bool = True) -> None:
#     if (not os.path.exists(IPath)):
#         warnings.warn(f"[WARNING] Directory '{IPath}' should exist in order for current script to run properly.")
#         if (ICreateDir):
#             print(f"[LOG] Creating directory: '{IPath}'.")
#             os.mkdir(IPath)
#     else:
#         print(f"[LOG] Directory found: '{IPath}'.")

    return None

#  Search for basename paths (i.e. files OR directories), starting from a given directory (CURRENT working directory, if not provided) in a RECURSIVELY manner.
def UDFSearchPaths(IBasename: str, IDirpath: str = '**') -> list:
    filepaths_list = []
    basename_regex = IBasename.encode('unicode-escape').decode('unicode-escape') + r'$'     #  Python raw strings and RegEx: 'https://www.digitalocean.com/community/tutorials/python-raw-string'.
    search_space_pattern = IDirpath if (IDirpath == '**') else (IDirpath + '/**')
    filepaths_list = [i for i in glob.iglob(search_space_pattern, recursive = True) if re.search(basename_regex, i, re.IGNORECASE)]     #  RegEx re.search() vs. re.match(): 'https://www.geeksforgeeks.org/python/python-re-search-vs-re-match/'.
    #  Throws an AssertionError, if no path found.
    assert len(filepaths_list) > 0, f"[ERROR] File or directory called '{basename_regex[:-1]}' (after unicode escaping) should exist in order for current script to run properly."
    
    return filepaths_list

#  [AUXILIARY] Prettify JSONs; i.e. converts Python object (generally lists and dictionaries with appropiate structure) to JSON string (a.k.a. 'dumps'). Ref. 'https://www.dataquest.io/blog/api-in-python/'.
def UDFJsonPrint(IObject) -> None:
    text = json.dumps(IObject, sort_keys = False, indent = 4)
    print(text)
    
    return None

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
#  - NOTE: IT REQUIRES CUSTOM FUNCTION UDFConvertToBasicDataTypes().
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
    print(f"[LOG] Variables loaded to 'globals()' (x{len(IDictionary)}): '{"' | '".join([*IDictionary.keys()])}'.")

    return None

#  Get HTML element's value: if 'innerHTML'; e.g. "<div>some text</div>".
#+ Otherwise, 'value' element's property; e.g. "<input value='some text' />".
#  Ref.: 'https://superuser.com/questions/1037389/innerhtml-vs-value-when-and-why',
#+ 'https://stackoverflow.com/questions/8823498/setting-innerhtml-vs-setting-value-with-javascript'.
def UDFGetHTMLValue(IID: str, IIsProperty: bool = True) -> str:
    
    html_element_value          = ''
    html_element                = document.querySelector(f'#{IID}')             #  e.g. Methods to get value of 'input' HTML tag: 'https://stackoverflow.com/questions/11563638/how-do-i-get-the-value-of-text-input-field-using-javascript/11563667#11563667'.

    if (IIsProperty):
        html_element_value      = html_element.value
    else:
        html_element_value      = html_element.innerHTML

    return html_element_value

#  Set HTML element's value; '.value' vs '.innerHTML'.
def UDFSetHTMLValue(IID: str, IInput: str, IIsProperty: bool = True) -> None:

    html_element                = document.querySelector(f'#{IID}')
    
    if (IIsProperty):
        html_element.value      = IInput
    else:
        html_element.innerHTML  = IInput

    return None

#  Validate API token format.
def UDFValidateFormatAPIToken(IHTMLObject) -> bool:

    validation                  = False
    html_id                     = IHTMLObject.id

    html_value                  = UDFGetHTMLValue(html_id)
    value_string                = html_value.strip()

    if value_string == '':
        UDFSetHTMLValue(html_id, '')

    re_pattern = re.compile(r'^pat-')                       #  HubSpot API regex pattern.
    if re_pattern.match(value_string) is not None:
        UDFSetHTMLValue(html_id, value_string)
        validation = True
    
    return validation

#  Validate contact first name format.
def UDFValidateFormatContactFirstName(IHTMLObject) -> bool:

    validation                  = False
    html_id                     = IHTMLObject.id

    html_value                  = UDFGetHTMLValue(html_id)
    value_string                = html_value.strip()

    if value_string == '':
        UDFSetHTMLValue(html_id, '')
    else:
        UDFSetHTMLValue(html_id, value_string)
        validation = True
    
    return validation

#  Validate contact last name format.
#  - NOTE: ALWAYS 'True'; only cleans up field.
def UDFValidateFormatContactLastName(IHTMLObject) -> bool:

    validation                  = True
    html_id                     = IHTMLObject.id

    html_value                  = UDFGetHTMLValue(html_id)
    value_string                = html_value.strip()

    if value_string == '':
        UDFSetHTMLValue(html_id, '')
    else:
        UDFSetHTMLValue(html_id, value_string)
        # validation = True
    
    return validation

#  Validate contact email format.
def UDFValidateFormatContactEmail(IHTMLObject) -> bool:

    validation                  = False
    html_id                     = IHTMLObject.id

    html_value                  = UDFGetHTMLValue(html_id)
    value_string                = html_value.strip()

    if value_string == '':
        UDFSetHTMLValue(html_id, '')

    re_pattern = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')        #  Email regex pattern: 'https://www.w3resource.com/python-exercises/pandas/pandas-validate-email-format-in-a-column-using-regex.php'.
    if re_pattern.match(value_string) is not None:
        UDFSetHTMLValue(html_id, value_string)
        validation = True
    
    return validation

# #  NOTE: not using YET, since when using it with PyScript from a client / web-browser, depending on the API (e.g. HubSpot), it could block requests and throw CORS error: 'https://developers.hubspot.com/docs/cms/reference/serverless-functions/serverless-functions#cors'.
# #+ ALTERNATIVE: use simple PHP server for request: 'https://www.kelp.agency/blog/how-to-enable-cors-ajax-requests-for-any-hubspot-api/'.
# #  Function to make calls to HubStop API, for either: a. get contacts, b. create a batch of contacts.
# #  - Function depends on API URL node passed as parameter; i.e. 'IApiUrlNode'.
# #    - e.g. IApiUrlNode = 'crm/v3/objects/contacts', is for getting HubSpot account contacts.
# #    - e.g. IApiUrlNode = 'crm/v3/objects/contacts/batch/create', is for creating a batch of contacts; it requires a JSON payload; i.e. 'IApiPayload'.
# #  - Function only returns if there are no errors in API connection, and returns a dictionary with JSON response.
# def UDFHubSpotSendAPIRequest(IApiUrl: str, IApiUrlNode: str, IApiToken: str, IApiPayload: dict = {}) -> dict:
#     api_results = {}
#     api_headers = {}
#
#     #  HTTP Request: url.
#     api_url = IApiUrl + IApiUrlNode
#
#     #  HTTP Request: headers.
#     api_token = "Bearer " + IApiToken
#
#     #  Validate if payload (as dictionary) is empty.
#     if not bool(IApiPayload):
#
#         #  If no payload, it's for requesting contacts.
#         api_headers = {
#             "Authorization": api_token
#         }
#
#         UDFPrintLog(f"[LOG] Making HTTP request to API... URL node: '{api_url}'.")
#         #  HTTP Request - GET.
#         api_response = requests.get(api_url, headers = api_headers)
#
#     else:
#
#         #  If payload, it's for creating contacts.
#         api_headers = {
#             "Authorization": api_token,
#             "Content-Type": "application/json"
#         }
#         api_payload = IApiPayload
#
#         UDFPrintLog(f"[LOG] Making HTTP request to API... URL node: '{api_url}'.")
#         #  HTTP Request - POST.
#         api_response = requests.post(api_url, headers = api_headers, json = api_payload)
#
#     #  Validate if there were any errors: 'https://www.w3schools.com/python/ref_requests_response.asp'.
#     if not api_response.ok:
#         UDFPrintLog(f"[ERROR] Error connecting to API... Reason: [{api_response.status_code}] '{api_response.reason}'. Error message: {api_response.text}")
#         #  Raise an exception if connection wasn't possible: 'https://requests.readthedocs.io/en/latest/user/quickstart/#response-status-codes'.
#         # api_response.raise_for_status()
#     else:
#         UDFPrintLog(f"[SUCCESS] HTTP request to API successful. Reason: [{api_response.status_code}] '{api_response.reason}'.")
#
#         if bool(IApiPayload):
#             UDFPrintLog(f"[LOG] Please validate contacts creation in your personal HubStop account at 'https://app.hubspot.com/contacts/<account_id>'.")
#
#     #  HTTP Request - Result (as dictionary).
#     api_results = api_response.json()
#     return api_results

#  Function to manage workflow when button with id '#button_validate_api_token' is clicked.
#  - NOTE: requires importing 'when' module from package 'pyscript', to add decorators.
@when("click", "#button_validate_api_token")
def UDFValidateAPIToken(event) -> None:

    api_token                               = ''

    #  Get user input from the html; e.g. API token from element with id 'input_api_token'.
    api_token_html_element                  = document.querySelector('#input_api_token')
    api_token_format_validation             = UDFValidateFormatAPIToken(api_token_html_element)
    if api_token_format_validation:
        api_token                           = UDFGetHTMLValue(api_token_html_element.id)

    #  Validate if all validations are 'True': 'https://www.w3schools.com/python/ref_func_all.asp'.
    if all([api_token_format_validation]):
        
        # #  NOTE: not using YET, since when using it with PyScript from a client / web-browser, depending on the API (e.g. HubSpot), it could block requests and throw CORS error: 'https://developers.hubspot.com/docs/cms/reference/serverless-functions/serverless-functions#cors'.
        # #+ ALTERNATIVE: use simple PHP server for request: 'https://www.kelp.agency/blog/how-to-enable-cors-ajax-requests-for-any-hubspot-api/'.
        # api_results_listing_contacts        = UDFHubSpotSendAPIRequest(

        #     IApiUrl = _HUBSPOT_API_URL,
        #     IApiUrlNode = _HUBSPOT_API_URL_NODE_CONTACTS,
        #     IApiToken = api_token,

        # )

        UDFPrintLog(f"[SUCCESS] API token is valid. Please validate contacts list was retrieved succesfully.")

        #  Enables parameter fields for inputs.
        globals()['_IS_HUBSPOT_API_TOKEN_VALIDATED']    = True          #  To set globally; e.g. outside 'main()': 'https://www.w3schools.com/python/python_variables_global.asp'. NOTE: previous method of using keyword 'global' didn't work.
        contact_first_name_html_element                 = document.querySelector('#input_contact_first_name')
        contact_first_name_html_element.disabled        = False         #  Disable an input element: 'https://stackoverflow.com/questions/2874688/how-to-disable-an-input-type-text/2874745#2874745'.
        contact_last_name_html_element                  = document.querySelector('#input_contact_last_name')
        contact_last_name_html_element.disabled         = False
        contact_email_html_element                      = document.querySelector('#input_contact_email')
        contact_email_html_element.disabled             = False
        create_contact_html_element                     = document.querySelector('#button_create_contact')
        create_contact_html_element.disabled            = False
                
        contact_first_name_html_element.focus()                         #  Set focus with JavaScript (JS): 'https://stackoverflow.com/questions/17500704/how-can-i-set-focus-on-an-element-in-an-html-form-using-javascript/17500718#17500718'.

    else:

        UDFPrintLog(f"[ERROR] API token is not valid. Please make sure it's valid; i.e. doesn't have trailing spaces, and starts with 'pat-'.")

        #  Disables parameter fields for inputs.
        globals()['_IS_HUBSPOT_API_TOKEN_VALIDATED']    = False
        contact_first_name_html_element                 = document.querySelector('#input_contact_first_name')
        contact_first_name_html_element.disabled        = True
        contact_last_name_html_element                  = document.querySelector('#input_contact_last_name')
        contact_last_name_html_element.disabled         = True
        contact_email_html_element                      = document.querySelector('#input_contact_email')
        contact_email_html_element.disabled             = True
        create_contact_html_element                     = document.querySelector('#button_create_contact')
        create_contact_html_element.disabled            = True
        
        #  Cleans any previous entry.
        UDFSetHTMLValue(contact_first_name_html_element.id, '')
        UDFSetHTMLValue(contact_last_name_html_element.id, '')
        UDFSetHTMLValue(contact_email_html_element.id, '')
        
        api_token_html_element.focus()

    return None

#  Function to manage workflow when button with id '#button_create_contact' is clicked.
#  - NOTE: requires importing 'when' module from package 'pyscript', to add decorators.
@when("click", "#button_create_contact")
def UDFCreateContact(event) -> None:
    
    #  Get user input from the html; e.g. API token from element with id 'input_api_token'.
    api_token_html_element                  = document.querySelector('#input_api_token')

    if (not _IS_HUBSPOT_API_TOKEN_VALIDATED):
        UDFPrintLog(f"[ERROR] Please 1st validate your API token is valid.")
        api_token_html_element.focus()

    else:

        api_token                               = UDFGetHTMLValue(api_token_html_element.id)
        contact_first_name                      = ''
        contact_last_name                       = ''
        contact_email                           = ''

        #  Get user input from the html.
        contact_first_name_html_element         = document.querySelector('#input_contact_first_name')
        contact_first_name_format_validation    = UDFValidateFormatContactFirstName(contact_first_name_html_element)
        if contact_first_name_format_validation:
            contact_first_name                  = UDFGetHTMLValue(contact_first_name_html_element.id)
        #  Get user input from the html.
        contact_last_name_html_element          = document.querySelector('#input_contact_last_name')
        contact_last_name_format_validation     = UDFValidateFormatContactLastName(contact_last_name_html_element)
        if contact_last_name_format_validation:
            contact_last_name                   = UDFGetHTMLValue(contact_last_name_html_element.id)
        #  Get user input from the html.
        contact_email_html_element              = document.querySelector('#input_contact_email')
        contact_email_format_validation         = UDFValidateFormatContactEmail(contact_email_html_element)
        if contact_email_format_validation:
            contact_email                       = UDFGetHTMLValue(contact_email_html_element.id)

        #  Validate if all validations are 'True': 'https://www.w3schools.com/python/ref_func_all.asp'.
        if all([contact_first_name_format_validation, contact_last_name_format_validation, contact_email_format_validation]):
            
            # #  NOTE: not using YET, since when using it with PyScript from a client / web-browser, depending on the API (e.g. HubSpot), it could block requests and throw CORS error: 'https://developers.hubspot.com/docs/cms/reference/serverless-functions/serverless-functions#cors'.
            # #+ ALTERNATIVE: use simple PHP server for request: 'https://www.kelp.agency/blog/how-to-enable-cors-ajax-requests-for-any-hubspot-api/'.
            # new_contact_payload = {}
            # if (contact_last_name != ''):
            #     new_contact_payload = {
            #         "properties": {
            #             "email": contact_email,
            #             "firstname": contact_first_name,
            #             "lastname": contact_last_name
            #         }
            #     }
            # else:
            #     new_contact_payload = {
            #         "properties": {
            #             "email": contact_email,
            #             "firstname": contact_first_name
            #         }
            #     }
            # api_results_listing_contacts        = UDFHubSpotSendAPIRequest(
            #     IApiUrl = _HUBSPOT_API_URL,
            #     IApiUrlNode = _HUBSPOT_API_URL_NODE_CONTACTS,
            #     IApiToken = api_token,
            #     IApiPayload = new_contact_payload
            # )

            UDFPrintLog(f"[SUCCESS] Please validate execution results with previous LOG messages.")

            #  If succesful execution (at least before the HubSpot API call), it cleans input fields.
            UDFSetHTMLValue(contact_first_name_html_element.id, '')
            UDFSetHTMLValue(contact_last_name_html_element.id, '')
            UDFSetHTMLValue(contact_email_html_element.id, '')

        else:

            UDFPrintLog(f"[ERROR] At least one field is not valid. Please make sure all fields are valid; i.e. first name is not empty, email is not empty and it has a valid email format.")

        #  Set focus on contact's first name, regardless of inputs format validation being successful or not.
        contact_first_name_html_element.focus()
    
    return None

#  MAIN FUNCTION.
def main():

    #  'main()' INITIALIZATION.

    # UDFClearOutput()                            #  Clear screen. NOTE: doesn't work with PyScript in a browser.
    UDFPrintLog(f"[LOG] Initializing...")

    #  INPUTS.

    #  Main directory.

    #  Input: data.

    input_configuration_dirpat                  = '.'
    input_configuration_filenames_regex         = r'config_.*\.yaml'                 #  String literal for RegEx expresion of configuration filenames patterns; e.g. 'config_<...>.yaml': 'https://www.w3schools.com/python/python_regex.asp', 'https://regex101.com'. Files listing base variables and their structure; e.g. user timezone, column names for dataframes, etc. NOTE: all matching files will be processed the SAME WAY.

    #  INITIALIZATION.

    #  Print current working directory.
    working_directory                           = os.getcwd()
    UDFPrintLog(f"[LOG] Current working directory: '{working_directory}'.")

    #  [INITIALIZATION] PROJECT BASE STRUCTURE VALIDATION.

    # #  [DEBUG] List files and folders ONLY in current working directory.
    # UDFPrintLog(str([i for i in glob.iglob('*', recursive = True)] ))
    # #  [DEBUG] List ALL files and folders, RECURSIVELY, starting from current working directory.
    # UDFPrintLog(str([i for i in glob.iglob('*', recursive = True)] ))               # OP01.
    # UDFPrintLog(UDFSearchPaths(r'.*'))                                              # OP02.

    #  NOTE: how to access 'in-browser' filesystem files, imported via JSON config. file: 'https://docs.pyscript.net/2025.8.1/user-guide/filesystem/'.

    #  Inputs validations: searches for configuration of base variables.
    input_configuration_filepaths               = UDFSearchPaths(input_configuration_filenames_regex, input_configuration_dirpat)
    UDFPrintLog(f"[LOG] Configuration files found (x{len(input_configuration_filepaths)}): '{"' | '".join(input_configuration_filepaths)}'.")

    #  [INITIALIZATION] INPUT: CONFIGURATION FILE(S) LOAD.

    #  Load configuration YAML file.
    #  - Load '.yaml' file: 'https://www.geeksforgeeks.org/python/parse-a-yaml-file-in-python/'.
    yaml_variables_data                         = None
    yaml_variables_list                         = []

    for yaml_filepath in input_configuration_filepaths:
        with open(yaml_filepath, 'r') as file:
            yaml_variables_data = yaml.load(file, Loader = yaml.SafeLoader)
        if yaml_variables_data is not None:                                                 #  1st check YAML file is not empty.
            if yaml_variables_data['parameters'] is not None:                               #  2nd check if there is a 'parameters' section.
                yaml_variables_list             += yaml_variables_data['parameters']        #  Or also could use '<list>.extend(<other_list>)': 'https://sparkbyexamples.com/python/python-append-list-to-a-list/'.
                # print(f"[LOG] Variables imported (x{len(yaml_variables_data['parameters'])}), from '{yaml_filepath}'.")

    UDFPrintLog(f"[LOG] Variables imported in total (x{len(yaml_variables_list)}), from: '{"' | '".join(input_configuration_filepaths)}'.")

    # #  [DEBUG] List variables.
    # UDFJsonPrint(yaml_variables_list)

    #  Get a dictionary of variables from YAML file, with proper data conversion.
    yaml_variables_dictionary                   = UDFCreateVariablesDictionaryFromFormattedList(yaml_variables_list)

    # #  [DEBUG] List variables.
    # UDFJsonPrint(yaml_variables_dictionary)

    #  Load variables YAML file into globals().
    UDFLoadVariablesToGlobals(yaml_variables_dictionary)

    #  Set execution timezone.
    global _TIME_ZONE                           #  To set globally; e.g. outside 'main()': 'https://www.w3schools.com/python/python_variables_global.asp'.
    _TIME_ZONE                                  = zoneinfo.ZoneInfo(_USER_GEOGRAPHIC_TIMEZONE)

    UDFPrintLog(f"[LOG] Finished initializing.")

#  CODE EXECUTION.

#  Code executed ONLY when script is called directly; NOT IMPORTED from other script.
if __name__ == '__main__':
    main()
# EOF.