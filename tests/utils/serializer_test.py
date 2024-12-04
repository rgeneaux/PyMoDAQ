import numpy as np
import pytest

from pymodaq_utils.serialize.factory import SerializableFactory
from pymodaq.utils import data as data_mod


ser_factory = SerializableFactory()


def test_data_actuator_serialization_deserialization():
    dwa = data_mod.DataActuator(data=9.5)
    assert ser_factory.get_apply_deserializer(ser_factory.get_apply_serializer(dwa)) == dwa


def test_data_from_plugins_serialization_deserialization():
    dwa = data_mod.DataFromPlugins('myplug', data=[np.array([1, 2, 3])])
    dwa.create_missing_axes()
    assert ser_factory.get_apply_deserializer(ser_factory.get_apply_serializer(dwa)) == dwa
