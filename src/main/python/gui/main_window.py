import os
import pickle
from collections import defaultdict
from getpass import getuser
from datetime import date
from PyQt5.QtCore import (
    Qt,
    QSize,
    QSettings,
    QPoint
)
from PyQt5.QtWidgets import (
    QFileDialog,
    QMainWindow,
    QToolBar,
    QAction,
    QStatusBar,
    QSplitter,
    QScrollArea,
    QMessageBox
)
from PyQt5.QtGui import (
    QIcon,
    QKeySequence,
    QPixmap
)
from .initialization_dialog import InitializationDialog
from .corpus_view import CorpusView
from .location_definer import LocationDefinerDialog
from .panel import (
    LexicalInformationPanel,
    HandTranscriptionPanel,
    HandIllustrationPanel,
    ParameterPanel
)
from .decorator import check_unsaved_change, check_unsaved_corpus, check_duplicated_gloss
from constant import SAMPLE_LOCATIONS
from lexicon.lexicon_classes import (
    Corpus,
    Sign
)


# TODO: add undo/redo stack: https://doc.qt.io/qt-5/qtwidgets-tools-undoframework-example.html
# TODO: location image size problem
class MainWindow(QMainWindow):
    def __init__(self, app_ctx):
        super().__init__()
        self.app_ctx = app_ctx

        self.corpus = None
        self.current_sign = None

        # hand setting-related stuff
        self.handle_app_settings()
        self.check_storage()
        self.resize(self.app_settings['display']['size'])
        self.move(self.app_settings['display']['position'])

        #self.open_initialization_window()

        # date information
        self.today = date.today()

        # track unsaved changes
        self.unsaved_changes = True

        # app title
        self.setWindowTitle('Sign Language Phonetic Annotator and Analyzer')

        # toolbar
        toolbar = QToolBar('Main toolbar', parent=self)
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar)

        # actions
        # save
        action_save = QAction(QIcon(self.app_ctx.icons['save']), 'Save', parent=self)
        action_save.setStatusTip('Save')
        action_save.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_S))
        action_save.triggered.connect(self.on_action_save)
        action_save.setCheckable(False)

        # copy
        action_copy = QAction(QIcon(self.app_ctx.icons['copy']), 'Copy', parent=self)
        action_copy.setStatusTip('Copy the current sign')
        action_save.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_C))
        action_copy.triggered.connect(self.on_action_copy)
        action_copy.setCheckable(False)

        # paste
        action_paste = QAction(QIcon(self.app_ctx.icons['paste']), 'Paste', parent=self)
        action_paste.setStatusTip('Paste the copied sign')
        action_save.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_P))
        action_paste.triggered.connect(self.on_action_paste)
        action_paste.setCheckable(False)

        # define locations
        action_define_location = QAction('Define locations...', parent=self)
        action_define_location.setStatusTip('Open define location window')
        action_define_location.triggered.connect(self.on_action_define_location)
        action_define_location.setCheckable(False)

        # new corpus
        action_new_corpus = QAction('New corpus', parent=self)
        action_new_corpus.setStatusTip('Create a new corpus')
        action_new_corpus.triggered.connect(self.on_action_new_corpus)
        action_new_corpus.setCheckable(False)

        # load corpus
        action_load_corpus = QAction('Load corpus...', parent=self)
        action_load_corpus.setStatusTip('Load a .corpus file')
        action_save.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_L))
        action_load_corpus.triggered.connect(self.on_action_load_corpus)
        action_load_corpus.setCheckable(False)

        # close
        action_close = QAction('Close', parent=self)
        action_close.setStatusTip('Close the application')
        action_save.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_W))
        action_close.triggered.connect(self.on_action_close)
        action_close.setCheckable(False)

        # new sign
        action_new_sign = QAction(QIcon(self.app_ctx.icons['new_sign']), 'New sign', parent=self)
        action_new_sign.setStatusTip('Create a new sign')
        action_save.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_N))
        action_new_sign.triggered.connect(self.on_action_new_sign)
        action_new_sign.setCheckable(False)

        toolbar.addAction(action_new_sign)
        toolbar.addSeparator()
        toolbar.addAction(action_save)
        toolbar.addSeparator()
        toolbar.addAction(action_copy)
        toolbar.addAction(action_paste)

        # status bar
        self.status_bar = QStatusBar(parent=self)
        self.setStatusBar(self.status_bar)

        # menu
        main_menu = self.menuBar()

        menu_option = main_menu.addMenu('&Settings')
        menu_option.addAction(action_new_corpus)

        menu_file = main_menu.addMenu('&File')
        menu_file.addAction(action_new_corpus)
        menu_file.addAction(action_load_corpus)
        menu_file.addSeparator()
        menu_file.addAction(action_close)
        menu_file.addAction(action_save)
        menu_file.addSeparator()
        menu_file.addAction(action_new_sign)

        menu_edit = main_menu.addMenu('&Edit')
        menu_edit.addAction(action_copy)
        menu_edit.addAction(action_paste)

        menu_location = main_menu.addMenu('&Location')
        menu_location.addAction(action_define_location)

        central_splitter = QSplitter(Qt.Horizontal, parent=self)
        right_splitter = QSplitter(Qt.Vertical, parent=self)
        top_splitter = QSplitter(Qt.Horizontal, parent=self)
        bottom_splitter = QSplitter(Qt.Horizontal, parent=self)

        right_splitter.addWidget(top_splitter)
        right_splitter.addWidget(bottom_splitter)

        self.corpus_view = CorpusView('Untitled', parent=self)
        self.corpus_view.resize(QSize(100, 1000))
        self.corpus_view.selected_gloss.connect(self.handle_sign_selected)

        corpus_scroll = QScrollArea(parent=self)
        corpus_scroll.resize(QSize(100, 1000))
        corpus_scroll.setWidgetResizable(True)
        corpus_scroll.setWidget(self.corpus_view)

        self.lexical_scroll = LexicalInformationPanel(self.app_settings['metadata']['coder'], self.today, parent=self)

        self.illustration_scroll = HandIllustrationPanel(self.app_ctx, parent=self)

        self.transcription_scroll = HandTranscriptionPanel(parent=self)
        self.transcription_scroll.config1.slot_on_focus.connect(self.update_status_bar)
        self.transcription_scroll.config1.slot_num_on_focus.connect(self.update_hand_illustration)
        self.transcription_scroll.config1.slot_leave.connect(self.status_bar.clearMessage)
        self.transcription_scroll.config1.slot_leave.connect(self.illustration_scroll.set_neutral_img)

        self.transcription_scroll.config2.slot_on_focus.connect(self.update_status_bar)
        self.transcription_scroll.config2.slot_num_on_focus.connect(self.update_hand_illustration)
        self.transcription_scroll.config2.slot_leave.connect(self.status_bar.clearMessage)
        self.transcription_scroll.config2.slot_leave.connect(self.illustration_scroll.set_neutral_img)

        self.parameter_scroll = ParameterPanel(dict(), self.app_ctx, parent=self)

        top_splitter.addWidget(self.lexical_scroll)
        top_splitter.addWidget(self.transcription_scroll)
        bottom_splitter.addWidget(self.illustration_scroll)
        bottom_splitter.addWidget(self.parameter_scroll)

        central_splitter.addWidget(corpus_scroll)
        central_splitter.addWidget(right_splitter)

        self.setCentralWidget(central_splitter)

        self.open_initialization_window()

    def open_initialization_window(self):
        initialization = InitializationDialog(self.app_ctx, self.on_action_new_corpus, self.on_action_load_corpus, self.app_settings['metadata']['coder'], parent=self)
        response = initialization.exec_()
        if not response:  # close the window or press cancel
            self.on_action_new_corpus(False)

    def handle_sign_selected(self, gloss):
        selected_sign = self.corpus.get_sign_by_gloss(gloss)
        self.current_sign = selected_sign
        self.lexical_scroll.set_value(selected_sign.lexical_information)
        self.transcription_scroll.set_value(selected_sign.global_handshape_information,
                                            selected_sign.handshape_transcription)
        self.parameter_scroll.set_value(selected_sign.location)

    def handle_app_settings(self):
        self.app_settings = defaultdict(dict)

        self.app_qsettings = QSettings('UBC Phonology Tools',
                                       application='Sign Language Phonetic Annotator and Analyzer')

        self.app_qsettings.beginGroup('storage')
        self.app_settings['storage']['recent_folder'] = self.app_qsettings.value(
            'recent_folder',
            defaultValue=os.path.expanduser('~/Documents'))
        self.app_settings['storage']['corpora'] = self.app_qsettings.value('corpora',
                                                                           defaultValue=os.path.normpath(
                                                                               os.path.join(
                                                                                   os.path.expanduser('~/Documents'),
                                                                                   'PCT', 'SLP-AA', 'CORPORA')))
        self.app_settings['storage']['image'] = self.app_qsettings.value('image',
                                                                         defaultValue=os.path.normpath(
                                                                             os.path.join(
                                                                                 os.path.expanduser('~/Documents'),
                                                                                 'PCT', 'SLP-AA', 'IMAGE')))
        self.app_qsettings.endGroup()

        self.app_qsettings.beginGroup('display')
        self.app_settings['display']['size'] = self.app_qsettings.value('size', defaultValue=QSize(1200, 1000))
        self.app_settings['display']['position'] = self.app_qsettings.value('position', defaultValue=QPoint(50, 50))
        self.app_settings['display']['sig_figs'] = self.app_qsettings.value('sig_figs', defaultValue=3)
        self.app_settings['display']['tooltips'] = self.app_qsettings.value('tooltips', defaultValue=True)
        self.app_qsettings.endGroup()

        self.app_qsettings.beginGroup('metadata')
        self.app_settings['metadata']['coder'] = self.app_qsettings.value('coder', defaultValue=getuser())
        self.app_qsettings.endGroup()

    def check_storage(self):
        if not os.path.exists(self.app_settings['storage']['corpora']):
            os.makedirs(self.app_settings['storage']['corpora'])

        if not os.path.exists(self.app_settings['storage']['image']):
            os.makedirs(self.app_settings['storage']['image'])

    def save_app_settings(self):
        self.app_qsettings = QSettings('UBC Phonology Tools',
                                       application='Sign Language Phonetic Annotator and Analyzer')

        self.app_qsettings.beginGroup('storage')
        self.app_qsettings.setValue('recent_folder', self.app_settings['storage']['recent_folder'])
        self.app_qsettings.setValue('corpora', self.app_settings['storage']['corpora'])
        self.app_qsettings.setValue('image', self.app_settings['storage']['image'])
        self.app_qsettings.endGroup()

        self.app_qsettings.beginGroup('display')
        self.app_qsettings.setValue('size', self.size())
        self.app_qsettings.setValue('position', self.pos())
        self.app_qsettings.setValue('sig_figs', self.app_settings['display']['sig_figs'])
        self.app_qsettings.setValue('tooltips', self.app_settings['display']['tooltips'])
        self.app_qsettings.endGroup()

        self.app_qsettings.beginGroup('metadata')
        self.app_qsettings.setValue('coder', self.app_settings['metadata']['coder'])
        self.app_qsettings.endGroup()

    def on_action_define_location(self):
        location_definer = LocationDefinerDialog(self.corpus.location_definition, self.app_settings, self.app_ctx, parent=self)
        location_definer.saved_locations.connect(self.save_new_locations)
        location_definer.exec_()

    def save_new_locations(self, new_locations):
        #TODO: need to reimplement this once corpus class is there
        self.corpus.location_definition = new_locations
        self.parameter_scroll.clear(self.corpus.location_definition, self.app_ctx)

    def update_status_bar(self, text):
        self.status_bar.showMessage(text)

    def update_hand_illustration(self, num):
        hand_img = QPixmap(self.app_ctx.hand_illustrations['slot' + str(num)])
        self.illustration_scroll.set_img(hand_img)

    @check_duplicated_gloss
    @check_unsaved_corpus
    def on_action_save(self, clicked):
        lexical_info = self.lexical_scroll.get_value()
        location_transcription_info = self.parameter_scroll.location_layout.get_location_value()
        global_hand_info = self.transcription_scroll.global_info.get_value()
        configs = [self.transcription_scroll.config1.get_value(),
                   self.transcription_scroll.config2.get_value()]

        # if missing then some of them will be none
        if lexical_info and location_transcription_info and global_hand_info and configs:
            if self.current_sign:
                response = QMessageBox.question(self, 'Overwrite the current sign',
                                                'Do you want to overwrite the existing transcriptions?')
                if response == QMessageBox.Yes:
                    self.corpus.remove_sign(self.current_sign)
                else:
                    return

            new_sign = Sign(lexical_info, global_hand_info, configs, location_transcription_info)
            self.corpus.add_sign(new_sign)
            self.corpus_view.updated_glosses(self.corpus.get_sign_glosses(), new_sign.lexical_information.gloss)
            self.current_sign = new_sign

            self.corpus.name = self.corpus_view.corpus_title.text()
            self.save_corpus_binary()

    def save_corpus_binary(self):
        with open(self.corpus.path, 'wb') as f:
            pickle.dump(self.corpus, f, protocol=pickle.HIGHEST_PROTOCOL)

    def load_corpus_binary(self, path):
        with open(path, 'rb') as f:
            return pickle.load(f)

    def on_action_copy(self, clicked):
        pass
        #TODO: implement

    def on_action_paste(self, clicked):
        pass
        #TODO: implement

    def on_action_new_corpus(self, clicked):
        self.current_sign = None
        self.corpus = Corpus(signs=None, location_definition=SAMPLE_LOCATIONS)

        self.corpus_view.clear()
        self.lexical_scroll.clear(self.app_settings['metadata']['coder'])
        self.transcription_scroll.clear()
        self.parameter_scroll.clear(self.corpus.location_definition, self.app_ctx)

    def on_action_load_corpus(self, clicked):
        file_name, file_type = QFileDialog.getOpenFileName(self, self.tr('Open Corpus'), self.app_settings['storage']['recent_folder'],
                                                           self.tr('SLAP-AA Corpus (*.slpaa)'))
        folder, _ = os.path.split(file_name)
        if folder:
            self.app_settings['storage']['recent_folder'] = folder

        self.corpus = self.load_corpus_binary(file_name)

        first = self.corpus.get_sign_glosses()[0]
        self.parameter_scroll.clear(self.corpus.location_definition, self.app_ctx)
        self.corpus_view.updated_glosses(self.corpus.get_sign_glosses(), self.corpus.get_sign_by_gloss(first).lexical_information.gloss)
        self.corpus_view.selected_gloss.emit(self.corpus.get_sign_by_gloss(first).lexical_information.gloss)

        return bool(self.corpus)
        #TODO: implement

    def on_action_close(self, clicked):
        pass
        #TODO: implement

    def on_action_new_sign(self, clicked):
        self.current_sign = None

        self.lexical_scroll.clear(self.app_settings['metadata']['coder'])
        self.transcription_scroll.clear()
        self.parameter_scroll.clear(self.corpus.location_definition, self.app_ctx)

        self.corpus_view.corpus_view.clearSelection()

    @check_unsaved_change
    def closeEvent(self, event):
        self.save_app_settings()
        super().closeEvent(event)
