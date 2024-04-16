from pycloudevents import CloudEvent


def test_get_unbound_variable_from_empty_extensions():
    data = {
        "id": "12345",
        "specversion": "1.0",
        "type": "com.cloudevents.example.extension",
        "source": "https://example.com/source",
        "data": {"message": "Hello, world!"},
    }

    cloudevent = CloudEvent.from_dict(data)
    assert cloudevent.foo is None
