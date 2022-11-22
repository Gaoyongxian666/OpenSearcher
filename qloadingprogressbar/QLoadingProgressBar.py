from PyQt5.QtWidgets import QProgressBar
from PyQt5.QtCore import QPropertyAnimation, QAbstractAnimation, QEasingCurve, pyqtProperty


class QLoadingProgressBar(QProgressBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__initUi()

    def __initUi(self):
        self.setValue(0)
        self.setTextVisible(False)
        self._loading = 0
        self.__animation = QPropertyAnimation(self,b"loading")

    def start(self):
        self.__animation.setStartValue(self.minimum())
        self.__animation.setEndValue(self.maximum())
        self.__animation.valueChanged.connect(self.__loading)
        self.__animation.setDuration(1000)
        self.__animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.__animation.start()

    # 没有用到loading
    @pyqtProperty(int)
    def loading(self):
        return self._loading

    @loading.setter
    def loading(self, pos):
        self._loading = pos
        self.update()

    def __loading(self, v):
        self.setValue(v)
        if self.__animation.currentValue() == self.__animation.endValue():
            self.__animation.setDirection(QAbstractAnimation.Backward)
            self.setInvertedAppearance(True)
            self.__animation.start()
        elif self.__animation.currentValue() == self.__animation.startValue():
            self.__animation.setDirection(QAbstractAnimation.Forward)
            self.setInvertedAppearance(False)
            self.__animation.start()

    def setAnimationType(self, type: str):
        if type == 'fade':
            self.setStyleSheet('''
                QProgressBar::chunk {
                    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 transparent, stop: 0.5 #CCCCCC, stop: 0.6 #CCCCCC, stop:1 transparent);
                }
            ''')
            self.__animation.setEasingCurve(QEasingCurve.Linear)
            self.__animation.setDuration(500)
        elif type == 'dynamic':
            self.setStyleSheet('')
            self.__animation.setEasingCurve(QEasingCurve.InOutQuad)
            self.__animation.setDuration(1000)

    def stop(self):
        self.__animation.stop()
