from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QComboBox, QLineEdit, QListWidget, QCheckBox, QListWidgetItem
from PyQt5 import QtWidgets, QtCore
import sys


class QComboCheckBox(QComboBox):
    def __init__(self, *args):
        super(QComboCheckBox, self).__init__(*args)

    def UpdateComboBox(self, _len: int = None, _check_list: list = None):
        if _check_list is None or len(_check_list) == 0:
            _check_list = [True for i in range(_len)]
        for i, check in enumerate(_check_list):
            self.qCheckBox[i + 1].setChecked(check)

    def InitComboBox(self, first_item: str, first_item_icon: str, items: list, items_icon: list):
        self.items = items
        self.items_icon = items_icon

        self.items.insert(0, first_item)
        self.items_icon.insert(0, first_item_icon)
        self.setMaxVisibleItems(len(items))

        self.row_num = len(self.items)
        self.selectedrow_num = 0
        self.qCheckBox = []
        self.qLineEdit = QLineEdit()
        self.qLineEdit.setReadOnly(True)
        self.qListWidget = QListWidget()
        self.qListWidget.setSizeAdjustPolicy(QListWidget.AdjustToContents)

        self.addQCheckBox(0)
        self.qCheckBox[0].stateChanged.connect(self.All)
        for i in range(1, self.row_num):
            self.addQCheckBox(i)
            self.qCheckBox[i].stateChanged.connect(self.show)
        self.setModel(self.qListWidget.model())
        self.setView(self.qListWidget)
        self.setLineEdit(self.qLineEdit)
        self.qListWidget.setSpacing(0)
        self.qLineEdit.addAction(QIcon(first_item_icon), QLineEdit.LeadingPosition)
        self.UpdateComboBox(_len=len(self.items) - 1)
        self.setStyleSheet("QListWidget::item {margin-left: 5px;height:27px;}")

    def getState(self):
        all_list = []
        for i in range(len(self.qCheckBox)):
            all_list.append(self.qCheckBox[i].isChecked())
        return all_list

    def addQCheckBox(self, i):
        q = QCheckBox()
        q.setIconSize(QSize(27, 27))
        self.qCheckBox.append(q)
        qItem = QListWidgetItem(self.qListWidget)
        item_txt = self.items[i]
        for a in range(2):
            item_txt = "".join((item_txt, "\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t"
                                          "\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t"
                                          "\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t"))
        self.qCheckBox[i].setText(item_txt)
        self.qCheckBox[i].setIcon(QIcon(self.items_icon[i]))
        self.qListWidget.setItemWidget(qItem, self.qCheckBox[i])

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
        self.qLineEdit.setReadOnly(False)
        self.qLineEdit.clear()
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
        self.qLineEdit.setReadOnly(True)

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
            self.clear()

    def clear(self):
        for i in range(self.row_num):
            self.qCheckBox[i].setChecked(False)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    comboBox1 = QComboCheckBox(Form)

    items = ["Microsoft Word 97-2003 文件（.doc）",
             "Microsoft Word 文件（.docx）",
             "Microsoft Excel 97-2003 文件（.xls）",
             "Microsoft Excel 文件（.xlsx）",
             "PDF 文件（.pdf）",
             "文本文档（.txt）"
             ]
    items_icon = ["icon/doc.png",
                  "icon/docx.png",
                  "icon/xls.png",
                  "icon/xlsx.png",
                  "icon/pdf.png",
                  "icon/txt.png"
                  ]
    first_item = '全部文件类型'
    first_item_icon = 'icon/sysfile.png'
    line_edit_icon = "icon/sysfile.png"

    comboBox1.InitComboBox(
        line_edit_icon=line_edit_icon,
        first_item=first_item, first_item_icon=first_item_icon,
        items=items, items_icon=items_icon
    )

    comboBox1.setGeometry(QtCore.QRect(10, 10, 400, 40))
    comboBox1.setMinimumSize(QtCore.QSize(100, 20))
    Form.show()
    sys.exit(app.exec_())
