from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from .ui.BlockDialogUi import Ui_BlockDialog
from qgis.core import *

class BlockViewDialog(QDialog, Ui_BlockDialog):

    def __init__(self, project):
        QDialog.__init__(self)
        self.setupUi(self)
        self.proj = project
        self.current_block = None
        self.current_nodes = None
        self.accepted.connect(self.save)
        self.tableWidget.model().dataChanged.connect(self.onDataChanged)
        self.minDepth.valueChanged.connect(self.depthMinChanged)
        self.minSlope.valueChanged.connect(self.slopeMinChanged)

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
        self.tableWidget.setColumnCount(17)
        self.tableWidget.setRowCount(nodesCount)

        # Set the table headers
        self.tableWidget.setHorizontalHeaderLabels(
            ["up_box", "down_box","length", "up_gl", "down_gl",
             "upBrLevel", "dwnBrLevel", "upDepth", "dwnDepth", "model",
             "upRuleLvl", "dwnRuleLvl", "critDepth", "slopeSection",
             "pvc_diameter", "obs", "username"]
            )

        # Set the table values
        for i in range(nodesCount):
            node = nodes[i].attribute     
            self.tableWidget.setItem(i, 0, QTableWidgetItem(self.check(node('up_box'))))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(self.check(node('down_box'))))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(self.check(node('length'))))
            self.tableWidget.setItem(i, 3, QTableWidgetItem(self.check(node('up_gl'))))
            self.tableWidget.setItem(i, 4, QTableWidgetItem(self.check(node('down_gl'))))
            self.tableWidget.setItem(i, 5, QTableWidgetItem(self.check(node('upBrLevel'))))
            self.tableWidget.setItem(i, 6, QTableWidgetItem(self.check(node('dwnBrLevel'))))
            self.tableWidget.setItem(i, 7, QTableWidgetItem(self.check(node('upDepth'))))
            self.tableWidget.setItem(i, 8, QTableWidgetItem(self.check(node('dwnDepth'))))
            self.tableWidget.setItem(i, 9, QTableWidgetItem(self.check(node('model'))))
            self.tableWidget.setItem(i, 10, QTableWidgetItem(self.check(node('upRuleLvl'))))
            self.tableWidget.setItem(i, 11, QTableWidgetItem(self.check(node('dwnRuleLvl'))))
            self.tableWidget.setItem(i, 12, QTableWidgetItem(self.check(node('critDepth'))))
            self.tableWidget.setItem(i, 13, QTableWidgetItem(self.check(node('slopeSec'))))
            self.tableWidget.setItem(i, 14, QTableWidgetItem(self.check(node('pvc_diam'))))
            self.tableWidget.setItem(i, 15, QTableWidgetItem(self.check(node('comments'))))
            self.tableWidget.setItem(i, 16, QTableWidgetItem(self.check(node('username'))))

        # Resize of the rows and columns based on the content
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()
        # Display the table
        self.tableWidget.show()

        self.show()

    def save(self):
        #blocks
        blocks = self.proj.getBlocksLayer()        
        with edit(blocks):
            blocks.changeAttributeValue( self.current_block.id(), blocks.fields().lookupField('revision'), self.revision.text())
            blocks.changeAttributeValue( self.current_block.id(), blocks.fields().lookupField('blockName'), self.blockName.text())
            blocks.changeAttributeValue( self.current_block.id(), blocks.fields().lookupField('date'), self.date.date())
            blocks.changeAttributeValue( self.current_block.id(), blocks.fields().lookupField('revDate'), self.revisionDate.date())
            blocks.changeAttributeValue( self.current_block.id(), blocks.fields().lookupField('watershed'), self.watershed.text())
            blocks.changeAttributeValue( self.current_block.id(), blocks.fields().lookupField('length'), self.totalLength.value())
            blocks.changeAttributeValue( self.current_block.id(), blocks.fields().lookupField('minDepth'), self.minDepth.value())
            blocks.changeAttributeValue( self.current_block.id(), blocks.fields().lookupField('minSlope'), self.minSlope.value())
            blocks.changeAttributeValue( self.current_block.id(), blocks.fields().lookupField('comments'), self.observations.toPlainText())
                
        #nodes
        nodes = self.proj.getNodesLayer()
        with edit(nodes):
            row = 0
            for node in self.current_nodes:
                nodes.changeAttributeValue(node.id(), nodes.fields().lookupField('up_box'), self.tableWidget.item(row,0).text() )
                nodes.changeAttributeValue(node.id(), nodes.fields().lookupField('down_box'), self.tableWidget.item(row,1).text() )
                nodes.changeAttributeValue(node.id(), nodes.fields().lookupField('length'), self.tableWidget.item(row,2).text() )
                nodes.changeAttributeValue(node.id(), nodes.fields().lookupField('up_gl'), self.tableWidget.item(row,3).text() )
                nodes.changeAttributeValue(node.id(), nodes.fields().lookupField('down_gl'), self.tableWidget.item(row,4).text() )
                nodes.changeAttributeValue(node.id(), nodes.fields().lookupField('upBrLevel'), self.tableWidget.item(row,5).text() )
                nodes.changeAttributeValue(node.id(), nodes.fields().lookupField('dwnBrLevel'), self.tableWidget.item(row,6).text() )
                nodes.changeAttributeValue(node.id(), nodes.fields().lookupField('upDepth'), self.tableWidget.item(row,7).text() )
                nodes.changeAttributeValue(node.id(), nodes.fields().lookupField('dwnDepth'), self.tableWidget.item(row,8).text() )
                nodes.changeAttributeValue(node.id(), nodes.fields().lookupField('model'), self.tableWidget.item(row,9).text() )
                nodes.changeAttributeValue(node.id(), nodes.fields().lookupField('upRuleLvl'), self.tableWidget.item(row,10).text() )
                nodes.changeAttributeValue(node.id(), nodes.fields().lookupField('dwnRuleLvl'), self.tableWidget.item(row,11).text() )
                nodes.changeAttributeValue(node.id(), nodes.fields().lookupField('critDepth'), self.tableWidget.item(row,12).text() )
                nodes.changeAttributeValue(node.id(), nodes.fields().lookupField('slopeSec'), self.tableWidget.item(row,13).text() )
                nodes.changeAttributeValue(node.id(), nodes.fields().lookupField('pvc_diam'), self.tableWidget.item(row,14) )
                nodes.changeAttributeValue(node.id(), nodes.fields().lookupField('comments'), self.tableWidget.item(row,15).text() )
                nodes.changeAttributeValue(node.id(), nodes.fields().lookupField('username'), self.tableWidget.item(row,16).text() )
                row += 1       
        
        self.proj.showMessage('saved successfully')
        self.hide()

    def check(self, var):
        return ('' if var == None else str(var))

    def depthMinChanged(self, val):
        # print(val)
        self.calculate()
    
    def slopeMinChanged(self, val):
        # print(val)
        self.calculate()
    
    def onDataChanged(self, index, index2, roles):
        val = index.data()
        colName = self.tableWidget.horizontalHeaderItem(index.column()).text()
        # colName = self.tableWidget.record(index.row()).fieldName(index.column())
        # print(colName)
        # if (colName == ''):

    def calculate(self):
        minDepth = self.minDepth.value()
        minSlope = self.minSlope.value()
        nodesCount = len(self.current_nodes)
        for i in range(nodesCount):
            node = self.current_nodes[i].attribute
            length = node('length')
            up_gl = node('up_gl')
            down_box = node('down_box')
            down_gl = node('down_gl')
            #H21
            upDepth = (minDepth) if down_box != 0 else ''
            #F21
            upBrLevel = (up_gl - upDepth) if down_box != 0 else ''
            #G21
            dwnBrLevel = "" if down_box == 0 else (0 if length == 0 else ((down_gl - minDepth) if (upBrLevel - (down_gl - minDepth))/length >= minSlope else round((upBrLevel - length * minSlope - 0.0005), 3)))
            #I21
            dwnDepth = (down_gl - dwnBrLevel) if down_box != 0 else ''
            #J21 = 2 pero pueden modificar.
            model = 2
            #K21
            upRuleLvl = "" if down_box == 0 else ("" if length == 0 else (model + upBrLevel ))
            #L21 
            dwnRuleLvl = "" if down_box == 0 else ("" if length == 0 else (model + dwnBrLevel))
            #M21 critDepth puede modificarse y hace otro evento
            # N21 slopeSection
            slopeSection = "" if down_box == 0 else round((upBrLevel - dwnBrLevel)*100, 1)
            
            self.tableWidget.setItem(i, 5, QTableWidgetItem(str(upBrLevel)))
            self.tableWidget.setItem(i, 6, QTableWidgetItem(str(dwnBrLevel)))
            self.tableWidget.setItem(i, 7, QTableWidgetItem(str(upDepth)))
            self.tableWidget.setItem(i, 8, QTableWidgetItem(str(round(dwnDepth, 2))))
            self.tableWidget.setItem(i, 9, QTableWidgetItem(str(model))) #tocheck
            self.tableWidget.setItem(i, 10, QTableWidgetItem(str(upRuleLvl)))
            self.tableWidget.setItem(i, 11, QTableWidgetItem(str(dwnRuleLvl)))
            self.tableWidget.setItem(i, 13, QTableWidgetItem(str(slopeSection)))