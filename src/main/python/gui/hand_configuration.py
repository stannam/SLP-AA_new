from PyQt5.QtCore import (
    Qt,
    QSize,
    pyqtSignal,
    QEvent
)
from PyQt5.QtWidgets import (
    QWidget,
    QLineEdit,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QGroupBox,
    QSizePolicy,
    QCompleter,
    QPushButton,
    QCheckBox,
    QAction,
    QMenu,
    QFrame
)

from itertools import chain
from constant import NULL, X_IN_BOX, ESTIMATE_BORDER, UNCERTAIN_BACKGROUND


class ConfigSlot(QLineEdit):
    slot_num_on_focus = pyqtSignal(str)
    slot_on_focus = pyqtSignal(str)
    slot_leave = pyqtSignal()

    def __init__(self, completer_options, descriptions, **kwargs):
        super().__init__(**kwargs)

        self.estimate = False
        self.uncertain = False
        self.setProperty('Estimate', self.estimate)
        self.setProperty('Uncertain', self.uncertain)

        # styling
        self.setFixedSize(QSize(20, 20))
        qss = """
            QLineEdit {{
                text-align: center;
                margin: 0;
                padding: 0;
            }}
            
            QLineEdit[Estimate=true][Uncertain=true] {{
                background: {uncertain_background};
                border: {estimate_border};
            }}
            
            QLineEdit[Estimate=true][Uncertain=false] {{
                background: white;
                border: {estimate_border};
            }}
            
            QLineEdit[Estimate=false][Uncertain=true] {{
                background: {uncertain_background};
                border: 1px solid grey;
            }}
            
            QLineEdit[Estimate=false][Uncertain=false] {{
                background: white;
                border: 1px solid grey;
            }}
        """.format(estimate_border=ESTIMATE_BORDER, uncertain_background=UNCERTAIN_BACKGROUND)
        self.setStyleSheet(qss)

        # set completer
        completer = QCompleter(completer_options, parent=self)
        completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        popup = completer.popup()
        popup.setFixedWidth(200)
        completer.setPopup(popup)
        self.setCompleter(completer)

        self.num = descriptions[1]
        self.description = 'Field type: {f_type}; Slot number: {s_num}; Slot type: {s_type}'.format(f_type=descriptions[0],
                                                                                                    s_num=descriptions[1],
                                                                                                    s_type=descriptions[2])

        # create menu
        self.create_flag_menu()
        self.textChanged.connect(self.on_text_changed)

    def create_flag_menu(self):
        self.flag_menu = QMenu(parent=self)

        self.flag_estimate_action = QAction('Flag as estimate', parent=self, triggered=self.flag_estimate, checkable=True)
        self.flag_uncertain_action = QAction('Flag as uncertain', parent=self, triggered=self.flag_uncertain, checkable=True)

        self.flag_menu.addActions([self.flag_estimate_action, self.flag_uncertain_action])

    def flag_estimate(self):
        self.estimate = self.flag_estimate_action.isChecked()
        self.setProperty('Estimate', self.estimate)

        self.setStyle(self.style())

    def flag_uncertain(self):
        self.uncertain = self.flag_uncertain_action.isChecked()
        self.setProperty('Uncertain', self.uncertain)

        self.setStyle(self.style())

    def contextMenuEvent(self, event):
        self.flag_menu.exec_(event.globalPos())

    def mousePressEvent(self, event):
        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.LeftButton:
                self.completer().complete()
        super().mousePressEvent(event)

    def focusInEvent(self, event):
        self.slot_on_focus.emit(self.description)
        self.slot_num_on_focus.emit(self.num)
        super().focusInEvent(event)

    def on_text_changed(self, text):
        self.setText(text.split(sep=' ')[0])
        self.repaint()

    def enterEvent(self, event):
        self.slot_on_focus.emit(self.description)
        self.slot_num_on_focus.emit(self.num)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.slot_leave.emit()
        super().leaveEvent(event)


