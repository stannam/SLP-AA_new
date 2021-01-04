from PyQt5.QtCore import (
    Qt,
    QSize,
    QSettings,
    QPoint,
    QAbstractTableModel,
    pyqtSignal,
    QMimeData
)
from PyQt5.QtWidgets import (
    QVBoxLayout,
    QDialog,
    QTableView,
    QAction,
    QAbstractItemView,
    QMenu
)
from PyQt5.QtGui import (
    QIcon,
    QPixmap,
    QColor,
    QDrag,
    QImage
)

from lexicon.predefined_handshape import (
    Handshape1, Handshape5, HandshapeA, HandshapeB1, HandshapeB2, HandshapeBase, HandshapeC, HandshapeO, HandshapeS, HandshapeEmpty,
    HandshapeExtendedA, HandshapeClosedAIndex, HandshapeOpenA, HandshapeModifiedA,
    HandshapeBentB, HandshapeClawedExtendedB, HandshapeContractedB, HandshapeCrookedExtendedB, HandshapeExtendedB, HandshapeSlantedExtendedB,
    HandshapeBentExtendedB,
    HandshapeClawedC, HandshapeClawedSpreadC, HandshapeCrookedC, HandshapeContractedC, HandshapeExtendedC, HandshapeFlatC, HandshapeCIndex, HandshapeDoubleCIndex, HandshapeSpreadC, HandshapeSpreadExtendedC,
    HandshapeD, HandshapePartiallyBentD, HandshapeClosedBentD, HandshapeModifiedD,
    HandshapeE, HandshapeOpenE,
    HandshapeF, HandshapeClawedF, HandshapeCoveredF, HandshapeSlantedF, HandshapeFlatF, HandshapeFlatOpenF, HandshapeFlatClawedF, HandshapeAdductedF, HandshapeOffsetF, HandshapeOpenF,
    HandshapeG, HandshapeClosedG, HandshapeDoubleModifiedG, HandshapeClosedDoubleModifiedG, HandshapeModifiedG,
    HandshapeI, HandshapeBentCombinedIPlus1, HandshapeBentI, HandshapeClawedI, HandshapeCombinedIPlus1, HandshapeCombinedILY, HandshapeCombinedIPlusA, HandshapeFlatCombinedIPlus1,
    HandshapeK, HandshapeExtendedK,
    HandshapeL, HandshapeBentL, HandshapeBentThumbL, HandshapeClawedL, HandshapeContractedL, HandshapeDoubleContractedL, HandshapeCrookedL,
    HandshapeM, HandshapeFlatM,
    HandshapeN,
    HandshapeCoveredO, HandshapeFlatO, HandshapeOIndex, HandshapeModifiedO, HandshapeOffsetO, HandshapeOpenSpreadO, HandshapeOpenOIndex,
    HandshapeR, HandshapeBentR, HandshapeExtendedR,
    HandshapeT, HandshapeCoveredT,
    HandshapeU, HandshapeBentU, HandshapeBentExtendedU, HandshapeClawedU, HandshapeCombinedUAndY, HandshapeContractedU, HandshapeContractedUIndex, HandshapeCrookedU, HandshapeExtendedU,
    HandshapeV, HandshapeBentV, HandshapeBentExtendedV, HandshapeClawedV, HandshapeClawedExtendedV, HandshapeClosedV, HandshapeCrookedV, HandshapeCrookedExtendedV, HandshapeSlantedV,
    HandshapeW, HandshapeClawedW, HandshapeClosedW, HandshapeCrookedW,
    HandshapeX, HandshapeExtendedX, HandshapeClosedX,
    HandshapeY, HandshapeCombinedYAndMiddle, HandshapeModifiedY,
    HandshapeBent1, HandshapeBentOffset1, HandshapeClawed1, HandshapeCrooked1,
    Handshape3, HandshapeClawed3, HandshapeContracted3,
    Handshape4, HandshapeBent4, HandshapeClawed4, HandshapeCrooked4, HandshapeSlanted4,
    HandshapeBent5, HandshapeBentMidfinger5, HandshapeClawed5, HandshapeContracted5, HandshapeRelaxedContracted5, HandshapeCrooked5, HandshapeCrookedSlanted5, HandshapeModified5, HandshapeSlanted5,
    Handshape6,
    Handshape8, HandshapeCovered8, HandshapeExtended8, HandshapeOpen8,
    HandshapeMiddleFinger
)

