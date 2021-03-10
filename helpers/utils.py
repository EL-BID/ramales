def setComboItem(combo, value):
    fndIndex = combo.findText(value)
    if not fndIndex:
        combo.setCurrentIndex(0)
    else:
        combo.setCurrentIndex(fndIndex)
