from copy import deepcopy
from datetime import datetime
import json
from typing import Any, Dict, Hashable, Mapping, Optional


class CloudEvent:
    def __init__(
        self,
        *,
        id: str,
        source: str,
        specversion: str = "1.0",
        type: str,
        datacontenttype: Optional[str] = None,
        dataschema: Optional[str] = None,
        subject: Optional[str] = None,
        time: Optional[datetime] = None,
        data: Any = None,
        **extensions: Hashable,
    ) -> None:
        """
        Initialize the class with the provided parameters.

        Parameters:
            id (str): The identifier for the object.
            source (str): The source of the object.
            specversion (str): The specification version (default is "1.0").
            type (str): The type of the object.
            datacontenttype (Optional[str]): The content type of the data (default is None).
            dataschema (Optional[str]): The schema of the data (default is None).
            subject (Optional[str]): The subject of the object (default is None).
            time (Optional[datetime]): The timestamp of the object (default is None).
            data (Any): The data associated with the object (default is None).
            **extensions (Hashable): Additional extensions for the object.
        Returns:
            None
        """
        self._id = id
        self._source = source
        self._specversion = specversion
        self._type = type
        self._datacontenttype = datacontenttype
        self._dataschema = dataschema
        self._subject = subject
        self._time = time
        self._data = data
        self._extensions = extensions

    def to_json(self, *args, **kwargs):
        """
        A function that converts the object attributes into a JSON format.

        Parameters:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            str: A JSON string representing the object attributes.
        """
        v = {
            "id": self._id,
            "source": self._source,
            "specversion": self._specversion,
            "type": self._type,
            "data": self._data,
            **self._extensions,
        }
        if self._datacontenttype is not None:
            v["datacontenttype"] = self._datacontenttype
        if self._dataschema is not None:
            v["dataschema"] = self._dataschema
        if self._subject is not None:
            v["subject"] = self._subject
        if self._time is not None:
            v["time"] = self._time.isoformat()
        return json.dumps(v, *args, **kwargs)

    @classmethod
    def from_json(cls, json_str: str, *args, **kwargs):
        """
        Class method to create an instance from a JSON string.

        Args:
            json_str (str): The JSON string to parse.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The instance created from the JSON string.
        """
        v: dict[str, Any] = json.loads(json_str, *args, **kwargs)
        return cls.from_dict(v)

    @classmethod
    def from_mapping(cls, m: Mapping[str, Any]):
        """
        Create an instance of the class from a mapping, using the provided mapping as the initial data.

        Args:
            m (Mapping[str, Any]): A mapping of string keys to values of any type.

        Returns:
            An instance of the class.
        """
        v: Dict[str, Any] = deepcopy(m)
        return cls.from_dict(v)

    @classmethod
    def from_dict(cls, v: Dict[str, Any]):
        """
        Generate an instance from a dictionary.

        Parameters:
            v (Dict[str, Any]): A dictionary containing the data for the instance.

        Returns:
            An instance created from the dictionary data.
        """
        id_ = v.pop("id")
        source = v.pop("source")
        specversion = v.pop("specversion")
        type_ = v.pop("type")
        time = v.pop("time", None)
        if time is not None:
            time = datetime.fromisoformat(time)
        data = v.pop("data", None)
        return cls(
            id=id_,
            source=source,
            specversion=specversion,
            type=type_,
            time=time,
            data=data,
            **v,
        )


if __name__ == "__main__":
    v = {
        "specversion": "1.0",
        "type": "com.github.pull_request.opened",
        "source": "https://github.com/cloudevents/spec/pull",
        "subject": "123",
        "id": "A234-1234-1234",
        "time": "2018-04-05T17:31:00Z",
        "comexampleextension1": "value",
        "comexampleothervalue": 5,
        "datacontenttype": "text/xml",
        "data": '<much wow="xml"/>',
    }
    event = CloudEvent.from_mapping(v)
    print(event.to_json())
    print(v)
