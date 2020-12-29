from PyQt5.QtCore import (
    Qt,
    QAbstractListModel,
    pyqtSignal,
    QModelIndex,
    QItemSelectionModel
)

from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QListView,
    QVBoxLayout
)

#from PyQt5.QtGui import ()

class CorpusModel(QAbstractListModel):
    def __init__(self, glosses=None, **kwargs):
        super().__init__(**kwargs)
        self.glosses = glosses or []

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self.glosses[index.row()]

    def rowCount(self, index):
        return len(self.glosses)


class CorpusView(QWidget):
    selected_gloss = pyqtSignal(str)

    def __init__(self, corpus_title='Untitled', **kwargs):
        super().__init__(**kwargs)

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # TODO: maybe make this editable
        self.corpus_title = QLabel(corpus_title)
        main_layout.addWidget(self.corpus_title)

        self.corpus_model = CorpusModel(parent=self)
        self.corpus_view = QListView(parent=self)
        self.corpus_view.setModel(self.corpus_model)
        self.corpus_view.clicked.connect(self.handle_selection)
        main_layout.addWidget(self.corpus_view)

    def handle_selection(self, index):
        gloss = self.corpus_model.glosses[index.row()]
        self.selected_gloss.emit(gloss)

    def add_gloss(self, gloss):
        self.corpus_model.glosses.append(gloss)
        self.corpus_model.glosses.sort()
        self.corpus_model.layoutChanged.emit()

        index = self.corpus_model.glosses.index(gloss)

        # Ref: https://www.qtcentre.org/threads/32007-SetSelection-QListView-Pyqt
        self.corpus_view.selectionModel().setCurrentIndex(self.corpus_view.model().index(index, 0),
                                                          QItemSelectionModel.SelectCurrent)

    def remove_gloss(self, gloss):
        self.corpus_model.glosses.remove(gloss)
        self.corpus_model.layoutChanged.emit()
        self.corpus_view.clearSelection()

    def clear(self):
        self.corpus_title.setText('Untitled')

        self.corpus_model.glosses.clear()
        self.corpus_model.layoutChanged.emit()
        self.corpus_view.clearSelection()