PREDEFINED_MAP = {
        '1': Handshape1(),
        '5': Handshape5(),
        'A': HandshapeA(),
        'B1': HandshapeB1(),
        'B2': HandshapeB2(),
        'base': HandshapeBase(),
        'C': HandshapeC(),
        'O': HandshapeO(),
        'S': HandshapeS(),

        'extended-A': HandshapeExtendedA(),
        'closed-A-index': HandshapeClosedAIndex(),
        'open-A': HandshapeOpenA(),
        'modified-A': HandshapeModifiedA(),

        'bent-B': HandshapeBentB(),
        'clawed-extended-B': HandshapeClawedExtendedB(),
        'contracted-B': HandshapeContractedB(),
        'crooked-extended-B': HandshapeCrookedExtendedB(),
        'extended-B': HandshapeExtendedB(),
        'slanted-extended-B': HandshapeSlantedExtendedB(),
        'bent-extended-B': HandshapeBentExtendedB(),

        'clawed-C': HandshapeClawedC(),
        'clawed-spread-C': HandshapeClawedSpreadC(),
        'crooked-C': HandshapeCrookedC(),
        'contracted-C': HandshapeContractedC(),
        'extended-C': HandshapeExtendedC(),
        'flat-C': HandshapeFlatC(),
        'C-index': HandshapeCIndex(),
        'double-C-index': HandshapeDoubleCIndex(),
        'spread-C': HandshapeSpreadC(),
        'spread-extended-C': HandshapeSpreadExtendedC(),
        'D': HandshapeD(),
        'partially-bent-D': HandshapePartiallyBentD(),
        'closed-bent-D': HandshapeClosedBentD(),
        'modified-D': HandshapeModifiedD(),

        'E': HandshapeE(),
        'open-E': HandshapeOpenE(),

        'F': HandshapeF(),
        'clawed-F': HandshapeClawedF(),
        'covered-F': HandshapeCoveredF(),
        'slanted-F': HandshapeSlantedF(),
        'flat-F': HandshapeFlatF(),
        'flat-open-F': HandshapeFlatOpenF(),
        'flat-clawed-F': HandshapeFlatClawedF(),
        'adducted-F': HandshapeAdductedF(),
        'offset-F': HandshapeOffsetF(),
        'open-F': HandshapeOpenF(),

        'G': HandshapeG(),
        'closed-G': HandshapeClosedG(),
        'double-modified-G': HandshapeDoubleModifiedG(),
        'closed-double-modified-G': HandshapeClosedDoubleModifiedG(),
        'modified-G': HandshapeModifiedG(),

        'I': HandshapeI(),
        'bent-combined-I+1': HandshapeBentCombinedIPlus1(),
        'bent-I': HandshapeBentI(),
        'clawed-I': HandshapeClawedI(),
        'combined-I+1': HandshapeCombinedIPlus1(),
        'combined-ILY': HandshapeCombinedILY(),
        'combined-I+A': HandshapeCombinedIPlusA(),
        'flat-combined-I+1': HandshapeFlatCombinedIPlus1(),

        'K': HandshapeK(),
        'extended-K': HandshapeExtendedK(),

        'L': HandshapeL(),
        'bent-L': HandshapeBentL(),
        'thumb-L': HandshapeBentThumbL(),
        'clawed-L': HandshapeClawedL(),
        'contracted-L': HandshapeContractedL(),
        'double-contracted-L': HandshapeDoubleContractedL(),
        'crooked-L': HandshapeCrookedL(),

        'M': HandshapeM(),
        'flat-M': HandshapeFlatM(),

        'N': HandshapeN(),

        'covered-O': HandshapeCoveredO(),
        'flat-O': HandshapeFlatO(),
        'O-index': HandshapeOIndex(),
        'modified-O': HandshapeModifiedO(),
        'offset-O': HandshapeOffsetO(),
        'open-spread-O': HandshapeOpenSpreadO(),
        'open-O-index': HandshapeOpenOIndex(),

        'R': HandshapeR(),
        'bent-R': HandshapeBentR(),
        'extended-R': HandshapeExtendedR(),

        'T': HandshapeT(),
        'covered-T': HandshapeCoveredT(),

        'U': HandshapeU(),
        'bent-U': HandshapeBentU(),
        'bent-extended-U': HandshapeBentExtendedU(),
        'clawed-U': HandshapeClawedU(),
        'combined-U&Y': HandshapeCombinedUAndY(),
        'contracted-U': HandshapeContractedU(),
        'contracted-U-index': HandshapeContractedUIndex(),
        'crooked-U': HandshapeCrookedU(),
        'extended-U': HandshapeExtendedU(),

        'V': HandshapeV(),
        'bent-V': HandshapeBentV(),
        'bent-extended-V': HandshapeBentExtendedV(),
        'clawed-V': HandshapeClawedV(),
        'clawed-extended-V': HandshapeClawedExtendedV(),
        'closed-V': HandshapeClosedV(),
        'crooked-V': HandshapeCrookedV(),
        'crooked-extended-V': HandshapeCrookedExtendedV(),
        'slanted-V': HandshapeSlantedV(),

        'W': HandshapeW(),
        'clawed-W': HandshapeClawedW(),
        'closed-W': HandshapeClosedW(),
        'crooked-W': HandshapeCrookedW(),

        'X': HandshapeX(),
        'extended-X': HandshapeExtendedX(),
        'closed-X': HandshapeClosedX(),

        'Y': HandshapeY(),
        'combined-Y&middle': HandshapeCombinedYAndMiddle(),
        'modified-Y': HandshapeModifiedY(),

        'bent-1': HandshapeBent1(),
        'bent-offset-1': HandshapeBentOffset1(),
        'clawed-1': HandshapeClawed1(),
        'crooked-1': HandshapeCrooked1(),

        '3': Handshape3(),
        'clawed-3': HandshapeClawed3(),
        'contracted-3': HandshapeContracted3(),

        '4': Handshape4(),
        'bent-4': HandshapeBent4(),
        'clawed-4': HandshapeClawed4(),
        'crooked-4': HandshapeCrooked4(),
        'slanted-4': HandshapeSlanted4(),

        'bent-5': HandshapeBent5(),
        'bent-midfinger-5': HandshapeBentMidfinger5(),
        'clawed-5': HandshapeClawed5(),
        'contracted-5': HandshapeContracted5(),
        'relaxed-contracted-5': HandshapeRelaxedContracted5(),
        'crooked-5': HandshapeCrooked5(),
        'crooked-slanted-5': HandshapeCrookedSlanted5(),
        'modified-5': HandshapeModified5(),
        'slanted-5': HandshapeSlanted5(),

        '6': Handshape6(),

        '8': Handshape8(),
        'covered-8': HandshapeCovered8(),
        'extended-8': HandshapeExtended8(),
        'open-8': HandshapeOpen8(),
        'middle-finger': HandshapeMiddleFinger()
    }


