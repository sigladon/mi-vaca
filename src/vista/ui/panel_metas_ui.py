# Form implementation generated from reading ui file 'panel_metas.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_PanelMetas(object):
    def setupUi(self, PanelMetas):
        PanelMetas.setObjectName("PanelMetas")
        PanelMetas.resize(523, 247)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(PanelMetas)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(parent=PanelMetas)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(parent=PanelMetas)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.btn_nueva_meta = QtWidgets.QPushButton(parent=PanelMetas)
        self.btn_nueva_meta.setObjectName("btn_nueva_meta")
        self.horizontalLayout.addWidget(self.btn_nueva_meta)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.contenedor_metas = QtWidgets.QScrollArea(parent=PanelMetas)
        self.contenedor_metas.setWidgetResizable(True)
        self.contenedor_metas.setObjectName("contenedor_metas")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 511, 183))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.widget = QtWidgets.QWidget(parent=self.scrollAreaWidgetContents)
        self.widget.setObjectName("widget")
        self.verticalLayout_3.addWidget(self.widget)
        self.contenedor_metas.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_2.addWidget(self.contenedor_metas)

        self.retranslateUi(PanelMetas)
        QtCore.QMetaObject.connectSlotsByName(PanelMetas)

    def retranslateUi(self, PanelMetas):
        _translate = QtCore.QCoreApplication.translate
        PanelMetas.setWindowTitle(_translate("PanelMetas", "Form"))
        self.label.setText(_translate("PanelMetas", "Metas Financieras"))
        self.label_2.setText(_translate("PanelMetas", "Define y rastrea tus objetivos de ahorro e inversión"))
        self.btn_nueva_meta.setText(_translate("PanelMetas", "Nueva Meta"))
