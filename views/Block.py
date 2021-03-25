# Test
# from PyQt5.QtWidgets import *


def formOpen(dialog,layer,feature):
    print('FORMOPEN')
    geometry = feature.geometry()
    print(geometry)
    # wktString = geometry.exportToWkt()
    # print(wktString)