class PredefinedTableModel(QAbstractTableModel):
    def __init__(self, predefined_images, **kwargs):
        super().__init__(**kwargs)
        self.predefined_images = predefined_images
        self.col_labels = ['Handshape',
                           'Bent',
                           'Clawed', 'Closed', 'Combined', 'Contracted', 'Covered', 'Crooked', 'Curved',
                           'Extended',
                           'Flat',
                           'Index',
                           'Modified',
                           'Offset', 'Open',
                           'Slanted', 'Spread']

        self.data_cached = [
            ['A',
             '',  # bent
             '', '', '', '', '', '', '',  # clawed, closed, combined, contracted, covered, crooked, curved
             'extended-A',  # extended
             '',  # flat
             '',  # index
             'modified-A',  # modified
             '', 'open-A',  # offset, open
             '', ''],  # slanted, spread
            ['',
             '',  # bent
             '', '', '', '', '', '', '',  # clawed, closed, combined, contracted, covered, crooked, curved
             '',  # extended
             '',  # flat
             'closed-A-index',  # index
             '',  # modified
             '', '',  # offset, open
             '', ''],  # slanted, spread
            ['B1',
             'bent-B',  # bent
             'clawed-extended-B', '', '', 'contracted-B', '', 'crooked-extended-B', '',  # 7 slots
             'extended-B',  # extended
             '',  # flat
             '',  # index
             '',  # modified
             '', '',  # offset, open
             'slanted-extended-B', ''],  # slanted, spread
            ['B2',
             'bent-extended-B',  # bent
             '', '', '', '', '', '', '',  # 7 slots
             '',  # extended
             '',  # flat
             '',  # index
             '',  # modified
             '', '',  # offset, open
             '', ''],  # slanted, spread
            ['C',
             '',  # bent
             'clawed-C', '', '', 'contracted-C', '', 'crooked-C', '',  # 7 slots
             'extended-C',  # extended
             'flat-C',  # flat
             'C-index',  # index
             '',  # modified
             '', '',  # offset, open
             '', 'spread-C'],  # slanted, spread
            ['',
             '',  # bent
             'clawed-spread-C', '', '', '', '', '', '',  # 7 slots
             '',  # extended
             '',  # flat
             'double-C-index',  # index
             '',  # modified
             '', '',  # offset, open
             '', 'spread-extended-C'],  # slanted, spread
            ['D',
             'partially-bent-D',  # bent
             '', 'closed-bent-D', '', '', '', '', '',  # 7 slots
             '',  # extended
             '',  # flat
             '',  # index
             'modified-D',  # modified
             '', '',  # offset, open
             '', ''],  # slanted, spread
            ['',
             'closed-bent-D',  # bent
             '', '', '', '', '', '', '',  # 7 slots
             '',  # extended
             '',  # flat
             '',  # index
             '',  # modified
             '', '',  # offset, open
             '', ''],  # slanted, spread
            ['E',
             '',  # bent
             '', '', '', '', '', '', '',  # 7 slots
             '',  # extended
             '',  # flat
             '',  # index
             '',  # modified
             '', 'open-E',  # offset, open
             '', ''],  # slanted, spread
            ['F',
             '',  # bent
             'clawed-F', '', '', '', 'covered-F', '', '',  # 7 slots
             '',  # extended
             'flat-F',  # flat
             '',  # index
             'adducted-F',  # modified
             'offset-F', 'open-F',  # offset, open
             'slanted-F', ''],  # slanted, spread
            ['',
             '',  # bent
             '', '', '', '', '', '', '',  # 7 slots
             '',  # extended
             'flat-open-F',  # flat
             '',  # index
             '',  # modified
             '', '',  # offset, open
             '', ''],  # slanted, spread
            ['',
             '',  # bent
             '', '', '', '', '', '', '',  # 7 slots
             '',  # extended
             'flat-clawed-F',  # flat
             '',  # index
             '',  # modified
             '', '',  # offset, open
             '', ''],  # slanted, spread
            ['G',
             '',  # bent
             '', 'closed-modified-G', '', '', '', '', '',  # 7 slots
             '',  # extended
             '',  # flat
             '',  # index
             'modified-G',  # modified
             '', '',  # offset, open
             '', ''],  # slanted, spread
            ['',
             '',  # bent
             '', 'closed-double-modified-G', '', '', '', '', '',  # 7 slots
             '',  # extended
             '',  # flat
             '',  # index
             'double-modified-G',  # modified
             '', '',  # offset, open
             '', ''],  # slanted, spread
            ['I',
             'bent-I',  # bent
             'clawed-I', '', 'combined-I+1', '', '', '', '',  # 7 slots
             '',  # extended
             'flat-combined-I+1',  # flat
             '',  # index
             '',  # modified
             '', '',  # offset, open
             '', ''],  # slanted, spread
            ['',
             'bent-combined-I+1',  # bent
             '', '', 'combined-ILY', '', '', '', '',  # 7 slots
             '',  # extended
             '',  # flat
             '',  # index
             '',  # modified
             '', '',  # offset, open
             '', ''],  # slanted, spread
            ['',
             '',  # bent
             '', '', 'combined-I+A', '', '', '', '',  # 7 slots
             '',  # extended
             '',  # flat
             '',  # index
             '',  # modified
             '', '',  # offset, open
             '', ''],  # slanted, spread
            ['K',
             '',  # bent
             '', '', '', '', '', '', '',  # 7 slots
             'extended-K',  # extended
             '',  # flat
             '',  # index
             '',  # modified
             '', '',  # offset, open
             '', ''],  # slanted, spread
            ['L',
             'bent-L',  # bent
             'clawed-L', '', '', 'contracted-L', '', 'crooked-L', '',  # 7 slots
             '',  # extended
             '',  # flat
             '',  # index
             '',  # modified
             '', '',  # offset, open
             '', ''],  # slanted, spread
            ['',
             'bent-thumb-L',  # bent
             '', '', '', 'double-contracted-L', '', '', '',  # 7 slots
             '',  # extended
             '',  # flat
             '',  # index
             '',  # modified
             '', '',  # offset, open
             '', ''],  # slanted, spread
            ['M',
             '',  # bent
             '', '', '', '', '', '', '',  # 7 slots
             '',  # extended
             'flat-M',  # flat
             '',  # index
             '',  # modified
             '', '',  # offset, open
             '', ''],  # slanted, spread
            ['N',
             '',  # bent
             '', '', '', '', '', '', '',  # 7 slots
             '',  # extended
             '',  # flat
             '',  # index
             '',  # modified
             '', '',  # offset, open
             '', ''],  # slanted, spread
            ['O',
             '',  # bent
             '', '', '', '', 'covered-O', '', '',  # 7 slots
             '',  # extended
             'flat-O',  # flat
             'O-index',  # index
             'modified-O',  # modified
             'offset-O', 'open-spread-O',  # offset, open
             '', ''],  # slanted, spread
            ['',
             '',  # bent
             '', '', '', '', '', '', '',  # 7 slots
             '',  # extended
             '',  # flat
             '',  # index
             '',  # modified
             '', 'open-O-index',  # offset, open
             '', ''],  # slanted, spread
            ['R',
             'bent-R',  # bent
             '', '', '', '', '', '', '',  # 7 slots
             'extended-R',  # extended
             '',  # flat
             '',  # index
             '',  # modified
             '', '',  # offset, open
             '', ''],  # slanted, spread
            ['S',
             '',  # bent
             '', '', '', '', '', '', '',  # 7 slots
             '',  # extended
             '',  # flat
             '',  # index
             '',  # modified
             '', '',  # offset, open
             '', ''],  # slanted, spread
            ['T',
             '',  # bent
             '', '', '', '', 'covered-T', '', '',  # 7 slots
             '',  # extended
             '',  # flat
             '',  # index
             '',  # modified
             '', '',  # offset, open
             '', ''],  # slanted, spread
            ['U',
             'bent-U',  # bent
             'clawed-U', '', 'combined-U&Y', 'contracted-U', '', 'crooked-U', '',  # 7 slots
             'extended-U',  # extended
             '',  # flat
             '',  # index
             '',  # modified
             '', '',  # offset, open
             '', ''],  # slanted, spread
            ['',
             'bent-extended-U',  # bent
             '', '', '', 'contracted-U-index', '', '', '',  # 7 slots
             '',  # extended
             '',  # flat
             '',  # index
             '',  # modified
             '', '',  # offset, open
             '', ''],  # slanted, spread
            ['V',
             'bent-V',  # bent
             'clawed-V', 'closed-V', '', '', '', 'crooked-V', '',  # 7 slots
             '',  # extended
             '',  # flat
             '',  # index
             '',  # modified
             '', '',  # offset, open
             'slanted-V', ''],  # slanted, spread
            ['',
             'bent-extended-V',  # bent
             'clawed-extended-V', '', '', '', '', 'crooked-extended-V', '',  # 7 slots
             '',  # extended
             '',  # flat
             '',  # index
             '',  # modified
             '', '',  # offset, open
             '', ''],  # slanted, spread
            ['W',
             '',  # bent
             'clawed-W', 'closed-W', '', '', '', 'crooked-W', '',  # 7 slots
             '',  # extended
             '',  # flat
             '',  # index
             '',  # modified
             '', '',  # offset, open
             '', ''],  # slanted, spread
            ['X',
             '',  # bent
             'closed-X', '', '', '', '', '', '',  # 7 slots
             'extended-X',  # extended
             '',  # flat
             '',  # index
             '',  # modified
             '', '',  # offset, open
             '', ''],  # slanted, spread
            ['Y',
             '',  # bent
             '', '', 'combined-Y&middle', '', '', '', '',  # 7 slots
             '',  # extended
             '',  # flat
             '',  # index
             'modified-Y',  # modified
             '', '',  # offset, open
             '', ''],  # slanted, spread

            ['1',
             'bent-1',  # bent
             'clawed-1', '', '', '', '', 'crooked-1', '',  # clawed, closed, combined, contracted, covered, crooked, curved (7 slots)
             '',  # extended
             '',  # flat
             '',  # index
             '',  # modified
             '', '',  # offset, open
             '', ''],  # slanted, spread
            ['',
             'bent-offset-1',  # bent
             '', '', '', '', '', '', '', # clawed, closed, combined, contracted, covered, crooked, curved (7 slots)
             '',  # extended
             '',  # flat
             '',  # index
             '',  # modified
             '', '',  # offset, open
             '', ''],  # slanted, spread
            ['3',
             '',  # bent
             'clawed-3', '', '', 'contracted-3', '', '', '',  # 7 slots
             '',  # extended
             '',  # flat
             '',  # index
             '',  # modified
             '', '',  # offset, open
             '', ''],  # slanted, spread
            ['4',
             'bent-4',  # bent
             'clawed-4', '', '', '', '', 'crooked-4', '',  # 7 slots
             '',  # extended
             '',  # flat
             '',  # index
             '',  # modified
             '', '',  # offset, open
             'slanted-4', ''],  # slanted, spread
            ['5',
             'bent-5',  # bent
             'clawed-5', '', '', 'contracted-5', '', 'crooked-5', '',  # 7 slots
             '',  # extended
             '',  # flat
             '',  # index
             'modified-5',  # modified
             '', '',  # offset, open
             'slanted-5', ''],  # slanted, spread
            ['',
             'bent-midfinger-5',  # bent
             '', '', '', 'relaxed-contracted-5', '', 'crooked-slanted-5', '',  # 7 slots
             '',  # extended
             '',  # flat
             '',  # index
             '',  # modified
             '', '',  # offset, open
             '', ''],  # slanted, spread
            ['6',
             '',  # bent
             '', '', '', '', '', '', '',  # 7 slots
             '',  # extended
             '',  # flat
             '',  # index
             '',  # modified
             '', '',  # offset, open
             '', ''],  # slanted, spread
            ['8',
             '',  # bent
             '', '', '', '', 'covered-8', '', '',  # 7 slots
             'extended-8',  # extended
             '',  # flat
             '',  # index
             '',  # modified
             '', 'open-8',  # offset, open
             '', ''],  # slanted, spread

            ['middle-finger',
             '',  # bent
             '', '', '', '', '', '', '',  # 7 slots
             '',  # extended
             '',  # flat
             '',  # index
             '',  # modified
             '', '',  # offset, open
             '', ''],  # slanted, spread
            ['base',
             '',  # bent
             '', '', '', '', '', '', '',  # 7 slots
             '',  # extended
             '',  # flat
             '',  # index
             '',  # modified
             '', '',  # offset, open
             '', '']  # slanted, spread
        ]

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.data_cached)

    def columnCount(self, parent=None, *args, **kwargs):
        return len(self.col_labels)

    def get_value(self, index):
        return self.data_cached[index.row()][index.column()]

    def data(self, index, role=None):
        if not index.isValid():
            return None

        value = self.get_value(index)
        if role == Qt.DisplayRole:# or role == Qt.EditRole:
            return PREDEFINED_MAP[value].name if value in PREDEFINED_MAP.keys() else None
        #elif role == Qt.TextAlignmentRole:
        #    return Qt.AlignCenter
        elif role == Qt.DecorationRole:
            return QIcon(self.predefined_images[value]) if value in PREDEFINED_MAP else None
        elif role == Qt.BackgroundRole:
            if value in {'1', '5', 'A', 'B1', 'B2', 'C', 'O', 'S'}:
                return QColor('#90ee90')
        return None

    def setData(self, index, value, role=None):
        if index.isValid() and role == Qt.EditRole:
            self.data_cached[index.row()][index.column()] = value
            self.dataChanged.emit(index, index)
            return True
        else:
            return False

    def headerData(self, section, orientation, role=None):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            header = self.col_labels[section]
            return header
        if orientation == Qt.Vertical and role == Qt.DisplayRole:
            return str(section + 1)

        return None


