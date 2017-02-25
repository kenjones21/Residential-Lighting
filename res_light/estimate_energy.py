from .data import ResLight
import zipcode
import pkg_resources

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
    filename = pkg_resources.resource_filename("res_light", "data/reslight_DOE_2012.xlsx")
    rl = ResLight(filename, "DOE")
    recs_domains = rl.light_data.data.get_child("RECS Domain").category_list(1)
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
            
        region = _region("", zipc.state, partition, recs_domains)
        
    elif "state" in attributes:
        if "region" in attributes:
            state = attributes["state"]
            region2 = _region("", state, partition, RECS_Domains)
            if region != region2:
                raise Exception("State does not match region")
            
    else:
        region = "National"
            
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
        for cat in RECS_Domains:
            states = cat.name.split()
            if state in states:
                return cat.name
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
