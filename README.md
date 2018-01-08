# planet-fetch-data

A simple python script to download Planet Earth Observation Data (PlanetScope and RapidEye, asset type: 'analytic') using the Planet API and some HTTP resquests.

Use in commandline
`python PlanetDataDownloader.py \your\download\directory startdate enddate limit`

Parameters `startdate` and `enddate` have to be in `YYYY-MM-DD` format. 
`limit` is a number standing for the maximum number of files you want to retrieve.