class FrozenTableView(QTableView):
    def __init__(self, predefined_images, drag_enabled=False, **kwargs):
        super().__init__(**kwargs)
        self.predefined_images = predefined_images
        self.setDragEnabled(drag_enabled)
        self.setDragDropMode(QAbstractItemView.DragOnly)
        self.setSelectionMode(QAbstractItemView.SingleSelection)

    def mouseMoveEvent(self, e):
        if self.dragEnabled():
            self.startDrag(e)
        else:
            super().mouseMoveEvent(e)

    def dragMoveEvent(self, event):
        #TODO: need to look into this
        if self.dragEnabled():
            if event.mimeData().hasText() and event.mimeData().hasImage():
                label = event.mimeData().text()
                if label in self.getSetOfItemLabels():
                    event.ignore()
                else:
                    event.setDropAction(Qt.CopyAction)
                    event.accept()
            else:
                event.ignore()
        else:
            super().dragMoveEvent(event)

    def startDrag(self, event):
        if self.dragEnabled():
            selectedshape = self.model().get_value(self.selectedIndexes()[0])
            symbol = str(selectedshape)
            icon = QPixmap(self.predefined_images[symbol])
            icon.scaled(100, 100)

            mime = QMimeData()
            mime.setImageData(QImage(self.predefined_images[symbol]))
            mime.setText(symbol)

            drag = QDrag(self)
            drag.setMimeData(mime)
            drag.setPixmap(icon)
            drag.setHotSpot(QPoint(icon.width() / 2, icon.height() / 2))
            drag.exec_(Qt.CopyAction)
        else:
            super().startDrag(event)


