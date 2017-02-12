import os
from openpyxl import load_workbook
class ResLight:
    def __init__(self, full_filename, source):
        if source is "DOE":
            filename, extension = os.path.splitext(full_filename)
            if extension != ".xlsx":
                raise Exception("DOE files must be in xlsx format")
            print("Loading workbook...", end="", flush=True)
            wb = load_workbook(full_filename)
            print("Done")
            tool = wb.get_sheet_by_name("C) Tool")
            self.light_data = []
            for row in tool["A3:A16197"]: #16197
                attributes = {}
                for cell in row:
                    col = cell.column
                    if col is "A" or col is "B" or col is "C" or col is "D":
                        category = tool[col + "2"].value
                        attributes[category] = str(cell.value)
                    else:
                        category = tool[col + "2"].value
                        attributes[category] = cell.value
                light_datum_temp = LightDatum(attributes)
                self.light_data.append(light_datum_temp)
            print(len(self.light_data))
        else:
            raise Exception("Only DOE files accepted at this time")

class LightDatum:
    def __init__(self, attributes):
        self.attributes = attributes
        

r = ResLight('../Data/reslight_DOE_2012.xlsx', 'DOE')
        
