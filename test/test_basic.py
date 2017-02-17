from .context import res_light

r = ResLight('../Data/reslight_DOE_2012.xlsx', 'DOE')
search = ["Census Division", "01. New England", "bathrooms", "0 to 1"]
retrieved = r.light_data.get(search)
print(retrieved.attributes)
