import os
from PyQt5.QtCore import *
from kiwoom import Kiwoom
from kiwoomType import *

class Thread3(QThread):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.k = Kiwoom()           #절대언어 불러옴

        account = self.parent.accComboBox.currentText()
        self.account_num = account  #계좌번호 가져오기
  
        self.Load_code() #매수 종목/금액/수량 가져오기

    def Lode_code(self):
        if os.path.exists("dist/Seclected_code.txt"):
            f = open("dist/Selected_code.txt","r",encoding = "utf8")
            lines = f.readlines()
            screen =4000