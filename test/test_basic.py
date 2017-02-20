from res_light.res_light import Category, ResLight, LightDatum, LightData
from res_light.estimate_energy import _region
import pytest

def test_region():
    with pytest.raises(Exception):
        _region("", "", "Census Division")
    assert _region("19143", "PA", "Census Division") == "02. Middle Atlantic"
    assert _region("", "CA", "Census Division") == "10. Pacific"
    assert _region("77001", "", "Census Division") == "07. West South Central"
    assert _region("19143", "PA", "Census Region") == "1. Northeast"
    assert _region("", "CA", "Census Region") == "4. Pacific"
    assert _region("77001", "", "Census Region") == "3. South"

def test_category_list():
    master = Category("Master")
    child1 = master.add(Category("child1"))
    child2 = master.add(Category("child2"))
    child3 = child1.add(Category("child3"))
    child4 = child1.add(Category("child4"))
    child5 = child2.add(Category("child5"))
    assert master.category_list(0) == [master]
    assert master.category_list(1) == [child1, child2]
    assert master.category_list(2) == [child3, child4, child5]
    
