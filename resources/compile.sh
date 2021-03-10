#!/bin/bash
pyuic5 sanibid_ramales_dialog_base.ui -o ../views/ui/SanibidRamalesDialogBaseUi.py
pyuic5 layers_panel_dialog.ui -o ../views/ui/LayersPanelDialogUi.py

echo " "
echo "done!"