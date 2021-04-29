import numpy as np

from predictors.temp.aemet import aemet

#import torch


def temp_prediction():
    # Get data from AEMET database
    status, result_data = aemet.get_data_url()
    if status == 'ERROR':
        return ('ERROR', result_data, 0)
    status, maxima, minima = aemet.get_data(result_data)
    if status == 'ERROR':
        return ('ERROR', maxima, minima)
    
    return ("OK", maxima, minima)
