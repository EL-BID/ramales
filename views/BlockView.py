from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from .ui.BlockDialogUi import Ui_BlockDialog

class BlockViewDialog(QDialog, Ui_BlockDialog):

    def __init__(self, project):
        QDialog.__init__(self)
        self.setupUi(self)
        self.proj = project
        self.current_block = None
        self.current_nodes = None
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
        self.current_nodes = nodes

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
        #blocks
        blocks = self.proj.getBlocksLayer()        
        if not blocks.isEditable():
                blocks.startEditing()
        blocks.changeAttributeValue( self.current_block.id(), blocks.fields().lookupField('revision'), self.revision.text())
        blocks.changeAttributeValue( self.current_block.id(), blocks.fields().lookupField('blockName'), self.blockName.text())
        blocks.changeAttributeValue( self.current_block.id(), blocks.fields().lookupField('date'), self.date.date())
        blocks.changeAttributeValue( self.current_block.id(), blocks.fields().lookupField('revDate'), self.revisionDate.date())
        blocks.changeAttributeValue( self.current_block.id(), blocks.fields().lookupField('watershed'), self.watershed.text())
        blocks.changeAttributeValue( self.current_block.id(), blocks.fields().lookupField('length'), self.totalLength.value())
        blocks.changeAttributeValue( self.current_block.id(), blocks.fields().lookupField('minDepth'), self.minDepth.value())
        blocks.changeAttributeValue( self.current_block.id(), blocks.fields().lookupField('minSlope'), self.minSlope.value())
        blocks.changeAttributeValue( self.current_block.id(), blocks.fields().lookupField('comments'), self.observations.toPlainText())
        blocks.commitChanges()
        
        #nodes
        nodes = self.proj.getNodesLayer()
        if not nodes.isEditable():
            nodes.startEditing()
        row = 0
        for node in self.current_nodes:                        
            nodes.changeAttributeValue(node.id(), nodes.fields().lookupField('id'), self.tableWidget.item(row,0).text() )
            nodes.changeAttributeValue(node.id(), nodes.fields().lookupField('length'), self.tableWidget.item(row,1).text() )
            nodes.changeAttributeValue(node.id(), nodes.fields().lookupField('username'), self.tableWidget.item(row,2).text() )
            nodes.changeAttributeValue(node.id(), nodes.fields().lookupField('up_box'), self.tableWidget.item(row,3).text() )
            nodes.changeAttributeValue(node.id(), nodes.fields().lookupField('down_box'), self.tableWidget.item(row,4).text() )
            nodes.changeAttributeValue(node.id(), nodes.fields().lookupField('up_gl'), self.tableWidget.item(row,5).text() )
            nodes.changeAttributeValue(node.id(), nodes.fields().lookupField('down_gl'), self.tableWidget.item(row,6).text() )
            nodes.changeAttributeValue(node.id(), nodes.fields().lookupField('pvc_diam'), self.tableWidget.item(row,7).text() )
            nodes.changeAttributeValue(node.id(), nodes.fields().lookupField('comments'), self.tableWidget.item(row,17).text() )
            row += 1
        nodes.commitChanges()
        
        self.proj.showMessage('saved successfully')
        self.hide()

    def check(self, var):
        return ('' if var == None else str(var))