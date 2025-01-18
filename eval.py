import numpy as np

class EvaluateMode:
    def __init__(self):
        pass

    def mean_absolute_percentage_error(y_true, y_pred):
        return 100 * np.mean(np.abs((y_true - y_pred) / y_true))
