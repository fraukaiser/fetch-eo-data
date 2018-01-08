#-------------------------------------------------------------------------------
# Name:        Filter Planet Data  V02 (sleep loop for activation)
# Purpose:
#
# Author:      skaiser
#
# Created:     05.01.2018
# Copyright:   (c) skaiser 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------
# the geo json geometry object we got from geojson.io

from planet import api
import sys
import os
import requests
import time

apikey = os.getenv('PLANET_API_KEY')

ddir = str(sys.argv[1])
sdate = str(sys.argv[2])
edate = str(sys.argv[3])
limit = int(sys.argv[4])

##ddir = 'C:\Users\skaiser\Downloads'


client = api.ClientV1(api_key= apikey)


####
## Define data specifications
####
# geometry
aoi = {
        "type": "Polygon",
        "coordinates": [
          [
            [
              -148.97048950195312,
              70.14456261942247
            ],
            [
              -148.282470703125,
              70.14456261942247
            ],
            [
              -148.282470703125,
              70.41333338476161
            ],
            [
              -148.97048950195312,
              70.41333338476161
            ],
            [
              -148.97048950195312,
              70.14456261942247
            ]
          ]
        ]
      }


ubicacion = api.filters.geom_filter(aoi)

# product type
item_type = ["PSScene4Band", "REOrthoTile"]
##item_type = 'PSScene4Band'
asset_type = 'analytic'                 # can be analytic, analytic_xml, udm, visual, visual_xml
                                        # for reference see https://www.planet.com/docs/api-quickstart-examples/step-2-download/

# date range

date_range_filter = {
  "type": "DateRangeFilter",
  "field_name": "acquired",
  "config": {
    "gte": "%sT00:00:00.000Z" %(sdate),
    "lte": "%sT00:00:00.000Z" %(edate)
  }
}


# cloud cover

cloud_cover_filter = {
  "type": "RangeFilter",
  "field_name": "cloud_cover",
  "config": {
    "lte": 0.05
  }
}

PB_filter = {
    "type": "AndFilter",
    "config": [date_range_filter, cloud_cover_filter, ubicacion]
}

# setup auth
session = requests.Session()
session.auth = (apikey, '')

####
## Post request
####

for i in item_type:
    request = api.filters.build_search_request(PB_filter, [i], name = None, interval= 'day')
    results = client.quick_search(request)
    print i
    for item in results.items_iter(limit):
        print item['id']
        dataset = \
            session.get(
                ("https://api.planet.com/data/v1/item-types/" +
                "{}/items/{}/assets/").format(i, item['id']))
        # extract the activation url from the item for the desired asset
        item_activation_url = dataset.json()[asset_type]["_links"]["activate"]
        # request activation
        response = session.post(item_activation_url)
        print response.status_code
        while response.status_code!=204:
            time.sleep(30)
            response = session.post(item_activation_url)
            response.status_code = response.status_code
            print response.status_code
    ##        assets = client.get_assets(item).get()
    ##        print('activating asset')
    ##        activation = client.activate(assets[asset_type])
    ##        # wait for it
        assets = client.get_assets(item).get()
        callback = api.write_to_file(directory=ddir, callback= None, overwrite= True)
        body = client.download(assets[asset_type], callback=callback)
        body.await()


##("https://api.planet.com/data/v1/item-types/" + "{}/items/{}/assets/").format(item_type, item['id'])

