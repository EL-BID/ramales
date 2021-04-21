from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from .ui.BlockDialogUi import Ui_BlockDialog
from qgis.PyQt.QtCore import QCoreApplication

translate = QCoreApplication.translate

class BlockViewDialog(QDialog, Ui_BlockDialog):

    def __init__(self, project):
        QDialog.__init__(self)
        self.setupUi(self)
        self.proj = project
        self.current_block = None
        self.current_nodes = None
        self.accepted.connect(self.save)
        self.tableWidget.itemChanged.connect(self.onItemChanged)
        self.minDepth.valueChanged.connect(self.depthMinChanged)
        self.minSlope.valueChanged.connect(self.slopeMinChanged)

    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return translate('BlockViewDialog', message)

    def setData(self, block, nodes):
        self.minDepth.blockSignals(True)
        self.minSlope.blockSignals(True)
        self.tableWidget.blockSignals(True)
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
        self.tableWidget.setColumnCount(16)
        self.tableWidget.setRowCount(nodesCount)

        # Set the table headers
        self.tableWidget.setHorizontalHeaderLabels(
            [self.tr("up_box"), self.tr("down_box"),self.tr("length"), self.tr("up_gl"), self.tr("down_gl"),
             self.tr("upBrLevel"), self.tr("dwnBrLevel"), self.tr("upDepth"), self.tr("dwnDepth"), self.tr("model"),
             self.tr("upRuleLvl"), self.tr("dwnRuleLvl"), self.tr("critDepth"), self.tr("slopeSection"),
             self.tr("pvc_diameter"), self.tr("obs")]
            )

        # Set the table values
        totalLength = 0
        for i in range(nodesCount):
            node = nodes[i].attribute
            if node('length') != None :
                totalLength = totalLength + float(node('length'))
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

        self.totalLength.setValue(float(totalLength))
        # Resize of the rows and columns based on the content
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()
        # Display the table
        self.tableWidget.show()
        self.tableWidget.blockSignals(False)
        self.minDepth.blockSignals(False)
        self.minSlope.blockSignals(False)
        self.show()

    def save(self):
        self.tableWidget.blockSignals(True)
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
        nodes = self.proj.getNodesLayer()
        if not nodes.isEditable():
            nodes.startEditing()
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
            nodes.changeAttributeValue(node.id(), nodes.fields().lookupField('pvc_diam'), self.tableWidget.item(row,14).text() )
            nodes.changeAttributeValue(node.id(), nodes.fields().lookupField('comments'), self.tableWidget.item(row,15).text() )
            row += 1
        blocks.commitChanges()
        nodes.commitChanges()
        self.tableWidget.blockSignals(False)
        self.proj.showMessage('saved successfully')
        self.hide()

    def check(self, var):
        return ('' if var == None else str(var))

    def depthMinChanged(self, val):
        self.calculate()
    
    def slopeMinChanged(self, val):
        self.calculate()
    
    def onItemChanged(self, index):
        val = self.tableWidget.item(index.row(), index.column()).text()
        val = val if val != '' else None
        if (index.column() == 12):
            self.tableWidget.blockSignals(True)
            self.tableWidget.setItem(index.row(), 7, QTableWidgetItem(val))
            self.tableWidget.blockSignals(False)
            self.calculate()

    def calculate(self):
        self.tableWidget.blockSignals(True)
        minDepth = self.minDepth.value()
        minSlope = self.minSlope.value()
        for i in range(self.tableWidget.rowCount()):
            length = float(self.tableWidget.item(i, 2).text())
            up_gl = float(self.tableWidget.item(i, 3).text())
            down_box = float(self.tableWidget.item(i, 1).text())
            down_gl = float(self.tableWidget.item(i, 4).text())
            critDepth = float(self.tableWidget.item(i, 12).text()) if self.tableWidget.item(i, 12).text() != None and self.tableWidget.item(i, 12).text() != '' else 0
            dwnDepthPrev = 0 if i == 0 else float(self.tableWidget.item((i-1), 8).text())
            dwnBrLevelPrev = 0 if i == 0 else float(self.tableWidget.item((i-1), 6).text())
            if (i == 0):
                upDepth = (minDepth) if down_box != 0 else ''  #H21 i==0
                upBrLevel = (up_gl - upDepth) if down_box != 0 else '' #tocheck ''  #F21 i==0
            else:
                upBrLevel = 0 if down_box == 0 else (0 if length == 0 else (dwnBrLevelPrev if (dwnDepthPrev > critDepth) else (up_gl - critDepth)))
                upDepth = (up_gl - upBrLevel) if (down_box != 0) else ""

            dwnBrLevel = "" if down_box == 0 else (0 if length == 0 else ((down_gl - minDepth) if (upBrLevel - (down_gl - minDepth))/length >= minSlope else round((upBrLevel - length * minSlope - 0.0005), 3))) #G21
            dwnDepth = (down_gl - dwnBrLevel) if down_box != 0 else ''#I21
            model = 2 #J21 = 2 -> setear en el setdata

            upRuleLvl = "" if down_box == 0 else ("" if length == 0 else (model + upBrLevel )) #K21
            dwnRuleLvl = "" if down_box == 0 else ("" if length == 0 else (model + dwnBrLevel)) #L21
            slopeSection = "" if down_box == 0 else round((upBrLevel - dwnBrLevel) * 100, 1) # N21 slopeSection

            self.tableWidget.setItem(i, 5, QTableWidgetItem(str(round(upBrLevel, 3))))
            self.tableWidget.setItem(i, 6, QTableWidgetItem(str(round(dwnBrLevel, 3))))
            self.tableWidget.setItem(i, 7, QTableWidgetItem(str(round(upDepth, 2))))
            self.tableWidget.setItem(i, 8, QTableWidgetItem(str(round(dwnDepth, 2))))
            self.tableWidget.setItem(i, 9, QTableWidgetItem(str(model))) #tocheck
            self.tableWidget.setItem(i, 10, QTableWidgetItem(str(round(upRuleLvl, 3))))
            self.tableWidget.setItem(i, 11, QTableWidgetItem(str(round(dwnRuleLvl, 3))))
            self.tableWidget.setItem(i, 12, QTableWidgetItem(str(round(critDepth, 3))))
            self.tableWidget.setItem(i, 13, QTableWidgetItem(str(slopeSection)))

        self.tableWidget.blockSignals(False)