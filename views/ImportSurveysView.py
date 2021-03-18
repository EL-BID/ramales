from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QAbstractItemView
from .ui.ImportSurveysDialogUi import Ui_SurveysDialog


class ImportSurveysDialog(QDialog, Ui_SurveysDialog):

    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)
        self.surveysTableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)         
        


    def hasRows(self):
        return self.surveysTableWidget.rowCount() > 0
    
    def clearAll(self):
        self.surveysTableWidget.setRowCount(0)

    def populateSurveys(self, data):
        self.clearAll()
        table = self.surveysTableWidget
        for p in data:
            project = p['projectName']
            for s in p['surveys']:
                rowPosition = table.rowCount()
                table.insertRow(rowPosition)            
                survey = s['name']
                id = str(s['id'])
                numcols = table.columnCount()
                numrows = table.rowCount()           
                table.setRowCount(numrows)
                table.setColumnCount(numcols)
                table.setItem(numrows -1,0, QTableWidgetItem(id))            
                table.setItem(numrows -1,1, QTableWidgetItem(project))
                table.setItem(numrows -1,2, QTableWidgetItem(survey))
                


    def getIdFromRow(self):
        row = self.surveysTableWidget.currentRow()        
        item = self.surveysTableWidget.item(row,0)
        id = item.text()
        return id