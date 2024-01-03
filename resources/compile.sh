#!/bin/bash
#pyuic5 sanihub_ramales_dialog_base.ui -o ../views/ui/SanihubRamalesDialogBaseUi.py
#pyuic5 layers_panel_dialog.ui -o ../views/ui/LayersPanelDialogUi.py
#pyuic5 block_dialog.ui -o ../views/ui/BlockDialogUi.py
#pyuic5 login_dialog.ui -o ../views/ui/LoginView.py
#pyuic5 import_surveys_dialog.ui -o ../views/ui/ImportSurveysDialogUi.py
#pyuic5 publish_dialog.ui -o ../views/ui/PublishDialogUi.py
#pyrcc5 resources.qrc -o resources.py
#echo " "
#echo "done!"


#@echo off
#call "C:\OSGeo4W\bin\o4w_env.bat"
#call "C:\OSGeo4W\bin\qt5_env.bat"
#call "C:\OSGeo4W\bin\py3_env.bat"
#
#@echo on
pyrcc5 -o resources.py resources.qrc