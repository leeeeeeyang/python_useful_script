from geopy.geocoders import Nominatim
import pandas as pd
from geopy.exc import GeocoderTimedOut

store_list = pd.read_csv('covered_store_list.csv')


def do_geocode(address):
    try:
        return geolocator.geocode(address)
    except GeocoderTimedOut:
        return do_geocode(address)

geolocator = Nominatim()
location = do_geocode("15 Us Highway 9, Manalapan, NJ 07726")
print(location)

geopy_address = []

for i in range(len(store_list)):
    location = do_geocode(store_list.full_address_mventix[i])
    if location is None:
        geopy_address.append('None')
    else:
        geopy_address.append(location.address)
            
store_list['geopy_address'] = geopy_address
store_list.to_csv('test.csv')
