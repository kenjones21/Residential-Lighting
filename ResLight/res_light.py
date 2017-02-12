import os
from openpyxl import load_workbook
class ResLight:
    def __init__(self, full_filename, source):
        if source is "DOE":
            filename, extension = os.path.splitext(full_filename)
            print(extension)
            if extension != ".xlsx":
                raise Exception("DOE files must be in xlsx format")
            wb = load_workbook(full_filename)
            print(wb.get_sheet_names())

r = ResLight('../Data/reslight_DOE_2012.xlsx', 'DOE')
        
