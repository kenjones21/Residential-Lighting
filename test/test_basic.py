from res_light.res_light import Category

def test_1():
    test_cat = Category("test")
    assert test_cat.name == "test"

"""
r = ResLight('../Data/reslight_DOE_2012.xlsx', 'DOE')
search = ["Census Division", "01. New England", "bathrooms", "0 to 1"]
retrieved = r.light_data.get(search)
print(retrieved.attributes)
"""
