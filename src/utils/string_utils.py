from typing import Any


def key_value_str(test_dict: dict):
    return "".join(["{", ",".join([f'{strip(key)}: {identify(val)}' for key, val in test_dict.items()]),
                   "}"]) if test_dict else ""


def strip(k: str):
    return k.replace('"', '')


def identify(val: Any):
    return f'"{val}"' if type(val) == str else val
