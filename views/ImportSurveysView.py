from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QAbstractItemView
from .ui.ImportSurveysDialogUi import Ui_SurveysDialog


class ImportSurveysDialog(QDialog, Ui_SurveysDialog):

    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)
        self.surveysTableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)   


    def hasData(self):
        return self.surveysTableWidget.rowCount() > 0
    
    def clearData(self):
        self.surveysTableWidget.setRowCount(0)

    def populateSurveys(self, data):
        self.clearData()
        table = self.surveysTableWidget
        for p in data:
            project = p['projectName']
            for s in p['surveys']:
                rowPosition = table.rowCount()
                table.insertRow(rowPosition)            
                survey = s['name']
                numcols = table.columnCount()
                numrows = table.rowCount()           
                table.setRowCount(numrows)
                table.setColumnCount(numcols)           
                table.setItem(numrows -1,0, QTableWidgetItem(project))
                table.setItem(numrows -1,1, QTableWidgetItem(survey)) 