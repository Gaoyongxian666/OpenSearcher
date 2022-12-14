# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1277, 571)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        font = QtGui.QFont()
        font.setFamily("华文细黑")
        self.centralwidget.setFont(font)
        self.centralwidget.setStyleSheet("/*QPushButton {\n"
"    border: none; \n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #cce8f2;\n"
"}\n"
"*/")
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setContentsMargins(5, 5, 5, 5)
        self.gridLayout_2.setHorizontalSpacing(5)
        self.gridLayout_2.setVerticalSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("宋体")
        self.frame.setFont(font)
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setLineWidth(0)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setContentsMargins(3, 2, 3, 2)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_top = QtWidgets.QFrame(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_top.sizePolicy().hasHeightForWidth())
        self.frame_top.setSizePolicy(sizePolicy)
        self.frame_top.setMaximumSize(QtCore.QSize(1677777, 16777215))
        self.frame_top.setStyleSheet("")
        self.frame_top.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_top.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_top.setObjectName("frame_top")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_top)
        self.horizontalLayout_2.setContentsMargins(1, 1, 1, 1)
        self.horizontalLayout_2.setSpacing(2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frame_top_left = QtWidgets.QFrame(self.frame_top)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_top_left.sizePolicy().hasHeightForWidth())
        self.frame_top_left.setSizePolicy(sizePolicy)
        self.frame_top_left.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_top_left.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_top_left.setObjectName("frame_top_left")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_top_left)
        self.horizontalLayout_3.setContentsMargins(1, 1, 1, 1)
        self.horizontalLayout_3.setSpacing(2)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.show_all_button = QtWidgets.QToolButton(self.frame_top_left)
        self.show_all_button.setMinimumSize(QtCore.QSize(60, 60))
        self.show_all_button.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.show_all_button.setFont(font)
        self.show_all_button.setToolTipDuration(1000)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/icon/planning.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.show_all_button.setIcon(icon)
        self.show_all_button.setIconSize(QtCore.QSize(34, 36))
        self.show_all_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.show_all_button.setObjectName("show_all_button")
        self.horizontalLayout_3.addWidget(self.show_all_button)
        self.common_dir_button = QtWidgets.QToolButton(self.frame_top_left)
        self.common_dir_button.setMinimumSize(QtCore.QSize(60, 60))
        self.common_dir_button.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.common_dir_button.setFont(font)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icon/icon/folders.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.common_dir_button.setIcon(icon1)
        self.common_dir_button.setIconSize(QtCore.QSize(33, 33))
        self.common_dir_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.common_dir_button.setObjectName("common_dir_button")
        self.horizontalLayout_3.addWidget(self.common_dir_button)
        self.types_button = QtWidgets.QToolButton(self.frame_top_left)
        self.types_button.setMinimumSize(QtCore.QSize(60, 60))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icon/icon/types.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.types_button.setIcon(icon2)
        self.types_button.setIconSize(QtCore.QSize(35, 35))
        self.types_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.types_button.setObjectName("types_button")
        self.horizontalLayout_3.addWidget(self.types_button)
        self.help_button = QtWidgets.QToolButton(self.frame_top_left)
        self.help_button.setMinimumSize(QtCore.QSize(60, 60))
        self.help_button.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.help_button.setFont(font)
        self.help_button.setToolTipDuration(1000)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icon/icon/working.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.help_button.setIcon(icon3)
        self.help_button.setIconSize(QtCore.QSize(33, 33))
        self.help_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.help_button.setObjectName("help_button")
        self.horizontalLayout_3.addWidget(self.help_button)
        self.setting_button = QtWidgets.QToolButton(self.frame_top_left)
        self.setting_button.setMinimumSize(QtCore.QSize(60, 60))
        self.setting_button.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.setting_button.setFont(font)
        self.setting_button.setToolTipDuration(1000)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icon/icon/settings.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setting_button.setIcon(icon4)
        self.setting_button.setIconSize(QtCore.QSize(33, 33))
        self.setting_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.setting_button.setObjectName("setting_button")
        self.horizontalLayout_3.addWidget(self.setting_button)
        self.update_button = QtWidgets.QToolButton(self.frame_top_left)
        self.update_button.setMinimumSize(QtCore.QSize(60, 60))
        self.update_button.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.update_button.setFont(font)
        self.update_button.setToolTipDuration(1000)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/icon/icon/all-inclusive.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.update_button.setIcon(icon5)
        self.update_button.setIconSize(QtCore.QSize(35, 35))
        self.update_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.update_button.setObjectName("update_button")
        self.horizontalLayout_3.addWidget(self.update_button)
        spacerItem = QtWidgets.QSpacerItem(25, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.index_button = QtWidgets.QToolButton(self.frame_top_left)
        self.index_button.setMinimumSize(QtCore.QSize(60, 60))
        self.index_button.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.index_button.setFont(font)
        self.index_button.setToolTipDuration(1000)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/icon/icon/documents.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.index_button.setIcon(icon6)
        self.index_button.setIconSize(QtCore.QSize(33, 33))
        self.index_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.index_button.setObjectName("index_button")
        self.horizontalLayout_3.addWidget(self.index_button)
        self.scale_up_button = QtWidgets.QToolButton(self.frame_top_left)
        self.scale_up_button.setMinimumSize(QtCore.QSize(60, 60))
        self.scale_up_button.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.scale_up_button.setFont(font)
        self.scale_up_button.setToolTipDuration(1000)
        self.scale_up_button.setStyleSheet("")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/icon/icon/zoom-in.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.scale_up_button.setIcon(icon7)
        self.scale_up_button.setIconSize(QtCore.QSize(34, 34))
        self.scale_up_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.scale_up_button.setObjectName("scale_up_button")
        self.horizontalLayout_3.addWidget(self.scale_up_button)
        self.scale_down_button = QtWidgets.QToolButton(self.frame_top_left)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scale_down_button.sizePolicy().hasHeightForWidth())
        self.scale_down_button.setSizePolicy(sizePolicy)
        self.scale_down_button.setMinimumSize(QtCore.QSize(60, 60))
        self.scale_down_button.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.scale_down_button.setFont(font)
        self.scale_down_button.setToolTipDuration(1000)
        self.scale_down_button.setStyleSheet("")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/icon/icon/zoom-out.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.scale_down_button.setIcon(icon8)
        self.scale_down_button.setIconSize(QtCore.QSize(34, 34))
        self.scale_down_button.setShortcut("")
        self.scale_down_button.setCheckable(False)
        self.scale_down_button.setChecked(False)
        self.scale_down_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.scale_down_button.setObjectName("scale_down_button")
        self.horizontalLayout_3.addWidget(self.scale_down_button)
        self.horizontalLayout_2.addWidget(self.frame_top_left)
        self.frame_top_right = QtWidgets.QFrame(self.frame_top)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_top_right.sizePolicy().hasHeightForWidth())
        self.frame_top_right.setSizePolicy(sizePolicy)
        self.frame_top_right.setMinimumSize(QtCore.QSize(0, 0))
        self.frame_top_right.setMaximumSize(QtCore.QSize(450, 40))
        self.frame_top_right.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.frame_top_right.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_top_right.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_top_right.setObjectName("frame_top_right")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.frame_top_right)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setSpacing(3)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.progressBar = QLoadingProgressBar(self.frame_top_right)
        self.progressBar.setMaximumSize(QtCore.QSize(100, 16777215))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout_6.addWidget(self.progressBar)
        self.top_lable = QClickableLabel(self.frame_top_right)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.top_lable.sizePolicy().hasHeightForWidth())
        self.top_lable.setSizePolicy(sizePolicy)
        self.top_lable.setMinimumSize(QtCore.QSize(0, 0))
        self.top_lable.setMaximumSize(QtCore.QSize(16666, 16777215))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.top_lable.setFont(font)
        self.top_lable.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.top_lable.setObjectName("top_lable")
        self.horizontalLayout_6.addWidget(self.top_lable)
        self.horizontalLayout_2.addWidget(self.frame_top_right, 0, QtCore.Qt.AlignRight)
        self.verticalLayout.addWidget(self.frame_top)
        self.frame_center = QtWidgets.QFrame(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(19)
        sizePolicy.setHeightForWidth(self.frame_center.sizePolicy().hasHeightForWidth())
        self.frame_center.setSizePolicy(sizePolicy)
        self.frame_center.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_center.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_center.setObjectName("frame_center")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_center)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.splitter = QtWidgets.QSplitter(self.frame_center)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setObjectName("splitter")
        self.frame_center_left = QtWidgets.QFrame(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(4)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_center_left.sizePolicy().hasHeightForWidth())
        self.frame_center_left.setSizePolicy(sizePolicy)
        self.frame_center_left.setMinimumSize(QtCore.QSize(200, 0))
        self.frame_center_left.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_center_left.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_center_left.setObjectName("frame_center_left")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.frame_center_left)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.listView_all = QFileListView(self.frame_center_left)
        self.listView_all.setObjectName("listView_all")
        self.verticalLayout_6.addWidget(self.listView_all)
        self.frame_center_center = QtWidgets.QFrame(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(8)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_center_center.sizePolicy().hasHeightForWidth())
        self.frame_center_center.setSizePolicy(sizePolicy)
        self.frame_center_center.setMinimumSize(QtCore.QSize(380, 0))
        self.frame_center_center.setMaximumSize(QtCore.QSize(1677777, 16777215))
        self.frame_center_center.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_center_center.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_center_center.setObjectName("frame_center_center")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_center_center)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame_search = QtWidgets.QFrame(self.frame_center_center)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_search.sizePolicy().hasHeightForWidth())
        self.frame_search.setSizePolicy(sizePolicy)
        self.frame_search.setMaximumSize(QtCore.QSize(16777215, 70))
        self.frame_search.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_search.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_search.setObjectName("frame_search")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame_search)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(6)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.textEdit_keywords = QtWidgets.QLineEdit(self.frame_search)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit_keywords.sizePolicy().hasHeightForWidth())
        self.textEdit_keywords.setSizePolicy(sizePolicy)
        self.textEdit_keywords.setMinimumSize(QtCore.QSize(0, 30))
        self.textEdit_keywords.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.textEdit_keywords.setFont(font)
        self.textEdit_keywords.setStyleSheet("font: 12pt \"宋体\";")
        self.textEdit_keywords.setText("")
        self.textEdit_keywords.setObjectName("textEdit_keywords")
        self.horizontalLayout_4.addWidget(self.textEdit_keywords)
        self.search_button = QtWidgets.QPushButton(self.frame_search)
        self.search_button.setMinimumSize(QtCore.QSize(0, 30))
        self.search_button.setMaximumSize(QtCore.QSize(70, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.search_button.setFont(font)
        self.search_button.setObjectName("search_button")
        self.horizontalLayout_4.addWidget(self.search_button)
        self.verticalLayout_2.addWidget(self.frame_search)
        self.frame_dir = QtWidgets.QFrame(self.frame_center_center)
        self.frame_dir.setMinimumSize(QtCore.QSize(0, 0))
        self.frame_dir.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_dir.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_dir.setObjectName("frame_dir")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.frame_dir)
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_7.setSpacing(6)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_2 = QtWidgets.QLabel(self.frame_dir)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_7.addWidget(self.label_2, 0, QtCore.Qt.AlignLeft)
        self.comboBox_dir = QComboDirBox(self.frame_dir)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_dir.sizePolicy().hasHeightForWidth())
        self.comboBox_dir.setSizePolicy(sizePolicy)
        self.comboBox_dir.setMinimumSize(QtCore.QSize(0, 30))
        self.comboBox_dir.setObjectName("comboBox_dir")
        self.horizontalLayout_7.addWidget(self.comboBox_dir)
        self.verticalLayout_2.addWidget(self.frame_dir)
        self.frame_screen = QtWidgets.QFrame(self.frame_center_center)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_screen.sizePolicy().hasHeightForWidth())
        self.frame_screen.setSizePolicy(sizePolicy)
        self.frame_screen.setMaximumSize(QtCore.QSize(16777215, 40))
        self.frame_screen.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_screen.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_screen.setObjectName("frame_screen")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.frame_screen)
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_8.setSpacing(6)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label = QtWidgets.QLabel(self.frame_screen)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout_8.addWidget(self.label)
        self.comboBox_type = QComboCheckBox(self.frame_screen)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_type.sizePolicy().hasHeightForWidth())
        self.comboBox_type.setSizePolicy(sizePolicy)
        self.comboBox_type.setMinimumSize(QtCore.QSize(200, 30))
        self.comboBox_type.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.comboBox_type.setFont(font)
        self.comboBox_type.setObjectName("comboBox_type")
        self.horizontalLayout_8.addWidget(self.comboBox_type)
        self.verticalLayout_2.addWidget(self.frame_screen)
        self.splitter_2 = QtWidgets.QSplitter(self.frame_center_center)
        self.splitter_2.setOrientation(QtCore.Qt.Vertical)
        self.splitter_2.setHandleWidth(3)
        self.splitter_2.setObjectName("splitter_2")
        self.tableView = QFileTableView(self.splitter_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(7)
        sizePolicy.setHeightForWidth(self.tableView.sizePolicy().hasHeightForWidth())
        self.tableView.setSizePolicy(sizePolicy)
        self.tableView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.tableView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.tableView.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerItem)
        self.tableView.setGridStyle(QtCore.Qt.NoPen)
        self.tableView.setWordWrap(True)
        self.tableView.setObjectName("tableView")
        self.tableView.horizontalHeader().setDefaultSectionSize(300)
        self.tableView.horizontalHeader().setSortIndicatorShown(False)
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.listView_error = QFileListView(self.splitter_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(3)
        sizePolicy.setHeightForWidth(self.listView_error.sizePolicy().hasHeightForWidth())
        self.listView_error.setSizePolicy(sizePolicy)
        self.listView_error.setObjectName("listView_error")
        self.verticalLayout_2.addWidget(self.splitter_2)
        self.frame_center_right = QtWidgets.QFrame(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(10)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_center_right.sizePolicy().hasHeightForWidth())
        self.frame_center_right.setSizePolicy(sizePolicy)
        self.frame_center_right.setMinimumSize(QtCore.QSize(300, 0))
        self.frame_center_right.setStyleSheet("")
        self.frame_center_right.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_center_right.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_center_right.setObjectName("frame_center_right")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.frame_center_right)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.textframe = QTextFrame(self.frame_center_right)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textframe.sizePolicy().hasHeightForWidth())
        self.textframe.setSizePolicy(sizePolicy)
        self.textframe.setMinimumSize(QtCore.QSize(300, 0))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.textframe.setFont(font)
        self.textframe.setFrameShape(QtWidgets.QFrame.Box)
        self.textframe.setFrameShadow(QtWidgets.QFrame.Raised)
        self.textframe.setObjectName("textframe")
        self.verticalLayout_7.addWidget(self.textframe)
        self.horizontalLayout.addWidget(self.splitter)
        self.verticalLayout.addWidget(self.frame_center)
        self.frame_bottom = QtWidgets.QFrame(self.frame)
        self.frame_bottom.setMinimumSize(QtCore.QSize(0, 20))
        self.frame_bottom.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.frame_bottom.setFont(font)
        self.frame_bottom.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_bottom.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_bottom.setLineWidth(0)
        self.frame_bottom.setObjectName("frame_bottom")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.frame_bottom)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setSpacing(2)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.show_error_button = QtWidgets.QPushButton(self.frame_bottom)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.show_error_button.sizePolicy().hasHeightForWidth())
        self.show_error_button.setSizePolicy(sizePolicy)
        self.show_error_button.setMaximumSize(QtCore.QSize(20, 20))
        self.show_error_button.setText("")
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/icon/icon/remind.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.show_error_button.setIcon(icon9)
        self.show_error_button.setIconSize(QtCore.QSize(13, 13))
        self.show_error_button.setObjectName("show_error_button")
        self.horizontalLayout_5.addWidget(self.show_error_button)
        self.bottom_lable = QtWidgets.QLabel(self.frame_bottom)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bottom_lable.sizePolicy().hasHeightForWidth())
        self.bottom_lable.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.bottom_lable.setFont(font)
        self.bottom_lable.setWordWrap(True)
        self.bottom_lable.setObjectName("bottom_lable")
        self.horizontalLayout_5.addWidget(self.bottom_lable)
        self.verticalLayout.addWidget(self.frame_bottom)
        self.gridLayout_2.addWidget(self.frame, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.show_all_button.setToolTip(_translate("MainWindow", "显示全部"))
        self.show_all_button.setText(_translate("MainWindow", "显示全部"))
        self.common_dir_button.setText(_translate("MainWindow", "目录管理"))
        self.types_button.setText(_translate("MainWindow", "文件类型"))
        self.help_button.setToolTip(_translate("MainWindow", "使用说明"))
        self.help_button.setText(_translate("MainWindow", "使用说明"))
        self.setting_button.setToolTip(_translate("MainWindow", "设置"))
        self.setting_button.setText(_translate("MainWindow", "软件设置"))
        self.update_button.setToolTip(_translate("MainWindow", "检查更新"))
        self.update_button.setText(_translate("MainWindow", "检查更新"))
        self.index_button.setToolTip(_translate("MainWindow", "建立索引"))
        self.index_button.setText(_translate("MainWindow", "建立索引"))
        self.scale_up_button.setToolTip(_translate("MainWindow", "放大"))
        self.scale_up_button.setText(_translate("MainWindow", "放大"))
        self.scale_down_button.setToolTip(_translate("MainWindow", "缩小"))
        self.scale_down_button.setText(_translate("MainWindow", "缩小"))
        self.top_lable.setText(_translate("MainWindow", "搜索就绪"))
        self.textEdit_keywords.setPlaceholderText(_translate("MainWindow", "请输入关键词，回车"))
        self.search_button.setText(_translate("MainWindow", "搜索"))
        self.label_2.setText(_translate("MainWindow", "目录："))
        self.label.setText(_translate("MainWindow", "类型："))
        self.show_error_button.setToolTip(_translate("MainWindow", "显示错误"))
        self.bottom_lable.setText(_translate("MainWindow", "准备就绪！"))
from qclickablelabel import QClickableLabel
from qcombocheckbox import QComboCheckBox
from qcombodirbox import QComboDirBox
from qfilelistview import QFileListView
from qfiletableview import QFileTableView
from qloadingprogressbar import QLoadingProgressBar
from qtextframe import QTextFrame
import icon_rc
