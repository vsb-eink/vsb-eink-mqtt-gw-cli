import json
from dataclasses import dataclass, asdict


def skip_none_factory(cls):
    return {k: v for (k, v) in cls if v is not None}


def to_json(dataclass_instance: dataclass):
    return json.dumps(asdict(dataclass_instance, dict_factory=skip_none_factory))