class PredefinedHandshapeView(QTableView):
    def __init__(self, predefined_images, drag_enabled=False, **kwargs):
        super().__init__(**kwargs)

        self.predefined_images = predefined_images
        self.setDragEnabled(drag_enabled)
        self.setDragDropMode(QAbstractItemView.DragOnly)
        self.setSelectionMode(QAbstractItemView.SingleSelection)

        # set the table model
        predefined_model = PredefinedTableModel(predefined_images, parent=self)
        self.setModel(predefined_model)

        # the following view is only for the first froze column
        self.frozen_table_view = FrozenTableView(predefined_images, drag_enabled=drag_enabled, parent=self)
        self.frozen_table_view.setModel(predefined_model)

        self.frozen_table_view.setIconSize(QSize(50, 50))
        self.frozen_table_view.verticalHeader().hide()
        self.frozen_table_view.setFocusPolicy(Qt.NoFocus)

        # so there are no scroll bars in the frozen panel
        self.frozen_table_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.frozen_table_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.frozen_table_view.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)

        # self.frozenTableView.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        #self.frozenTableView.setStyleSheet('''border: none; background-color: #CCC''')
        #self.frozen_table_view.setSelectionModel(QAbstractItemView.selectionModel(self))

        self.viewport().stackUnder(self.frozen_table_view)

        #self.setEditTriggers(QAbstractItemView.SelectedClicked)

        # style-related stuff
        self.setIconSize(QSize(50, 50))
        self.setShowGrid(False)
        self.setStyleSheet('font: 10pt')
        self.setAlternatingRowColors(True)

        self.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)

        horizontal_header = self.horizontalHeader()
        horizontal_header.setDefaultAlignment(Qt.AlignCenter)
        horizontal_header.setStretchLastSection(True)

        vertical_header = self.verticalHeader()
        vertical_header.setDefaultSectionSize(25)
        vertical_header.setDefaultAlignment(Qt.AlignCenter)
        vertical_header.setVisible(True)

        num_col = predefined_model.columnCount(self)
        for col in range(num_col):
            if col == 0:
                self.horizontalHeader().resizeSection(col, 100)
                # self.horizontalHeader().setSectionResizeMode(col, QHeaderView.Fixed)
                self.frozen_table_view.setColumnWidth(col, self.columnWidth(col))
            else:
                self.horizontalHeader().resizeSection(col, 125)
                self.frozen_table_view.setColumnHidden(col, True)

        #self.frozen_table_view.show()
        #self.updateFrozenTableGeometry()

        # connect the headers and scrollbars of both tableviews together
        self.horizontalHeader().sectionResized.connect(self.update_section_width)
        self.verticalHeader().sectionResized.connect(self.update_section_height)
        self.frozen_table_view.verticalScrollBar().valueChanged.connect(self.verticalScrollBar().setValue)
        self.verticalScrollBar().valueChanged.connect(self.frozen_table_view.verticalScrollBar().setValue)

        self.resizeRowsToContents()
        self.update_frozen_table_geometry()

        #self.makeMenu()
        #self.setContextMenuPolicy(Qt.CustomContextMenu)
        #self.customContextMenuRequested.connect(self.showContextMenu)

    def makeMenu(self):
        self.popMenu = QMenu(self)
        self.editHandshapeAct = QAction('Edit handshape', self, triggered=self.editHandshape)
        self.popMenu.addAction(self.editHandshapeAct)

    def editHandshape(self):
        pass

    def showContextMenu(self, point):
        # TODO: maybe need to initiate this...
        self.indexToBeEdited = self.indexAt(point)
        self.popMenu.exec_(self.mapToGlobal(point))

    def update_section_width(self, logical_index, old_size, new_size):
        if logical_index == 0:  # we're only concerned about the first column
            self.frozen_table_view.setColumnWidth(logical_index, new_size)
            self.update_frozen_table_geometry()

    def update_section_height(self, logical_index, old_size, new_size):
        self.frozen_table_view.setRowHeight(logical_index, new_size)

    def resizeEvent(self, event):
        self.update_frozen_table_geometry()
        super().resizeEvent(event)

    def scrollTo(self, index, hint=None):
        if index.column() >= 1:
            super().scrollTo(index, hint)

    def update_frozen_table_geometry(self):
        if self.verticalHeader().isVisible():
            self.frozen_table_view.setGeometry(self.verticalHeader().width() + self.frameWidth(),
                                             self.frameWidth(),
                                             self.columnWidth(0),
                                             self.viewport().height() + self.horizontalHeader().height())
        else:
            self.frozen_table_view.setGeometry(self.frameWidth(),
                                             self.frameWidth(),
                                             self.columnWidth(0),
                                             self.viewport().height() + self.horizontalHeader().height())

    #https://stackoverflow.com/questions/37496320/pyqt-dragging-item-from-list-view-and-dropping-to-table-view-the-drop-index-is
    def mouseMoveEvent(self, e):
        if self.dragEnabled():
            self.startDrag(e)
        else:
            super().mouseMoveEvent(e)

    def dragMoveEvent(self, event):
        #TODO: need to look into this
        if self.dragEnabled():
            if event.mimeData().hasText() and event.mimeData().hasImage():
                label = event.mimeData().text()
                if label in self.getSetOfItemLabels():
                    event.ignore()
                else:
                    event.setDropAction(Qt.CopyAction)
                    event.accept()
            else:
                event.ignore()
        else:
            super().dragMoveEvent(event)

    def startDrag(self, event):
        if self.dragEnabled():
            selectedshape = self.model().get_value(self.selectedIndexes()[0])
            symbol = str(selectedshape)
            icon = QPixmap(self.predefined_images[symbol])
            icon.scaled(100, 100)

            mime = QMimeData()
            mime.setImageData(QImage(self.predefined_images[symbol]))
            mime.setText(symbol)

            drag = QDrag(self)
            drag.setMimeData(mime)
            drag.setPixmap(icon)
            drag.setHotSpot(QPoint(icon.width() / 2, icon.height() / 2))
            drag.exec_(Qt.CopyAction)
        else:
            super().startDrag(event)

    '''
    def moveCursor(self, cursorAction, modifiers):
        current = QTableView.moveCursor(self, cursorAction, modifiers)
        x = self.visualRect(current).topLeft().x()
        frozen_width = self.frozenTableView.columnWidth(0) + self.frozenTableView.columnWidth(1)
        if cursorAction == self.MoveLeft and current.column() > 1 and x < frozen_width:
            new_value = self.horizontalScrollBar().value() + x - frozen_width
            self.horizontalScrollBar().setValue(new_value)
        return current
    '''


