#!/bin/bash
pyuic5 sanibid_ramales_dialog_base.ui -o ../views/ui/SanibidRamalesDialogBaseUi.py
pyuic5 block_dialog.ui -o ../views/ui/BlockDialogUi.py

echo " "
echo "done!"