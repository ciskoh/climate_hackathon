from datetime import datetime as dt, timedelta
import requests
from pathlib import Path
import json
import os


TOKEN="35eb1ab686210d5a7f51c3ef17ab9a4b"
def create_polygon(geometry, name, token):
    #geometry : the polygon geometry given as a GEOjson
    #token : key token for Agro API account (account is free up to 1000 ha)
    #This function returns the id number of the created polygon
    response_creation = requests.post(
    url = f'http://api.agromonitoring.com/agro/1.0/polygons?appid={token}',
    headers={'Content-Type': 'application/json'},
    json = {'name': name,
            'appid': token,
            'geo_json':{
                'type': 'FeatureCollection',
                'features':[
                    {'type':'Feature',
                        'properties':{},
                        'geometry': geometry
                    }]}})
    return response_creation.json()['id']


def get_AgroAPI_GEOtiff(polygonID, start, end, imagedProperty, token):
    #polygonID : The ID of the polygon saved on the Agro API account as string
    #start : Start date of period in format datetime(int year, int month, int day, tzinfo=timezone.utc)
    #end : End date of period in format datetime(int year, int month, int day, tzinfo=timezone.utc)
    #imagedProperty : Selects which property to plot, ex. 'ndvi'
    #token : key token for Agro API account (account is free up to 1000 ha) as string

    response = requests.get(
        url = f'http://api.agromonitoring.com/agro/1.0/image/search?start={start.timestamp()}&end={end.timestamp()}&polyid={polygonID}&appid={token}'
    )
    if not response.status_code == 200:
        print(f"problem retrieving file from the link!")
        return None

    for index in range(0,len(response.json())):
        image = requests.get(url = response.json()[index]['data'][imagedProperty])

        # set output filename
        timestamp = dt.utcfromtimestamp(response.json()[index]['dt'])
        timestamp = timestamp.isoformat()
        satellite = response.json()[index]['type']
        print("timestamp:", timestamp)
        out_file = Path("AgroAPIimages", satellite+'_'+timestamp[0:10]+".tiff")
        print("outfile:", out_file)

        with open(out_file, "wb") as f:
                f.write(image.content)
        return out_file

def download_dataset_AgroAPI(aoi_path, imagedProperty="ndvi", token=None):

    # get coordinates
    with open(aoi_path) as f:
        coords = json.load(f)
    coords_list = coords['features']

    # get date range
    end_date = dt.now()
    start_date = end_date - timedelta(days=365)
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")

    # cycle through polygones
    for n, c_dict in enumerate(coords_list):
        c = c_dict["geometry"]["coordinates"][0]
        print(f" \n downloading agroAPI data for area {n}")
        polyID = create_polygon(c, "aoi", token)
        out_file = get_AgroAPI_GEOtiff(polyID, start_date, end_date, imagedProperty, token )
        if os.path.exists(out_file):
            print(f"downloaded {imagedProperty} file in location: {out_file}")
            return out_file
        else:
            raise FileNotFoundError

if __name__ == '__main__':
    token = TOKEN
    aoi_path = str(Path("..", "..", "data", "raw", "test_aoi_valencia.geojson"))
    download_dataset_AgroAPI(aoi_path, "ndvi", token)