import res_light
import zipcode

def estimate_energy(attributes):
    """ 
    Estimates energy use given a dictionary of attributes.
    attributes:
      zip:       (int/string) indicates zip code of residence
      state:     (string) indicates state for household
      region:    (string) indicates region for household
      room:      (string) specifies room to estimate energy. If blank, 
                 whole residence is assumed
      month:     (string) month to get energy for. If blank, yearly 
                 energy assumed
      size:      (string) indicates size of house. "small", "medium", 
                 or "large"
      num_baths: (int) number of bathrooms. Used as proxy for house size
      num_beds"  (int) number of bedrooms. Used as proxy for house size
    """
    return
