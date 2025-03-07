
import pytest

from pymodaq.control_modules.daq_move import DataActuator

from pymodaq.utils.leco.utils import serialize_object, binary_serialization, binary_serialization_to_kwargs


@pytest.mark.parametrize("value", (
        5,
        6.7,
        "some value",
))
def test_native_json_object(value):
    assert serialize_object(value) == value


def test_data_actuator():
    value = DataActuator(data=10.5)
    serialized = serialize_object(value)
    assert isinstance(serialized, str)
    # with Serializer
    # expected = "AAAADERhdGFBY3R1YXRvcgAAAAM8ZjgAAAAIc8Pcmx7U2UEAAAAIYWN0dWF0b3IAAAADcmF3AAAABkRhdGEwRAAAAAd1bmlmb3JtAAAAAQAAAAVhcnJheQAAAAM8ZjgAAAAIAAAAAQAAAAEAAAAAAAAlQAAAAAAAAAABAAAABnN0cmluZwAAAARDSDAwAAAAAAAAAAAAAAAAAAAAAAAAAAA="
    # with Serializer Factory
    expected = "AAAADERhdGFBY3R1YXRvcgAAAAVmbG9hdAAAAAM8ZjgAAAAIYGa0OSDU2UEAAAADc3RyAAAACGFjdHVhdG9yAAAAA3N0cgAAAANyYXcAAAADc3RyAAAABkRhdGEwRAAAAANzdHIAAAAHdW5pZm9ybQAAAARsaXN0AAAAAQAAAAduZGFycmF5AAAAAzxmOAAAAAgAAAABAAAAAQAAAAAAACVAAAAAA3N0cgAAAAAAAAAEbGlzdAAAAAEAAAADc3RyAAAABENIMDAAAAADc3RyAAAAAAAAAARsaXN0AAAAAAAAAARsaXN0AAAAAAAAAARsaXN0AAAAAAAAAARsaXN0AAAAAA=="
    # test before and after timestamp
    assert serialized[:30] == expected[:30]
    assert serialized[64:] == expected[64:]


@pytest.mark.parametrize("value", (
        5,
        6.7,
        "some value",
))
def test_native_json_object_binary_serialization(value):
    serialized_tuple = binary_serialization(value)
    assert serialized_tuple[1] is None
    assert serialized_tuple[0] == value


def test_binary_serialization():
    value = DataActuator(data=10.5)
    serialized_tuple = binary_serialization(value)
    assert serialized_tuple[0] is None
    content = serialized_tuple[1][0]  # type: ignore
    assert isinstance(content, bytes)
    # content at one point in time:
    expected = b"\x00\x00\x00\x0cDataActuator\x00\x00\x00\x05float\x00\x00\x00\x03<f8\x00\x00\x00\x08\x890\x82\x91\x1e\xd4\xd9A\x00\x00\x00\x03str\x00\x00\x00\x08actuator\x00\x00\x00\x03str\x00\x00\x00\x03raw\x00\x00\x00\x03str\x00\x00\x00\x06Data0D\x00\x00\x00\x03str\x00\x00\x00\x07uniform\x00\x00\x00\x04list\x00\x00\x00\x01\x00\x00\x00\x07ndarray\x00\x00\x00\x03<f8\x00\x00\x00\x08\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00%@\x00\x00\x00\x03str\x00\x00\x00\x00\x00\x00\x00\x04list\x00\x00\x00\x01\x00\x00\x00\x03str\x00\x00\x00\x04CH00\x00\x00\x00\x03str\x00\x00\x00\x00\x00\x00\x00\x04list\x00\x00\x00\x00\x00\x00\x00\x04list\x00\x00\x00\x00\x00\x00\x00\x04list\x00\x00\x00\x00\x00\x00\x00\x04list\x00\x00\x00\x00"
    # test part before and after timestamp, as timestamp varies
    assert content[:25] == expected[:25]
    assert content[48:] == expected[48:]


def test_binary_serialization_to_kwargs_simple():
    data = binary_serialization_to_kwargs(6.7)
    assert data == {"data": 6.7, "additional_payload": None}