class PredefinedHandshapeDialog(QDialog):
    def __init__(self, predefined_images, **kwargs):
        super().__init__(**kwargs)
        self.resize(750, 750)
        self.setWindowTitle('Predefined Handshapes')
        self.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)

        # create table view
        self.table_view = PredefinedHandshapeView(predefined_images, parent=self)

        #self.table_view.clicked.connect(self.fillSlots)
        #self.table_view.frozenTableView.clicked.connect(self.fillSlots)
        #table.itemClicked.connect(self.fillSlots)

        # layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.table_view)
        self.setLayout(main_layout)

    def fillSlots(self, clicked):
        #TODO
        config1 = self.parent().configTabs.widget(0)
        config2 = self.parent().configTabs.widget(1)
        selected = self.parent().selected.checkedId()

        if selected == 1:
            transcription = config1.hand1Transcription
        elif selected == 2:
            transcription = config1.hand2Transcription
        elif selected == 3:
            transcription = config2.hand1Transcription
        elif selected == 4:
            transcription = config2.hand2Transcription

        for slot, symbol in zip(transcription.slots, PredefinedHandshapeDialog.handshape_mapping.get(clicked.data(), HandshapeEmpty).canonical):
            if slot.num == 1:
                slot.setChecked(False)
            else:
                slot.setText(symbol)
