import numpy as np

def calculate_mse(predictions, actual):
    return np.mean((np.array(predictions) - np.array(actual)) ** 2)

def calculate_rmse(predictions, actual):
    return np.sqrt(calculate_mse(predictions, actual))

def calculate_mape(predictions, actual):
    actual, predictions = np.array(actual), np.array(predictions)
    return np.mean(np.abs((actual - predictions) / actual)) * 100