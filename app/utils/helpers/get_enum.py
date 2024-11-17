from typing import Dict, Type
from enum import Enum

def enum_to_dict(enum_class: Type[Enum]) -> Dict:
    return {item.name: item.value for item in enum_class}