#!/bin/bash
pyuic5 sanibid_ramales_dialog_base.ui -o ../views/ui/SanibidRamalesDialogBaseUi.py
pyuic5 block_dialog.ui -o ../views/ui/BlockDialogUi.py
pyuic5 login_dialog.ui -o ../views/ui/LoginView.py
pyuic5 import_surveys_dialog.ui -o ../views/ui/ImportSurveysDialogUi.py

echo " "
echo "done!"