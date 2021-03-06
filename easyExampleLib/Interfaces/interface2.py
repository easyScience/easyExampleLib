__author__ = "github.com/wardsimon"
__version__ = "0.0.1"

from typing import Callable

import numpy as np
import json

from easyExampleLib.Interfaces.interfaceTemplate import InterfaceTemplate
from easyExampleLib.Calculators.calculator2 import Calculator2


class Interface2(InterfaceTemplate):
    """
    A simple example interface using Calculator2
    """
    _link = {'amplitude': 'A',
             'period':    'p',
             'x_shift':   'dx',
             'y_shift':   'dy'}
    name = 'cosine'

    def __init__(self):
        # This interface will use calculator1
        self.calculator = Calculator2()

    def get_value(self, value_label: str, external: bool) -> float:
        """
        Method to get a value from the calculator
        :param value_label: parameter name to get
        :type value_label: str
        :return: associated value
        :rtype: float
        """
        if external and value_label in self._link.keys():
            value_label = self._link[value_label]
        file_read = json.loads(self.calculator.export_data())
        return file_read.get(value_label, None)

    def set_value(self, value_label: str, value: float, external: bool):
        """
        Method to set a value from the calculator
        :param value_label: parameter name to get
        :type value_label: str
        :param value: new numeric value
        :type value: float
        :return: None
        :rtype: noneType
        """
        if self._borg.debug:
            print(f'Interface1: Value of {value_label} set to {value}')
        if external and value_label in self._link.keys():
            value_label = self._link[value_label]
        file_read = json.loads(self.calculator.export_data())
        file_read[value_label] = value
        self.calculator.import_data(json.dumps(file_read))

    def fit_func(self, x_array: np.ndarray) -> np.ndarray:
        """
        Function to perform a fit
        :param x_array: points to be calculated at
        :type x_array: np.ndarray
        :return: calculated points
        :rtype: np.ndarray
        """
        return self.calculator.calculate(x_array)

    @staticmethod
    def get_item_fn(obj, key: str) -> Callable:
        """
        Access the value of a key by a callable object
        :param key: name of parameter to be retrieved
        :type key: str
        :return: function to get key
        :rtype: Callable
        """

        def inner():
            return obj.get_value(key)

        return inner

    @staticmethod
    def set_item_fn(obj, key):
        """
        Set the value of a key by a callable object
        :param obj: object to be created from
        :type obj: InterfaceFactory
        :param key: name of parameter to be set
        :type key: str
        :return: function to set key
        :rtype: Callable
        """

        def inner(value):
            obj.set_value(key, value)

        return inner
