from PyQt5 import QtCore
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from qcustomdialog import customtype


class CustomTypeWindow(QMainWindow):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.child = customtype.Ui_MainWindow()
        self.child.setupUi(self)
        self.setWindowTitle("自定义类型")

        self.mysetting_dict = parent.mysetting_dict
        self.parent = parent

        self._text_types_dict = self.mysetting_dict["_text_types_dict"]
        self._image_types_dict = self.mysetting_dict["_image_types_dict"]
        self._text_types_list = self.mysetting_dict["_text_types_list"]
        self._image_types_list = self.mysetting_dict["_image_types_list"]
        self._types_dict = self.mysetting_dict["_types_dict"]

        self.child.comboBox_text.InitComboBox(self._text_types_dict)
        self.child.comboBox_image.InitComboBox(self._image_types_dict)
        self.child.cancel_button.clicked.connect(self.close)
        self.child.save_button.clicked.connect(self.save)
        self.child.lineEdit_text.setValidator(QRegExpValidator(QRegExp('^\.[a-zA-z0-9.;]+$'), self))
        self.child.lineEdit_image.setValidator(QRegExpValidator(QRegExp('^\.[a-zA-z0-9.;]+$'), self))
        self.child.lineEdit_text.setText(";".join(self._text_types_list))
        self.child.lineEdit_image.setText(";".join(self._image_types_list))

    def closeEvent(self, a0) -> None:
        self.parent.InitComboBox(self.mysetting_dict)
        super().closeEvent(a0)

    def save(self):
        self.comboBox_text_text = self.child.comboBox_text.text()
        self.comboBox_text_list = [x for x in self.comboBox_text_text.split(";") if x]
        self.lineEdit_text_text = self.child.lineEdit_text.text()
        self.lineEdit_text_list = [x for x in self.lineEdit_text_text.split(";") if x]
        self.comboBox_text_list.extend(self.lineEdit_text_list)
        for i in self.lineEdit_text_list:
            if i[0] != ".":
                QMessageBox.information(self, "提示", "文本文档中的自定义数据类型需要英文小数点作为前缀",
                                        QMessageBox.Ok)
                return

        self.comboBox_image_text = self.child.comboBox_image.text()
        self.comboBox_image_list = [x for x in self.comboBox_image_text.split(";") if x]
        self.lineEdit_image_text = self.child.lineEdit_image.text()
        self.lineEdit_image_list = [x for x in self.lineEdit_image_text.split(";") if x]
        self.comboBox_image_list.extend(self.lineEdit_image_list)
        for i in self.lineEdit_image_list:
            if i[0] != ".":
                QMessageBox.information(self, "提示", "图像元数据中的自定义数据类型需要英文小数点作为前缀",
                                        QMessageBox.Ok)
                return

        if len(self.comboBox_text_list) == 0:
            QMessageBox.information(self, "提示", "请至少选择一项 文本文档 的文件类型！", QMessageBox.Ok)
        elif len(self.comboBox_image_list) == 0:
            QMessageBox.information(self, "提示", "请至少选择一项 图像元数据 的文件类型！", QMessageBox.Ok)
        else:
            self._types_dict["txt"]["types"] = self.comboBox_text_list
            self._types_dict["image"]["types"] = self.comboBox_image_list
            self.mysetting_dict["_types_dict"] = self._types_dict
            for key in self._text_types_dict:
                self._text_types_dict[key]["state"] = False
            for key in self._image_types_dict:
                self._image_types_dict[key]["state"] = False

            for type in self.comboBox_text_list:
                if type in [".md", ".markdown"]:
                    type = ".md"
                try:
                    self._text_types_dict[type[1:]]["state"] = True
                except:
                    pass

            for type in self.comboBox_image_list:
                if type in [".jpg", ".jpeg"]:
                    type = ".jpg"
                try:
                    self._image_types_dict[type[1:]]["state"] = True
                except:
                    pass

            self.mysetting_dict["_text_types_dict"] = self._text_types_dict
            self.mysetting_dict["_image_types_dict"] = self._image_types_dict
            self.mysetting_dict["_text_types_list"] = self.lineEdit_text_list
            self.mysetting_dict["_image_types_list"] = self.lineEdit_image_list

            self.close()
