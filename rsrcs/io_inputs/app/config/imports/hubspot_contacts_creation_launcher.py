# #  Code that ALWAYS get executed; either main, or imported as module from other script.
# print(__name__)
# print("---")

#  LIBRARIES / PACKAGES IMPORTS.

from js import console                      #  Allows usage of 'console.log()' function from JavaScript (JS).
from pyscript import when                   #  [PyScript] Allows usage of 'pyscript.when' decorator for Python functions, to handle events: 'https://docs.pyscript.net/2024.8.1/api/#pyscriptwhen'.
from pyscript import document               #  [PyScript] To manage html elements, via DOM: 'https://docs.pyscript.net/2024.8.1/api/#pyscriptdocument'.
# from pyscript import display                #  [PyScript] Displays content, using in-function intelligence for proper display: 'https://docs.pyscript.net/2024.8.1/api/#pyscriptdisplay'.

#  Function to print LOG in both environments: Python, and browser console, via JS.
#  - IMPORTANT: requires import package 'js' ('console' module), to print in console.
def UDFPrintLog(IMessage: str) -> None:
    
    #  Prints log in Python console.
    print(IMessage)
    #  Prints log in JS console.
    console.log(IMessage)

    return None

@when("click", "#button_validate_api_token")
def UDFTest(event) -> None:
    UDFPrintLog("[LOG] Testing...")
    return None

# #  Function to manage workflow when button with id '#button_create_contact' is clicked.
# #  - IMPORTANT: requires import package 'pyscript' ('when' module), to add decorators.
# @when("click", "#button_create_contact")
# def UDFLoadFromURL(event) -> None:

#     page["#pyscript_output_dataset_table"][0].innerHTML                     = ""                                        #  Clears any previous result.
#     input_dataset_url                                                       = page["#input_dataset_url"][0].value       #  Gets input value (not the 'innerHTML').

#     UDFPrintLog(f"[LOG] Fetching data from: '{input_dataset_url}'.")
#     dataset_dataframe = pd.read_csv(open_url(input_dataset_url))                                                        #  Reads pandas dataframe, by firstly parsing the provided URL.

#     #  Make visible pyscript output sections of dataset and console log. Elements used are 'div's, with 'display' property INITIALLY set to 'none' (or 'hidden' via direct property).
#     #  - Ref.: 'https://www.w3schools.com/css/css_display_visibility.asp'.
#     page["#pyscript_output_dataset_section"][0].style["display"]            = "block"
#     page["#pyscript_output_console_log_section"][0].style["display"]        = "block"

#     display(dataset_dataframe, target = "pyscript_output_dataset_table", append = "False")                              #  INJECTS the dataframe in the 'innerHTML' of the target element. With 'append="False"', it REPLACES any previous content there might be, instead of appending it with 'div's if using 'append="True"' (DEFAULT, if ommitted).

# #  MAIN FUNCTION.
# def main():

#     page_message                                                = "This example loads a remote CSV file into a Pandas dataframe, and displays it."
#     input_dataset_url_default                                   = "https://raw.githubusercontent.com/datasets/airport-codes/master/data/airport-codes.csv"

#     #  Set 'DEFAULT' values, via DOM:
#     page["#pyscript_output_page_message"][0].innerHTML          = page_message                      #  Since using a no-self closing element; e.g. 'div', content is placed as 'innerHTML'.
#     page["#input_dataset_url"][0].value                         = input_dataset_url_default         #  BE CAREFUL! Since using a self-closing element; e.g. 'input', content is set to its value, not using 'innerHTML'. The latter will return empty; i.e. ''.

# #  CODE EXECUTION.

# #  Code executed ONLY when script is called directly; NOT IMPORTED from other script.
# if __name__ == '__main__':
#     main()

# ---

# def translate_english(event):
#     #  Get text from HTML element with id = '#english'.
#     input_text = document.querySelector('#english')
#     english = input_text.value
#     #  Set text fo HTML element with id = '#output'.
#     output_div = document.querySelector('#output')
#     output_div.innerText = arrr.translate(english)

# input_text = document.querySelector('input_api_token')
# input_text = document.querySelector('input_user_name')
# input_text = document.querySelector('input_user_last_name')
# input_text = document.querySelector('input_user_email')
# input_text = document.querySelector('output_contacts')
# input_text = document.querySelector('output_log')