class ConfigField(QWidget):
    slot_num_on_focus = pyqtSignal(str)
    slot_on_focus = pyqtSignal(str)
    slot_leave = pyqtSignal()

    def __init__(self, field_number, parent=None):
        super().__init__(parent=parent)
        self.field_number = field_number

        # styling
        self.setStyleSheet('QWidget{margin: 0; padding: 0}')

        self.main_layout = QHBoxLayout()
        self.main_layout.setSpacing(0)
        self.main_layout.addStretch()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.main_layout)

        # testing...
        left_bracket = QLabel('[')
        left_bracket.setFixedSize(QSize(10, 20))
        left_bracket.setAlignment(Qt.AlignHCenter)
        self.main_layout.addWidget(left_bracket)

        right_bracket = QLabel(']{}'.format(self.field_number))
        right_bracket.setFixedSize(QSize(15, 20))
        right_bracket.setAlignment(Qt.AlignHCenter)
        self.main_layout.addWidget(right_bracket)

        self.generate_slots()

    def insert_slot(self, slot):
        position = self.main_layout.count() - 1
        self.main_layout.insertWidget(position, slot)

    def __iter__(self):
        if self.field_number == 2:
            return [self.slot2, self.slot3, self.slot4, self.slot5].__iter__()
        elif self.field_number == 3:
            return [self.slot6, self.slot7, self.slot8, self.slot9, self.slot10, self.slot11, self.slot12, self.slot13, self.slot14, self.slot15].__iter__()
        elif self.field_number == 4:
            return [self.slot16, self.slot17, self.slot18, self.slot19].__iter__()
        elif self.field_number == 5:
            return [self.slot20, self.slot21, self.slot22, self.slot23, self.slot24].__iter__()
        elif self.field_number == 6:
            return [self.slot25, self.slot26, self.slot27, self.slot28, self.slot29].__iter__()
        elif self.field_number == 7:
            return [self.slot30, self.slot31, self.slot32, self.slot33, self.slot34].__iter__()

    def generate_slots(self):
        if self.field_number == 2:
            self.slot2 = ConfigSlot(['L [lateral]', 'U [unopposed]', 'O [opposed]', '? [unestimatable]'],
                                    ['thumb', '2', 'thumb oppositional positions (CM rotation)'],
                                    parent=self)
            self.slot2.slot_on_focus.connect(self.slot_on_focus.emit)
            self.slot2.slot_num_on_focus.connect(self.slot_num_on_focus.emit)
            self.slot2.slot_leave.connect(self.slot_leave.emit)
            self.insert_slot(self.slot2)

            self.slot3 = ConfigSlot(['{ [full abduction]', '< [neutral]', '= [adducted]', '? [unestimatable]'],
                                    ['thumb', '3', 'thumb abduction/adduction (CM adduction)'],
                                    parent=self)
            self.slot3.slot_on_focus.connect(self.slot_on_focus.emit)
            self.slot3.slot_num_on_focus.connect(self.slot_num_on_focus.emit)
            self.slot3.slot_leave.connect(self.slot_leave.emit)
            self.insert_slot(self.slot3)

            self.slot4 = ConfigSlot(['H [hyperextended]', 'E [fully extended]', 'e [somewhat extended]', 'i [clearly intermediate]', 'F [fully flexed]', 'f [somewhat flexed]', '? [unestimatable]'],
                                    ['thumb', '4', 'thumb MCP flexion'],
                                    parent=self)
            self.slot4.slot_on_focus.connect(self.slot_on_focus.emit)
            self.slot4.slot_num_on_focus.connect(self.slot_num_on_focus.emit)
            self.slot4.slot_leave.connect(self.slot_leave.emit)
            self.insert_slot(self.slot4)

            self.slot5 = ConfigSlot(['H [hyperextended]', 'E [fully extended]', 'e [somewhat extended]', 'i [clearly intermediate]', 'F [fully flexed]', 'f [somewhat flexed]', '? [unestimatable]'],
                                    ['thumb', '5', 'thumb DIP flexion'],
                                    parent=self)
            self.slot5.slot_on_focus.connect(self.slot_on_focus.emit)
            self.slot5.slot_num_on_focus.connect(self.slot_num_on_focus.emit)
            self.slot5.slot_leave.connect(self.slot_leave.emit)
            self.insert_slot(self.slot5)

        elif self.field_number == 3:
            self.slot6 = ConfigSlot(['- [no contact]', 't [tip]', 'fr [friction surface]', 'b [back surface]', 'r [radial surface]', 'u [ulnar surface]', '? [unestimatable]'],
                                    ['thumb/finger contact', '6', 'thumb surface options'],
                                    parent=self)
            self.slot6.slot_on_focus.connect(self.slot_on_focus.emit)
            self.slot6.slot_num_on_focus.connect(self.slot_num_on_focus.emit)
            self.slot6.slot_leave.connect(self.slot_leave.emit)
            self.insert_slot(self.slot6)

            self.slot7 = ConfigSlot(
                ['- [no contact]', 'd [distal]', 'p [proximal]', 'M [meta-carpal]', '? [unestimatable]'],
                ['thumb/finger contact', '7', 'thumb bone options'],
                parent=self)
            self.slot7.slot_on_focus.connect(self.slot_on_focus.emit)
            self.slot7.slot_num_on_focus.connect(self.slot_num_on_focus.emit)
            self.slot7.slot_leave.connect(self.slot_leave.emit)
            self.insert_slot(self.slot7)

            self.slot8 = ConfigSlot(
                [],
                ['thumb/finger contact', '8', 'what?'],
                parent=self)
            self.slot8.setText(NULL)
            self.slot8.setEnabled(False)
            self.slot8.slot_on_focus.connect(self.slot_on_focus.emit)
            self.slot8.slot_leave.connect(self.slot_leave.emit)
            self.insert_slot(self.slot8)

            self.slot9 = ConfigSlot(
                [],
                ['thumb/finger contact', '9', 'what?'],
                parent=self)
            self.slot9.setText('/')
            self.slot9.setEnabled(False)
            self.slot9.slot_on_focus.connect(self.slot_on_focus.emit)
            self.slot9.slot_leave.connect(self.slot_leave.emit)
            self.insert_slot(self.slot9)

            self.slot10 = ConfigSlot(['- [no contact]', 't [tip]', 'fr [friction surface]', 'b [back surface]', 'r [radial surface]', 'u [ulnar surface]', '? [unestimatable]'],
                                     ['thumb/finger contact', '10', 'finger surface options'],
                                     parent=self)
            self.slot10.slot_on_focus.connect(self.slot_on_focus.emit)
            self.slot10.slot_num_on_focus.connect(self.slot_num_on_focus.emit)
            self.slot10.slot_leave.connect(self.slot_leave.emit)
            self.insert_slot(self.slot10)

            self.slot11 = ConfigSlot(
                ['- [no contact]', 'd [distal]', 'm [medial]', 'p [proximal]', 'M [meta-carpal]', '? [unestimatable]'],
                ['thumb/finger contact', '11', 'finger bone options'],
                parent=self)
            self.slot11.slot_on_focus.connect(self.slot_on_focus.emit)
            self.slot11.slot_num_on_focus.connect(self.slot_num_on_focus.emit)
            self.slot11.slot_leave.connect(self.slot_leave.emit)
            self.insert_slot(self.slot11)

            self.slot12 = ConfigSlot(
                ['- [no contact]', '1 [contact with index finger]', '? [unestimatable]'],
                ['thumb/finger contact', '12', 'index/thumb contact'],
                parent=self)
            self.slot12.slot_on_focus.connect(self.slot_on_focus.emit)
            self.slot12.slot_num_on_focus.connect(self.slot_num_on_focus.emit)
            self.slot12.slot_leave.connect(self.slot_leave.emit)
            self.insert_slot(self.slot12)

            self.slot13 = ConfigSlot(
                ['- [no contact]', '2 [contact with middle finger]', '? [unestimatable]'],
                ['thumb/finger contact', '13', 'middle/thumb contact'],
                parent=self)
            self.slot13.slot_on_focus.connect(self.slot_on_focus.emit)
            self.slot13.slot_num_on_focus.connect(self.slot_num_on_focus.emit)
            self.slot13.slot_leave.connect(self.slot_leave.emit)
            self.insert_slot(self.slot13)

            self.slot14 = ConfigSlot(
                ['- [no contact]', '3 [contact with ring finger]', '? [unestimatable]'],
                ['thumb/finger contact', '14', 'ring/thumb contact'],
                parent=self)
            self.slot14.slot_on_focus.connect(self.slot_on_focus.emit)
            self.slot14.slot_num_on_focus.connect(self.slot_num_on_focus.emit)
            self.slot14.slot_leave.connect(self.slot_leave.emit)
            self.insert_slot(self.slot14)

            self.slot15 = ConfigSlot(
                ['- [no contact]', '4 [contact with pinky finger]', '? [unestimatable]'],
                ['thumb/finger contact', '15', 'pinky/thumb contact'],
                parent=self)
            self.slot15.slot_on_focus.connect(self.slot_on_focus.emit)
            self.slot15.slot_num_on_focus.connect(self.slot_num_on_focus.emit)
            self.slot15.slot_leave.connect(self.slot_leave.emit)
            self.insert_slot(self.slot15)
        elif self.field_number == 4:
            self.slot16 = ConfigSlot(
                [],
                ['index finger', '16', 'what?'],
                parent=self)
            self.slot16.setText('1')
            self.slot16.setEnabled(False)
            self.slot16.slot_on_focus.connect(self.slot_on_focus.emit)
            self.slot16.slot_leave.connect(self.slot_leave.emit)
            self.insert_slot(self.slot16)

            self.slot17 = ConfigSlot(
                ['H [hyperextended]', 'E [fully extended]', 'e [somewhat extended]', 'i [clearly intermediate]',
                 'F [fully flexed]', 'f [somewhat flexed]', '? [unestimatable]'],
                ['index finger', '17', 'index MCP flexion'],
                parent=self)
            self.slot17.slot_on_focus.connect(self.slot_on_focus.emit)
            self.slot17.slot_num_on_focus.connect(self.slot_num_on_focus.emit)
            self.slot17.slot_leave.connect(self.slot_leave.emit)
            self.insert_slot(self.slot17)

            self.slot18 = ConfigSlot(
                ['H [hyperextended]', 'E [fully extended]', 'e [somewhat extended]', 'i [clearly intermediate]',
                 'F [fully flexed]', 'f [somewhat flexed]', '? [unestimatable]'],
                ['index finger', '18', 'index PIP flexion'],
                parent=self)
            self.slot18.slot_on_focus.connect(self.slot_on_focus.emit)
            self.slot18.slot_num_on_focus.connect(self.slot_num_on_focus.emit)
            self.slot18.slot_leave.connect(self.slot_leave.emit)
            self.insert_slot(self.slot18)

            self.slot19 = ConfigSlot(
                ['H [hyperextended]', 'E [fully extended]', 'e [somewhat extended]', 'i [clearly intermediate]',
                 'F [fully flexed]', 'f [somewhat flexed]', '? [unestimatable]'],
                ['index finger', '19', 'index DIP flexion'],
                parent=self)
            self.slot19.slot_on_focus.connect(self.slot_on_focus.emit)
            self.slot19.slot_num_on_focus.connect(self.slot_num_on_focus.emit)
            self.slot19.slot_leave.connect(self.slot_leave.emit)
            self.insert_slot(self.slot19)
        elif self.field_number == 5:
            self.slot20 = ConfigSlot(
                ['{ [full abduction]', '< [neutral]', '= [adducted]', 'x- [slightly crossed with contact]',
                 'x [crossed with contact]', 'x+ [ultracrossed]', X_IN_BOX + ' [crossed without contact]', '? [unestimatable]'],
                ['middle finger', '20', 'index/middle contact'],
                parent=self)
            self.slot20.slot_on_focus.connect(self.slot_on_focus.emit)
            self.slot20.slot_num_on_focus.connect(self.slot_num_on_focus.emit)
            self.slot20.slot_leave.connect(self.slot_leave.emit)
            self.insert_slot(self.slot20)

            self.slot21 = ConfigSlot(
                [],
                ['middle finger', '21', 'what?'],
                parent=self)
            self.slot21.setText('2')
            self.slot21.setEnabled(False)
            self.slot21.slot_on_focus.connect(self.slot_on_focus.emit)
            self.slot21.slot_leave.connect(self.slot_leave.emit)
            self.insert_slot(self.slot21)

            self.slot22 = ConfigSlot(
                ['H [hyperextended]', 'E [fully extended]', 'e [somewhat extended]', 'i [clearly intermediate]',
                 'F [fully flexed]', 'f [somewhat flexed]', '? [unestimatable]'],
                ['middle finger', '22', 'middle MCP flexion'],
                parent=self)
            self.slot22.slot_on_focus.connect(self.slot_on_focus.emit)
            self.slot22.slot_num_on_focus.connect(self.slot_num_on_focus.emit)
            self.slot22.slot_leave.connect(self.slot_leave.emit)
            self.insert_slot(self.slot22)

            self.slot23 = ConfigSlot(
                ['H [hyperextended]', 'E [fully extended]', 'e [somewhat extended]', 'i [clearly intermediate]',
                 'F [fully flexed]', 'f [somewhat flexed]', '? [unestimatable]'],
                ['middle finger', '23', 'middle PIP flexion'],
                parent=self)
            self.slot23.slot_on_focus.connect(self.slot_on_focus.emit)
            self.slot23.slot_num_on_focus.connect(self.slot_num_on_focus.emit)
            self.slot23.slot_leave.connect(self.slot_leave.emit)
            self.insert_slot(self.slot23)

            self.slot24 = ConfigSlot(
                ['H [hyperextended]', 'E [fully extended]', 'e [somewhat extended]', 'i [clearly intermediate]',
                 'F [fully flexed]', 'f [somewhat flexed]', '? [unestimatable]'],
                ['middle finger', '24', 'middle DIP flexion'],
                parent=self)
            self.slot24.slot_on_focus.connect(self.slot_on_focus.emit)
            self.slot24.slot_num_on_focus.connect(self.slot_num_on_focus.emit)
            self.slot24.slot_leave.connect(self.slot_leave.emit)
            self.insert_slot(self.slot24)
        elif self.field_number == 6:
            self.slot25 = ConfigSlot(
                ['{ [full abduction]', '< [neutral]', '= [adducted]', 'x- [slightly crossed with contact]',
                 'x [crossed with contact]', 'x+ [ultracrossed]', X_IN_BOX + ' [crossed without contact]',
                 '? [unestimatable]'],
                ['ring finger', '25', 'middle/ring contact'],
                parent=self)
            self.slot25.slot_on_focus.connect(self.slot_on_focus.emit)
            self.slot25.slot_num_on_focus.connect(self.slot_num_on_focus.emit)
            self.slot25.slot_leave.connect(self.slot_leave.emit)
            self.insert_slot(self.slot25)

            self.slot26 = ConfigSlot(
                [],
                ['ring finger', '26', 'what?'],
                parent=self)
            self.slot26.setText('3')
            self.slot26.setEnabled(False)
            self.slot26.slot_on_focus.connect(self.slot_on_focus.emit)
            self.slot26.slot_leave.connect(self.slot_leave.emit)
            self.insert_slot(self.slot26)

            self.slot27 = ConfigSlot(
                ['H [hyperextended]', 'E [fully extended]', 'e [somewhat extended]', 'i [clearly intermediate]',
                 'F [fully flexed]', 'f [somewhat flexed]', '? [unestimatable]'],
                ['ring finger', '27', 'Ring MCP flexion'],
                parent=self)
            self.slot27.slot_on_focus.connect(self.slot_on_focus.emit)
            self.slot27.slot_num_on_focus.connect(self.slot_num_on_focus.emit)
            self.slot27.slot_leave.connect(self.slot_leave.emit)
            self.insert_slot(self.slot27)

            self.slot28 = ConfigSlot(
                ['H [hyperextended]', 'E [fully extended]', 'e [somewhat extended]', 'i [clearly intermediate]',
                 'F [fully flexed]', 'f [somewhat flexed]', '? [unestimatable]'],
                ['ring finger', '28', 'Ring PIP flexion'],
                parent=self)
            self.slot28.slot_on_focus.connect(self.slot_on_focus.emit)
            self.slot28.slot_num_on_focus.connect(self.slot_num_on_focus.emit)
            self.slot28.slot_leave.connect(self.slot_leave.emit)
            self.insert_slot(self.slot28)

            self.slot29 = ConfigSlot(
                ['H [hyperextended]', 'E [fully extended]', 'e [somewhat extended]', 'i [clearly intermediate]',
                 'F [fully flexed]', 'f [somewhat flexed]', '? [unestimatable]'],
                ['ring finger', '29', 'Ring DIP flexion'],
                parent=self)
            self.slot29.slot_on_focus.connect(self.slot_on_focus.emit)
            self.slot29.slot_num_on_focus.connect(self.slot_num_on_focus.emit)
            self.slot29.slot_leave.connect(self.slot_leave.emit)
            self.insert_slot(self.slot29)
        elif self.field_number == 7:
            self.slot30 = ConfigSlot(
                ['{ [full abduction]', '< [neutral]', '= [adducted]', 'x- [slightly crossed with contact]',
                 'x [crossed with contact]', 'x+ [ultracrossed]', X_IN_BOX + ' [crossed without contact]',
                 '? [unestimatable]'],
                ['pinky finger', '30', 'ring/pinky contact'],
                parent=self)
            self.slot30.slot_on_focus.connect(self.slot_on_focus.emit)
            self.slot30.slot_num_on_focus.connect(self.slot_num_on_focus.emit)
            self.slot30.slot_leave.connect(self.slot_leave.emit)
            self.insert_slot(self.slot30)

            self.slot31 = ConfigSlot(
                [],
                ['pinky finger', '31', 'what?'],
                parent=self)
            self.slot31.setText('4')
            self.slot31.setEnabled(False)
            self.slot31.slot_on_focus.connect(self.slot_on_focus.emit)
            self.slot31.slot_leave.connect(self.slot_leave.emit)
            self.insert_slot(self.slot31)

            self.slot32 = ConfigSlot(
                ['H [hyperextended]', 'E [fully extended]', 'e [somewhat extended]', 'i [clearly intermediate]',
                 'F [fully flexed]', 'f [somewhat flexed]', '? [unestimatable]'],
                ['pinky finger', '32', 'Pinky MCP flexion'],
                parent=self)
            self.slot32.slot_on_focus.connect(self.slot_on_focus.emit)
            self.slot32.slot_num_on_focus.connect(self.slot_num_on_focus.emit)
            self.slot32.slot_leave.connect(self.slot_leave.emit)
            self.insert_slot(self.slot32)

            self.slot33 = ConfigSlot(
                ['H [hyperextended]', 'E [fully extended]', 'e [somewhat extended]', 'i [clearly intermediate]',
                 'F [fully flexed]', 'f [somewhat flexed]', '? [unestimatable]'],
                ['pinky finger', '33', 'Pinky PIP flexion'],
                parent=self)
            self.slot33.slot_on_focus.connect(self.slot_on_focus.emit)
            self.slot33.slot_num_on_focus.connect(self.slot_num_on_focus.emit)
            self.slot33.slot_leave.connect(self.slot_leave.emit)
            self.insert_slot(self.slot33)

            self.slot34 = ConfigSlot(
                ['H [hyperextended]', 'E [fully extended]', 'e [somewhat extended]', 'i [clearly intermediate]',
                 'F [fully flexed]', 'f [somewhat flexed]', '? [unestimatable]'],
                ['pinky finger', '34', 'Pinky DIP flexion'],
                parent=self)
            self.slot34.slot_on_focus.connect(self.slot_on_focus.emit)
            self.slot34.slot_num_on_focus.connect(self.slot_num_on_focus.emit)
            self.slot34.slot_leave.connect(self.slot_leave.emit)
            self.insert_slot(self.slot34)


