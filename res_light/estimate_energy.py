from .data import ResLight
import zipcode
import pkg_resources

if (not "_rl" in globals()):
    filename = pkg_resources.resource_filename("res_light", "data/reslight_DOE_2012.xlsx")
    _rl = ResLight(filename, "DOE") # TODO: Do this in init

def estimate_energy(attributes):
    """ 
    Estimates energy use given a dictionary of attributes.
    attributes:
      zip:       (int/string) indicates zip code of residence
      state:     (string) indicates state for household. Use initials
      region:    (string) indicates region for household
      room:      (string) specifies room to estimate energy. If blank, 
                 whole residence is assumed
      month:     (string) month to get energy for. If blank, yearly 
                 energy assumed
      size:      (string) indicates size of house. "small", "medium", 
                 or "large"
      num_baths: (int) number of bathrooms. Used as proxy for house size
      num_beds"  (int) number of bedrooms. Used as proxy for house size
      partition: (string) partition method for country. Census Division, 
                 Census Region, RECS
    """

    partition, region = _partition_region(attributes)
    char_partition, char = _partition_char(attributes)
    categories = [partition, region, char_partition, char]

    # Categories are defined; retrieve data
    datum = _rl.light_data.get(categories)
    if "month" not in attributes:
        return datum.attributes["Daily Energy Consumption per Household (Wh)"]
    else:
        # Use montly HOU estimates to guess at energy usage
        HOU_per_lamp = estimate_HOU(attributes)
        num_lamps = datum.attributes["Number of Lamps \nper Household"]
        lamp_power = datum.attributes["Lamp Power (Watts)"]
        return HOU_per_lamp * num_lamps * lamp_power

def estimate_HOU(attributes):
    partition, region = _partition_region(attributes)
    char_partition, char = _partition_char(attributes)
    categories = [partition, region, char_partition, char]
    datum = _rl.light_data.get(categories)
    if "month" not in attributes:
        return datum.attributes["Daily HOU per Lamp"]
    else:
        month_str = attributes["month"][:3].capitalize()
        month_str += " Daily HOU per Lamp"
        return datum.attributes[month_str]
            
def _region(zipstring, state, partition, RECS_Domains=[]):
    if zipstring != "":
        zipc = zipcode.isequal(zipstring) # Initialize zipcode object if we have it
    if zipstring == "" and state == "": # If neither, raise exception
        raise Exception("Need either state or zipstring to return region")
    if zipstring != "" and state != "": # If both, check for equal
        if zipc.state != state:
            raise Exception("State does not match zip")
        else:
            working_state = state # Doesn't matter which we pull from
    elif zipstring != "": # If only zipstring, get state string
        working_state = zipc.state
    else: # If only state, copy to working_state
        working_state = state
    print(working_state)
    return _state_to_region(working_state, partition, RECS_Domains)
    
def _state_to_region(state, partition, RECS_Domains):
    if partition == "Census Division":
        if state in ["ME", "NH", "VT", "MA", "CT", "RI"]:
            return "01. New England"
        elif state in ["NY", "PA", "NJ"]:
            return "02. Middle Atlantic"
        elif state in ["WI", "MI", "IL", "IN", "OH"]:
            return "03. East North Central"
        elif state in ["ND", "SD", "NE", "KS", "MN", "IA", "MO"]:
            return "04. West North Central"
        elif state in ["MD", "DE", "VA", "WV", "VA", "NC", "SC", "GA", "FL"]:
            return "05. South Atlantic"
        elif state in ["KY", "TN", "MS", "AL"]:
            return "06. East South Central"
        elif state in ["TX", "OK", "AR", "LA"]:
            return "07. West South Central"
        elif state in ["ID", "MT", "WY"]: # Guess. Can't find info on "mountain north"
            return "08. Mountain North"
        elif state in ["NV", "UT", "CO", "AZ", "NM"]:
            return "09. Mountain South"
        elif state in ["CA", "AK", "OR", "WA", "HI"]:
            return "10. Pacific"
        else:
            raise Exception("State not in a census region")

    elif partition == "Census Region":
        if state in ["ME", "NH", "VT", "MA", "CT", "RI", "NY", "PA", "NJ"]:
            return "1. Northeast"
        elif state in ["WI", "MI", "IL", "IN", "OH", "ND", "SD",
                       "NE", "KS", "MN", "IA", "MO"]:
            return "2. Midwest"
        elif state in ["KY", "TN", "MS", "AL", "TX", "OK", "AR", "LA", "MD",
                       "DE", "VA", "WV", "VA", "NC", "SC", "GA", "FL"]:
            return "3. South"
        elif state in ["ID", "MT", "WY", "NV", "UT", "CO", "AZ", "NM",
                       "CA", "AK", "OR", "WA", "HI"]:
            return "4. Pacific"
        else:
            raise Exception("State not in a census division")

    elif partition == "RECS Domain":
        if RECS_Domains == []:
            raise Exception("RECS_Domains not provided")
        for name in RECS_Domains:
            states = name.split()
            if state in states:
                return name
        raise Exception("State not in a RECS Domain")
    
