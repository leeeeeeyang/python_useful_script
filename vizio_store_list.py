import pandas as pd
from uszipcode import ZipcodeSearchEngine
import math



##define distance between zipcodes function

def distance(df):
    lat1, lon1 = df['latitude_mventix'], df['longitude_mventix']
    lat2, lon2 = df['latitude_uncovered'], df['longitude_uncovered']
    radius = 3956 # miles

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    return d



##import store lists and transform zipcode to 5-digit string

store_mventix = pd.read_excel('store_mventix.xlsx')
store_uncovered = pd.read_excel('store_uncovered.xlsx')

store_mventix['zip'] = store_mventix['zip'].astype(str).str.zfill(5)
store_uncovered['zip'] = store_uncovered['zip'].astype(str).str.zfill(5)


##add latitude and longitude to store list

search = ZipcodeSearchEngine()

latitude1 = []
longitude1 = []
latitude2 = []
longitude2 = []

for i in range(len(store_mventix)):
    latitude1.append(search.by_zipcode(store_mventix['zip'][i])['Latitude'])
    longitude1.append(search.by_zipcode(store_mventix['zip'][i])['Longitude'])

for i in range(len(store_uncovered)):
    latitude2.append(search.by_zipcode(store_uncovered['zip'][i])['Latitude'])
    longitude2.append(search.by_zipcode(store_uncovered['zip'][i])['Longitude'])

store_mventix['latitude'] = latitude1
store_mventix['longitude'] = longitude1
store_uncovered['latitude'] = latitude2
store_uncovered['longitude'] = longitude2

##join covered and uncovered store lists

covered_uncovered = pd.merge(store_mventix, store_uncovered, on=['district', 'rank'])

store_list = covered_uncovered[['district','rank','coverage_x','store_id_x','full_address_x','zip_x','latitude_x','longitude_x',\
                                'coverage_y','store_id_y','full_address_y','zip_y','latitude_y','longitude_y']]

store_list.columns = ['district','rank','coverage_mventix','store_id_mventix','full_address_mventix','zip_mventix','latitude_mventix','longitude_mventix',\
                      'coverage_uncovered','store_id_uncovered','full_address_uncovered','zip_uncovered','latitude_uncovered','longitude_uncovered']


##add distance column to dataframe

store_list['distance'] = store_list.apply(distance, axis = 1)

store_list = store_list[store_list.distance < 50]


uncovered_store_list = pd.DataFrame({'num_mventix_stores_around': store_list.groupby(['coverage_uncovered','store_id_uncovered','full_address_uncovered','zip_uncovered',\
                                           'latitude_uncovered','longitude_uncovered']).size()}).reset_index()
print(uncovered_store_list.head())
print(uncovered_store_list.shape)
####
####store_list.to_csv('vizio_store_list.csv')










