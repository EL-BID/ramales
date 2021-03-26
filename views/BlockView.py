from PyQt5.QtWidgets import QDialog
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
        self.revision.setText(str(block['revision']))
        self.blockName.setText(str(block['blockName']))
        if block['date']:
            self.date.setDate(block['date'])
        if block['revDate']:
            self.revisionDate.setDate(block['revDate'])
        self.watershed.setText(str(block['watershed']))
        if block['length']:            
            self.totalLength.setValue(float(block['length']))
        if block['minDepth']:
            self.minDepth.setValue(block['minDepth'])
        if block['minSlope']:
            self.minSlope.setValue(block['minSlope'])
        self.observations.appendPlainText(str(block['comments']))        
        self.current_block = block
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