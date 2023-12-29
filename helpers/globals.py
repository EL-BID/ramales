LANGUAGE_FILE = None
LAYER_RASTER = None


def set_language_file(lang_file: str):
    global LANGUAGE_FILE
    LANGUAGE_FILE = lang_file


def get_language_file():
    global LANGUAGE_FILE
    return LANGUAGE_FILE


def set_layer_raster(layer_raster: str):
    global LAYER_RASTER
    LAYER_RASTER = layer_raster


def get_layer_raster():
    global LAYER_RASTER
    return LAYER_RASTER
