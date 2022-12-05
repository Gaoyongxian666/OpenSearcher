from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QComboBox, QLineEdit, QListWidget, QCheckBox, QListWidgetItem


class QComboCustomBox(QComboBox):
    def __init__(self, *args):
        super(QComboCustomBox, self).__init__(*args)
        self.qCheckBox = []
        self.selectedrow_num = 0

        self.qLineEdit = QLineEdit()
        self.qLineEdit.setReadOnly(True)
        self.setLineEdit(self.qLineEdit)

        self.qListWidget = QListWidget()
        self.qListWidget.setSizeAdjustPolicy(QListWidget.AdjustToContents)
        self.setModel(self.qListWidget.model())
        self.setView(self.qListWidget)
        self.qListWidget.setSpacing(0)
        self.setStyleSheet("QListWidget::item {margin-left: 5px;height:26px;}")

    def InitComboBox(self, _types_dict):
        self.qListWidget.clear()
        self._types_dict = _types_dict
        self.row_num = len(self._types_dict)
        # self.setMaxVisibleItems(self.row_num + 1)
        self.setMaxVisibleItems(12)
        self.qLineEdit.addAction(QIcon(self._types_dict["all"]["icon"]), QLineEdit.LeadingPosition)
        for key, value in self._types_dict.items():
            self.addQCheckBox(key=key, value=value)
        for i, value in enumerate(self._types_dict.values()):
            self.qCheckBox[i].setChecked(value["state"])

    def addQCheckBox(self, key, value):
        name = value["name"]
        icon = value["icon"]
        types_ = value["types"]
        q = QCheckBox()
        if key == "all":
            q.stateChanged.connect(self.All)
        else:
            q.stateChanged.connect(self.show)
        q.setIconSize(QSize(22, 22))
        if len(types_) > 0:
            name = name + " （%s）" % ";".join(types_)
        for a in range(2):
            name = "".join((name, "\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t"
                                  "\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t"
                                  "\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t"))
        q.setText(name)
        q.setIcon(QIcon(icon))
        qItem = QListWidgetItem(self.qListWidget)
        self.qCheckBox.append(q)
        self.qListWidget.setItemWidget(qItem, q)

    def text(self):
        return self.qLineEdit.text()

    def getCheckItems(self):
        checkedItems = []
        for i in range(1, self.row_num):
            if self.qCheckBox[i].isChecked() == True:
                checkedItems.append(self.qCheckBox[i].text().strip())
        self.selectedrow_num = len(checkedItems)
        return checkedItems

    def show(self):
        show = ''
        Outputlist = self.getCheckItems()
        for i in Outputlist:
            show += i.split("（")[-1][:-1] + ';'
        if self.selectedrow_num == 0:
            self.qCheckBox[0].setCheckState(0)
        elif self.selectedrow_num == self.row_num - 1:
            self.qCheckBox[0].setCheckState(2)
        else:
            self.qCheckBox[0].setCheckState(1)
        self.qLineEdit.setText(show)
        self.qLineEdit.home(0)

    def get_text(self):
        return self.qLineEdit.text()

    def All(self, state):
        if state == 2:
            for i in range(1, self.row_num):
                self.qCheckBox[i].setChecked(True)
        elif state == 1:
            if self.selectedrow_num == 0:
                self.qCheckBox[0].setCheckState(2)
        elif state == 0:
            self.Clear()

    def Clear(self):
        for i in range(self.row_num):
            self.qCheckBox[i].setChecked(False)