class ConfigHand(QWidget):
    slot_num_on_focus = pyqtSignal(str)
    slot_on_focus = pyqtSignal(str)
    slot_leave = pyqtSignal()
    def __init__(self, hand_number, parent=None):
        super().__init__(parent=parent)
        self.hand_number = hand_number
        self.setStyleSheet('QWidget{margin: 0; padding: 0}')

        self.main_layout = QHBoxLayout()
        self.main_layout.setSpacing(5)
        self.main_layout.addStretch()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.main_layout)

        self.generate_fields()

        clear_button = QPushButton('Clear', parent=self)
        clear_button.setFixedWidth(75)
        clear_button.setContentsMargins(0, 0, 0, 0)
        clear_button.clicked.connect(self.clear_transcription)
        self.main_layout.addWidget(clear_button)

    def __iter__(self):
        return chain(iter(self.field2), iter(self.field3), iter(self.field4), iter(self.field5), iter(self.field6), iter(self.field7))

    def get_list_transcription(self):
        return [slot.text() for slot in self.__iter__()]

    def get_string_transcription(self):
        return ''.join([slot.text() for slot in self.__iter__()])

    def clear_transcription(self):
        for slot in self.__iter__():
            if slot.num not in ['8', '9', '16', '21', '26', '31']:
                slot.clear()

    def generate_fields(self):
        self.field2 = ConfigField(2, parent=self)
        self.field2.slot_on_focus.connect(self.slot_on_focus.emit)
        self.field2.slot_num_on_focus.connect(self.slot_num_on_focus.emit)
        self.field2.slot_leave.connect(self.slot_leave.emit)
        self.main_layout.addWidget(self.field2)

        self.field3 = ConfigField(3, parent=self)
        self.field3.slot_on_focus.connect(self.slot_on_focus.emit)
        self.field3.slot_num_on_focus.connect(self.slot_num_on_focus.emit)
        self.field3.slot_leave.connect(self.slot_leave.emit)
        self.main_layout.addWidget(self.field3)

        self.field4 = ConfigField(4, parent=self)
        self.field4.slot_on_focus.connect(self.slot_on_focus.emit)
        self.field4.slot_num_on_focus.connect(self.slot_num_on_focus.emit)
        self.field4.slot_leave.connect(self.slot_leave.emit)
        self.main_layout.addWidget(self.field4)

        self.field5 = ConfigField(5, parent=self)
        self.field5.slot_on_focus.connect(self.slot_on_focus.emit)
        self.field5.slot_num_on_focus.connect(self.slot_num_on_focus.emit)
        self.field5.slot_leave.connect(self.slot_leave.emit)
        self.main_layout.addWidget(self.field5)

        self.field6 = ConfigField(6, parent=self)
        self.field6.slot_on_focus.connect(self.slot_on_focus.emit)
        self.field6.slot_num_on_focus.connect(self.slot_num_on_focus.emit)
        self.field6.slot_leave.connect(self.slot_leave.emit)
        self.main_layout.addWidget(self.field6)

        self.field7 = ConfigField(7, parent=self)
        self.field7.slot_on_focus.connect(self.slot_on_focus.emit)
        self.field7.slot_num_on_focus.connect(self.slot_num_on_focus.emit)
        self.field7.slot_leave.connect(self.slot_leave.emit)
        self.main_layout.addWidget(self.field7)


