"""This file provides a simple implementation of scipy.signal.convolve2d with mode
"""
import numpy as np
from numpy.lib.stride_tricks import as_strided

data = np.arange(30).reshape(6, 5)
kernel = np.eye(3)


def extrude_for_convolution(data, kernel):
    # Indices of the top left corner of the last window.
    last_row = data.shape[0] - (kernel.shape[0])
    last_col = data.shape[1] - (kernel.shape[1])

    num_windows = last_row * data.shape[1] + last_col + 1

    shape = (num_windows,) + kernel.shape
    strides = (data.strides[1],) + data.strides

    windows = as_strided(data, shape=shape, strides=strides)
    valid = np.arange(num_windows) % data.shape[1] <= last_col

    return windows, valid


def convolve_2d(data, kernel):
    windows, valid = extrude_for_convolution(data, kernel)

    # A 1D array containing the results of multiplying each window by the
    # convolution kernel.
    multiplication_results = np.tensordot(windows, kernel)[valid]

    return multiplication_results.reshape(data.shape[0] - kernel.shape[0] + 1,
                                          data.shape[1] - kernel.shape[1] + 1)
