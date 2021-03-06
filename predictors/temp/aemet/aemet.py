import requests
import urllib3
from flask import json

import globals

aemet_key =  "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJkaWVnb0BlbmNvcmUtbGFiLmNvbSIsImp0aSI6Ijc5ZDE1MmRjLWIwMzQtNDhkMS1hMjUwLTRmNzQ1ZTUwOGFkOSIsImlzcyI6IkFFTUVUIiwiaWF0IjoxNTY4Mjg0NzE1LCJ1c2VySWQiOiI3OWQxNTJkYy1iMDM0LTQ4ZDEtYTI1MC00Zjc0NWU1MDhhZDkiLCJyb2xlIjoiIn0._WCWYvR1V39OM0PfC8jmLPvA8zNWgtMSYid3nKQzBYY"

def get_data_url():
    # Para solucionar el problema de dh_key_too_small
    # https://stackoverflow.com/questions/38015537/python-requests-exceptions-sslerror-dh-key-too-small
    
    
    requests.packages.urllib3.disable_warnings()
    requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += 'HIGH:!DH:!aNULL'
    try:
        requests.packages.urllib3.contrib.pyopenssl.DEFAULT_SSL_CIPHER_LIST += 'HIGH:!DH:!aNULL'
    except AttributeError:
        # no pyopenssl support used / needed / available
        pass
    
    response_aemet = requests.get('https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/diaria/' + str(globals.MUNICIPIO), headers={"Accept": "application/json", "api_key" : aemet_key }, verify=False)
    if not response_aemet.ok:
        return ("ERROR", "AEMET API is not working")

    data_url = json.loads(response_aemet.text)["datos"]
    #print(data_url)s
    return("OK", data_url)

def get_data(url):
    requests.packages.urllib3.disable_warnings()
    requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += 'HIGH:!DH:!aNULL'
    try:
        requests.packages.urllib3.contrib.pyopenssl.DEFAULT_SSL_CIPHER_LIST += 'HIGH:!DH:!aNULL'
    except AttributeError:
        # no pyopenssl support used / needed / available
        pass
    data = requests.get(url, verify=False)
    if not data.ok:
        return ("ERROR", "AEMET data is not working")

    # extract data
    data = json.loads(data.text)
    data = data[0]
    #data0 = data['prediccion']['dia'][0]
    maxima = float(data['prediccion']['dia'][1]['temperatura']['maxima'])
    minima = float(data['prediccion']['dia'][1]['temperatura']['minima'])

   
    return ("OK", maxima, minima)








    return("OK", data.text)