class Config(QGroupBox):
    slot_num_on_focus = pyqtSignal(str)
    slot_on_focus = pyqtSignal(str)
    slot_leave = pyqtSignal()

    def __init__(self, config_number, title, **kwargs):
        super().__init__(title=title, **kwargs)
        self.config_number = config_number
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        #self.setStyleSheet('QGroupBox{margin: 0; padding: 0}')

        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(5)
        self.main_layout.addStretch()
        #self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.main_layout)

        self.generate_hands()

    def generate_hands(self):
        self.hand1 = ConfigHand(1, parent=self)
        self.hand1.slot_on_focus.connect(self.slot_on_focus.emit)
        self.hand1.slot_num_on_focus.connect(self.slot_num_on_focus.emit)
        self.hand1.slot_leave.connect(self.slot_leave.emit)
        self.hand2 = ConfigHand(2, parent=self)
        self.hand2.slot_on_focus.connect(self.slot_on_focus.emit)
        self.hand2.slot_num_on_focus.connect(self.slot_num_on_focus.emit)
        self.hand2.slot_leave.connect(self.slot_leave.emit)

        self.main_layout.addWidget(self.hand1)
        self.main_layout.addWidget(self.hand2)


class ConfigGlobal(QGroupBox):
    slot_on_focus = pyqtSignal(str)
    slot_leave = pyqtSignal()

    def __init__(self, title='', **kwargs):
        super().__init__(title=title, **kwargs)

        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(5)
        self.main_layout.addStretch()
        self.setLayout(self.main_layout)
        self.add_slot1()
        self.add_options()
        self.add_other()

    def add_slot1(self):
        slot1_layout = QHBoxLayout()
        slot1_layout.addStretch()
        self.main_layout.addLayout(slot1_layout)

        left_bracket = QLabel('[')
        left_bracket.setFixedSize(QSize(10, 20))
        left_bracket.setAlignment(Qt.AlignHCenter)
        slot1_layout.addWidget(left_bracket)

        self.slot1 = QCheckBox('Forearm', parent=self)
        slot1_layout.addWidget(self.slot1)

        right_bracket = QLabel(']1')
        right_bracket.setFixedSize(QSize(15, 20))
        right_bracket.setAlignment(Qt.AlignHCenter)
        slot1_layout.addWidget(right_bracket)

    def add_options(self):
        option_frame = QGroupBox(parent=self)
        option_layout = QVBoxLayout()
        option_layout.setSpacing(5)
        option_layout.addStretch()
        option_frame.setLayout(option_layout)
        self.main_layout.addWidget(option_frame)
        self.estimated = QCheckBox('Estimated', parent=self)
        self.uncertain = QCheckBox('Uncertain', parent=self)
        self.incomplete = QCheckBox('Incomplete', parent=self)
        option_layout.addWidget(self.estimated)
        option_layout.addWidget(self.uncertain)
        option_layout.addWidget(self.incomplete)

    def add_other(self):
        other_group = QGroupBox(parent=self)
        other_layout = QVBoxLayout()
        other_layout.setSpacing(5)
        other_layout.addStretch()
        other_group.setLayout(other_layout)
        self.main_layout.addWidget(other_group)
        self.fingerspelled = QCheckBox('Fingerspelled', parent=self)
        self.initialized = QCheckBox('Initialized', parent=self)
        other_layout.addWidget(self.fingerspelled)
        other_layout.addWidget(self.initialized)
