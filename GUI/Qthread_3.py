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
            for line in lines:
                if line != "":
                    ls = line.split("\t")
                    t_code = ls[0]
                    t_name = ls[1]
                    curren_price = ls[2]
                    dept = ls[3]
                    mesu = ls[4]
                    n_o_stock = ls[5]
                    profit = ls[6]
                    loss = ls[7].split("\n")[0]

                    self.k.portfolio_stock_dict.update({t_code:{"종목명":t_name}})
                    self.k.portfolio_stock_dict[t_code].update({"현재가":int(curren_price)})
                    self.k.portfolio_stock_dict[t_code].update({"신용비율":dept}) 
                    self.k.portfolio_stock_dict[t_code].update({"매수가":int(mesu)})
                    self.k.portfolio_stock_dict[t_code].update({"매수수량":int(n_o_stock)})  
                    self.k.portfolio_stock_dict[t_code].update({"익절가":int(profit)})  
                    self.k.portfolio_stock_dict[t_code].update({"손절가":int(loss)})  
                    self.k.portfolio_stock_dict[t_code].update({"주문용스크린번호":screen})  
                    screen += 1

            f.close()

                    