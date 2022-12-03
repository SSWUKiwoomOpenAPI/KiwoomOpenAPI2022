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

        self.realType = RealType()  #실시간 FID번호를 모아두는 곳
        
        ##등록된 계좌 전체 해제하기(작동정지되었을때 등록 정보를 다 끊어야 한다)
        self.k.kiwoom.dynamicCall("SetRealRemove(QString, QString)",["ALL","ALL"])
        
        ##키움서버에 리얼 데이터 등록하기
        self.screen_num = 5000
        for code in self.k.portfolio_stock_dict.keys():
            fids = self.realType.REALTYPE['주식체결']['체결시간']
            self.k.kiwoom.dynamicCall("SetRealReg(QString, QString, QString, QString)", self.screen_num, code, fids, "1")
            self.screen_num += 1

        print("종목등록 완료")
        print(self.k.portfolio_stock_dict.keys())

        ##현재 장 상태 알아보기(장 시작/장 마감 등)
        self.screen_start_stop_real = "300"  #장 시작 전/후 상태 확인용 스크린 번호
        self.k.kiwoom.dynamicCall("SetRealReg(QString, QString, QString,QString)", self.screen_start_stop_real,'',self.realType.REALTYPE['장시작시간']['장운영구분'],"0") #정보수신

        ##실시간 데이터를 받아오는 슬롯을 설정한다
        self.k.kiwoom.OnReceiveRealData.connect(self.realdata_slot) #실시간 데이터를 받아오는 곳

        self.k.kiwoom.OnReceiveChejanData.connect(self.chejan_slot)   # (주문접수, 체결통보)=0, (잔고변경) = 1 데이터 전송
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

    def realdata_slot(self, sCode, sRealType, sRealData):  # 실시간으로 서버에서 데이터들이 날라온다.

        if sRealType == "장시작시간":
            fid = self.realType.REALTYPE[sRealType]['장운영구분']

            # 실시간시세 데이터 수신 이벤트인 OnReceiveRealData() 가 발생될때 실시간데이터를 얻어오는 함수
            value = self.k.kiwoom.dynamicCall("GetCommRealData(QString, int)", sCode, fid)

            if value == '0':
                print("장 시작 전")

            elif value == '3':
                print("장 시작")

            elif value == '2':
                print("장 종료, 동시호가로 넘어감감")

            elif value == '4':
                print("장 마감했습니다.")
                    