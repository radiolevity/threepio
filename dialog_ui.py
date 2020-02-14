# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'misc/new_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(300, 260)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.file_name_value = QtWidgets.QLineEdit(Dialog)
        font = QtGui.QFont()
        font.setFamily("SF Mono")
        self.file_name_value.setFont(font)
        self.file_name_value.setObjectName("file_name_value")
        self.gridLayout.addWidget(self.file_name_value, 8, 3, 1, 1)
        self.dialog_button_box = QtWidgets.QDialogButtonBox(Dialog)
        self.dialog_button_box.setOrientation(QtCore.Qt.Horizontal)
        self.dialog_button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.dialog_button_box.setObjectName("dialog_button_box")
        self.gridLayout.addWidget(self.dialog_button_box, 9, 1, 1, 3)
        self.end_time = QtWidgets.QDateTimeEdit(Dialog)
        font = QtGui.QFont()
        font.setFamily("SF Mono")
        self.end_time.setFont(font)
        self.end_time.setObjectName("end_time")
        self.gridLayout.addWidget(self.end_time, 1, 3, 1, 1)
        self.data_acquisition_rate_value = QtWidgets.QSpinBox(Dialog)
        font = QtGui.QFont()
        font.setFamily("SF Mono")
        self.data_acquisition_rate_value.setFont(font)
        self.data_acquisition_rate_value.setMaximum(999)
        self.data_acquisition_rate_value.setProperty("value", 10)
        self.data_acquisition_rate_value.setObjectName("data_acquisition_rate_value")
        self.gridLayout.addWidget(self.data_acquisition_rate_value, 6, 3, 1, 1)
        self.starting_dec = QtWidgets.QLineEdit(Dialog)
        font = QtGui.QFont()
        font.setFamily("SF Mono")
        self.starting_dec.setFont(font)
        self.starting_dec.setObjectName("starting_dec")
        self.gridLayout.addWidget(self.starting_dec, 2, 3, 1, 1)
        self.end_label = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.end_label.setFont(font)
        self.end_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.end_label.setObjectName("end_label")
        self.gridLayout.addWidget(self.end_label, 1, 1, 1, 1)
        self.end_dec_label = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.end_dec_label.setFont(font)
        self.end_dec_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.end_dec_label.setObjectName("end_dec_label")
        self.gridLayout.addWidget(self.end_dec_label, 4, 1, 1, 1)
        self.ending_dec = QtWidgets.QLineEdit(Dialog)
        font = QtGui.QFont()
        font.setFamily("SF Mono")
        self.ending_dec.setFont(font)
        self.ending_dec.setObjectName("ending_dec")
        self.gridLayout.addWidget(self.ending_dec, 4, 3, 1, 1)
        self.start_label = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.start_label.setFont(font)
        self.start_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.start_label.setObjectName("start_label")
        self.gridLayout.addWidget(self.start_label, 0, 1, 1, 1)
        self.line = QtWidgets.QFrame(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line.sizePolicy().hasHeightForWidth())
        self.line.setSizePolicy(sizePolicy)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 7, 1, 1, 3)
        self.data_acquisition_rate_label = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.data_acquisition_rate_label.setFont(font)
        self.data_acquisition_rate_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.data_acquisition_rate_label.setObjectName("data_acquisition_rate_label")
        self.gridLayout.addWidget(self.data_acquisition_rate_label, 6, 1, 1, 1)
        self.start_time = QtWidgets.QTimeEdit(Dialog)
        font = QtGui.QFont()
        font.setFamily("SF Mono")
        self.start_time.setFont(font)
        self.start_time.setObjectName("start_time")
        self.gridLayout.addWidget(self.start_time, 0, 3, 1, 1)
        self.file_name_label = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.file_name_label.setFont(font)
        self.file_name_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.file_name_label.setObjectName("file_name_label")
        self.gridLayout.addWidget(self.file_name_label, 8, 1, 1, 1)
        self.start_dec_label = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.start_dec_label.setFont(font)
        self.start_dec_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.start_dec_label.setObjectName("start_dec_label")
        self.gridLayout.addWidget(self.start_dec_label, 2, 1, 1, 1)
        self.data_acquisition_rate_label.setBuddy(self.data_acquisition_rate_value)

        self.retranslateUi(Dialog)
        self.dialog_button_box.rejected.connect(Dialog.reject)
        self.dialog_button_box.accepted.connect(Dialog.accept)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.start_time, self.end_time)
        Dialog.setTabOrder(self.end_time, self.starting_dec)
        Dialog.setTabOrder(self.starting_dec, self.ending_dec)
        Dialog.setTabOrder(self.ending_dec, self.data_acquisition_rate_value)
        Dialog.setTabOrder(self.data_acquisition_rate_value, self.file_name_value)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.end_time.setDisplayFormat(_translate("Dialog", "HH:mm:ss"))
        self.starting_dec.setPlaceholderText(_translate("Dialog", "degrees"))
        self.end_label.setText(_translate("Dialog", "Ending RA"))
        self.end_dec_label.setText(_translate("Dialog", "Ending Declination"))
        self.ending_dec.setPlaceholderText(_translate("Dialog", "degrees"))
        self.start_label.setText(_translate("Dialog", "Starting RA"))
        self.data_acquisition_rate_label.setText(_translate("Dialog", "Data Acquisition Rate"))
        self.start_time.setDisplayFormat(_translate("Dialog", "HH:mm:ss"))
        self.file_name_label.setText(_translate("Dialog", "File name"))
        self.start_dec_label.setText(_translate("Dialog", "Starting Declination"))
