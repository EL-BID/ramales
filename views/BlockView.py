from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from .ui.BlockDialogUi import Ui_BlockDialog

class BlockViewDialog(QDialog, Ui_BlockDialog):

    def __init__(self, project):
        QDialog.__init__(self)
        self.setupUi(self)
        self.proj = project
        self.current_block = None
        self.accepted.connect(self.save)

    def setData(self, block, nodes):
        #data mapper
        self.revision.setText(self.check(block['revision']))
        self.blockName.setText(self.check(block['blockName']))
        if block['date']:
            self.date.setDate(block['date'])
        if block['revDate']:
            self.revisionDate.setDate(block['revDate'])
        self.watershed.setText(self.check(block['watershed']))
        if block['length']:            
            self.totalLength.setValue(float(block['length']))
        if block['minDepth']:
            self.minDepth.setValue(block['minDepth'])
        if block['minSlope']:
            self.minSlope.setValue(block['minSlope'])
        self.observations.appendPlainText(self.check(block['comments']))        
        self.current_block = block

        nodesCount = len(nodes)
        self.tableWidget.setColumnCount(18)
        self.tableWidget.setRowCount(nodesCount)
        # self.tableWidget.setMinimumWidth(500)
        # self.tableWidget.setMinimumHeight(500)

        # Set the table headers
        self.tableWidget.setHorizontalHeaderLabels(
            ["id", "length", "username","up_box", "down_box", "up_gl", "down_gl",
            "pvc_diameter", "upBrLevel", "dwnBrLevel", "upDepth", "dwnDepth", "model",
             "upRuleLvl", "dwnRuleLvl", "critDepth", "slopeSection", "obs"]
            )

        # Set the table values
        for i in range(nodesCount):
            node = nodes[i].attribute     
            self.tableWidget.setItem(i, 0, QTableWidgetItem(self.check(node('id'))))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(self.check(node('length'))))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(self.check(node('username'))))
            self.tableWidget.setItem(i, 3, QTableWidgetItem(self.check(node('up_box'))))
            self.tableWidget.setItem(i, 4, QTableWidgetItem(self.check(node('down_box'))))
            self.tableWidget.setItem(i, 5, QTableWidgetItem(self.check(node('up_gl'))))
            self.tableWidget.setItem(i, 6, QTableWidgetItem(self.check(node('down_gl'))))
            self.tableWidget.setItem(i, 7, QTableWidgetItem(self.check(node('pvc_diam'))))
            self.tableWidget.setItem(i, 17, QTableWidgetItem(self.check(node('comments'))))


        # Resize of the rows and columns based on the content
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()

        # Display the table
        self.tableWidget.show()

        self.show()

    def save(self):
        layer = self.proj.getBlocksLayer()
        
        if not layer.isEditable():
                layer.startEditing()
        
        layer.changeAttributeValue( self.current_block.id(), layer.fields().lookupField('revision'), self.revision.text())
        layer.changeAttributeValue( self.current_block.id(), layer.fields().lookupField('blockName'), self.blockName.text())
        layer.changeAttributeValue( self.current_block.id(), layer.fields().lookupField('date'), self.date.date())
        layer.changeAttributeValue( self.current_block.id(), layer.fields().lookupField('revDate'), self.revisionDate.date())
        layer.changeAttributeValue( self.current_block.id(), layer.fields().lookupField('watershed'), self.watershed.text())
        layer.changeAttributeValue( self.current_block.id(), layer.fields().lookupField('length'), self.totalLength.value())
        layer.changeAttributeValue( self.current_block.id(), layer.fields().lookupField('minDepth'), self.minDepth.value())
        layer.changeAttributeValue( self.current_block.id(), layer.fields().lookupField('minSlope'), self.minSlope.value())
        layer.changeAttributeValue( self.current_block.id(), layer.fields().lookupField('comments'), self.observations.toPlainText())
        layer.commitChanges()
        self.proj.showMessage('saved successfully')
        self.hide()

    def check(self, var):
        return ('' if var == None else str(var))