def _to_initials(state):
    states = {
        'Alaska': 'AK',
        'Alabama': 'AL',
        'Arkansas': 'AR',
        'American Samoa': 'AS',
        'Arizona': 'AZ',
        'California': 'CA',
        'Colorado': 'CO',
        'Connecticut': 'CT',
        'District of Columbia': 'DC',
        'Delaware': 'DE',
        'Florida': 'FL',
        'Georgia': 'GA',
        'Guam': 'GU',
        'Hawaii': 'HI',
        'Iowa': 'IA',
        'Idaho': 'ID',
        'Illinois': 'IL',
        'Indiana': 'IN',
        'Kansas': 'KS',
        'Kentucky': 'KY',
        'Louisiana': 'LA',
        'Massachusetts': 'MA',
        'Maryland': 'MD',
        'Maine': 'ME',
        'Michigan': 'MI',
        'Minnesota': 'MN',
        'Missouri': 'MO',
        'Northern Mariana Islands': 'MP',
        'Mississippi': 'MS',
        'Montana': 'MT',
        'National': 'NA',
        'North Carolina': 'NC',
        'North Dakota': 'ND',
        'Nebraska': 'NE',
        'New Hampshire': 'NH',
        'New Jersey': 'NJ',
        'New Mexico': 'NM',
        'Nevada': 'NV',
        'New York': 'NY',
        'Ohio': 'OH',
        'Oklahoma': 'OK',
        'Oregon': 'OR',
        'Pennsylvania': 'PA',
        'Puerto Rico': 'PR',
        'Rhode Island': 'RI',
        'South Carolina': 'SC',
        'South Dakota': 'SD',
        'Tennessee': 'TN',
        'Texas': 'TX',
        'Utah': 'UT',
        'Virginia': 'VA',
        'Virgin Islands': 'VI',
        'Vermont': 'VT',
        'Washington': 'WA',
        'Wisconsin': 'WI',
        'West Virginia': 'WV',
        'Wyoming': 'WY'
    }
    return states[state]

def _beds_to_str(num_beds_int):
    if num_beds_int == 0 or num_beds_int == 1:
        return "0 to 1"
    elif num_beds_int == 2 or num_beds_int == 3:
        return "2 to 3"
    elif num_beds_int >= 4:
        return "4 or more"
    else:
        raise Exception("num_beds_int is not a valid integer")

def _baths_to_str(num_baths_int):
    if num_baths_int == 0 or num_baths_int == 1:
        return "0 to 1"
    elif num_baths_int == 2:
        return "2"
    elif num_baths_int >=3:
        return "3 or more"
    else:
        raise Exception("num_baths_int is not a valid integer")

def _partition_region(attributes):
    recs_domains = _rl.light_data.data.get_child("RECS Domain").category_list(1)
    recs_names = []
    for cat in recs_domains:
        recs_names.append(cat.name)
    if "partition" in attributes:
        partition = attributes["partition"]
    else:
        partition = "RECS Domain" # Use most specific partitioning
    if "zip" in attributes:
        zipc = zipcode.isequal(attributes["zip"])

        if "state" in attributes:
            if zipc.state != attributes["state"]:
                raise Exception("State does not match zip")
            
        if "region" in attributes:
            if _region(zipc.state) != attributes["region"]:
                raise Exception("Zip does not match region")
            
        region = _region("", zipc.state, partition, recs_names)
        
    elif "state" in attributes:
        if "region" in attributes:
            state = attributes["state"]
            region2 = _region("", state, partition, recs_names)
            if region != region2:
                raise Exception("State does not match region")
            
    else:
        region = "National"
        partition = "National" # Reset partition in case it was not set explicitly

    return partition, region

def _partition_char(attributes):
    if "size" in attributes:
        if "num_baths" in attributes or "num_beds" in attributes:
            raise Exception("Only one of size, num_baths, or num_beds is accepted")
        size = attributes["size"]
        if size == "small":
            num_beds = "0 to 1"
        elif size == "medium":
            num_beds = "2 to 3"
        elif size == "large":
            num_beds = "4 or more"
        else:
            raise Exception("Size must be small, medium, or large")
        if "room" not in attributes:
            char_partition = "bedrooms"
            char = num_beds
        else:
            room = attributes["room"]
            if not _is_valid_room(room):
                raise Exception("Room is invalid")
            char_partition = "bedrooms space"
            char = num_beds + ", " + room # Assume room is ok. TODO: Check
    elif "num_beds" in attributes:
        if "num_baths" in attributes:
            raise Exception("Only one of num_baths or num_beds is accepted")
        num_beds = _beds_to_str(attributes["num_beds"])
        if "room" not in attributes:
            char_partition = "bedrooms"
            char = num_beds
        else:
            room = attributes["room"].capitalize()
            if not _is_valid_room(room):
                raise Exception("Room is invalid")
            char_partition = "bedrooms space"
            char = num_beds + ", " + room # Assume room is ok. TODO: Check
    elif "num_baths" in attributes:
        num_baths = _baths_to_str(attributes["num_baths"])
        if "room" not in attributes:
            char_partition = "bathrooms"
            char = num_baths
        else:
            room = attributes["room"]
            if not _is_valid_room(room):
                raise Exception("Room is invalid")
            char_partition = "bathrooms space"
            char = num_baths + ", " + room # Assume room is ok. TODO: Check
    return char_partition, char

def _is_valid_room(room):
    rooms = ["Bathroom", "Bedroom", "Dining Room", "Exterior", "Garage", "Hallway",
             "Kitchen", "Living Room", "Office", "Other Room"]
    return room in rooms
