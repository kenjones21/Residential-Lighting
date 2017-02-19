import res_light
import zipcode

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
    if "zip" in attributes:
        zipc = zipcode.isequal(attributes["zip"])
        if "state" in attributes:
            if zipc.state != attributes["state"]:
                raise Exception("State does not match zip")
        if "region" in attributes:
            if _region(zipc.state) != attributes["region"]:
                raise Exception("Zip does not match region")
    if "partition" in attributes:
        partition = attributes["partition"]
    else:
        partition = "Census Division"
    region = _region(zipc.state, partition)
    
        
def _region(state, partition):
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
        elif state in ["ID", "MT", "WY"]: #Just a guess. Can't find info on "mountain north"
            return "08. Mountain North"
        elif state in ["NV", "UT", "CO", "AZ", "NM"]:
            return "09. Mountain South"
        elif state in ["CA", "AK", "OR", "WA", "HI"]:
            return "10. Pacific"
        else:
            raise Exception("State not in a census region")

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
