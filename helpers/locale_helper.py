from .utils import Utils
from functools import lru_cache


@lru_cache(maxsize=1)
def get_localization_object():
    utils = Utils()
    return utils.get_locale_json()
