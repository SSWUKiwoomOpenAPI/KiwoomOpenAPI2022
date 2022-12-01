from PyQt5.QtCore import *           # eventloop/스레드를 사용 할 수 있는 함수 가져옴.
from kiwoom import Kiwoom            # 로그인을 위한 클래스
from PyQt5.QtWidgets import *        # PyQt import
from PyQt5.QtTest import *           # 시간관련 함수
from datetime import datetime, timedelta    # 특정 일자를 조회

class Thread2(Qthread):
    def __init__(self, parent):     # 부모의 윈도운 창을 가져올 수 있다.
        super().__init__(parent)    # 부모 윈도우 창을 초기화
        self.parent = parent

        self.k = Kiwoom() #키움서버함수사용 절대언어 참고


        self.Find_down_Screen = "1200"  # 계좌평가잔고내역을 받기위한 스크린
        self.code_in_all = None  # 1600개 코드 중 1개 코드, 쌓이지 않고 계속 갱신

        self.Predict_Screen = "1400"
        self.calcul_data = []
        self.second_filter = []
        self.Predic_start = []

        ###### 슬롯
        self.k.kiwoom.OnReceiveTrData.connect(self.trdata_slot)  # 내가 알고 있는 Tr 슬롯에다 특정 값을 던져 준다.

        ###### EventLoop
        self.detail_account_info_event_loop = QEventLoop()  # 계좌 이벤트루프

        ###### 기관외국인 평균가 가져오기
        self.C_K_F_class()

    def C_K_F_class(self):

        code_list = []

        for code in self.k.acc_portfolio.keys():
            code_list.append(code)

        print("계좌 종목 개수 %s" % (code_list))

        for idx, code in enumerate(code_list):
            QTest.qWait(1000)

            self.k.kiwoom.dynamicCall("DisconnectRealData(QString)", self.Find_down_Screen)
            self.code_in_all = code  # 종목코드 선언 (중간에 코드 정보 받아오기 위해서)
            print("%s / %s : 종목 검사 중 코드이름 : %s." % (idx + 1, len(code_list), self.code_in_all))

            date_today = datetime.today().strftime("%Y%m%d")
            date_prev = datetime.today() - timedelta(10)  # 넉넉히 10일전의 데이터를 받아온다. 또는 20일이상 데이터도 필요
            date_prev = date_prev.strftime("%Y%m%d")

            self.k.kiwoom.dynamicCall("SetInputValue(QString, QString)", "종목코드", code)
            self.k.kiwoom.dynamicCall("SetInputValue(QString, QString)", "시작일자", date_prev)
            self.k.kiwoom.dynamicCall("SetInputValue(QString, QString)", "종료일자", date_today)
            self.k.kiwoom.dynamicCall("SetInputValue(QString, QString)", "기관추정단가구분", "1")
            self.k.kiwoom.dynamicCall("SetInputValue(QString, QString)", "외인추정단가구분", "1")
            self.k.kiwoom.dynamicCall("CommRqData(String, String, int, String)", "종목별기관매매추이요청2", "opt10045", "0", self.Find_down_Screen)
            self.detail_account_info_event_loop.exec_()

    def kigwan_meme_dong2(self, a, c):  # a. 기관일별순매수량, b. 종가/기관/외국인 평균가, c. 외국인일별순매수량, d. 등락률

        a = a[0:4]
        c = c[0:4]
        print(a)




        if a[0] < 0 and a[1] < 0 and a[2] < 0 and a[3] < 0 and c[0] < 0 and c[1] < 0 and c[2] < 0 and c[3] < 0:
            self.k.acc_portfolio[self.code_in_all].update({"위험도": "손절"})

        elif a[0] < 0 and a[1] < 0 and a[2] < 0 and c[0] < 0 and c[1] < 0 and c[2] < 0:
            self.k.acc_portfolio[self.code_in_all].update({"위험도": "주의"})

        elif a[0] < 0 and a[1] < 0 and c[0] < 0 and c[1] < 0:
            self.k.acc_portfolio[self.code_in_all].update({"위험도": "관심"})

        else:
            self.k.acc_portfolio[self.code_in_all].update({"위험도": "낮음"})


    def trdata_slot(self, sScrNo, sRQName, sTrCode, sRecordName, sPrevNext):

        if sRQName == "종목별기관매매추이요청2":

            cnt2 = self.k.kiwoom.dynamicCall("GetRepeatCnt(QString, QString)", sTrCode, sRQName)  # 10일치 이상을 하려면 이부분에 10일치 이상데이터 필요

            self.calcul2_data = []
            self.calcul2_data2 = []
            self.calcul2_data3 = []
            self.calcul2_data4 = []

            for i in range(cnt2):  #

                Kigwan_meme = (self.k.kiwoom.dynamicCall("GetCommData(String, String, int, String)", sTrCode, sRQName, i, "기관일별순매매수량"))
                Kigwan_meme_ave = (self.k.kiwoom.dynamicCall("GetCommData(String, String, int, String)", sTrCode, sRQName, 0, "기관추정평균가"))
                Forgin_meme = (self.k.kiwoom.dynamicCall("GetCommData(String, String, int, String)", sTrCode, sRQName, i, "외인일별순매매수량"))
                Forgin_meme_ave = (self.k.kiwoom.dynamicCall("GetCommData(String, String, int, String)", sTrCode, sRQName, 0, "외인추정평균가"))
                percentage = (self.k.kiwoom.dynamicCall("GetCommData(String, String, int, String)", sTrCode, sRQName, i, "등락율"))
                Jongga = (self.k.kiwoom.dynamicCall("GetCommData(String, String, int, String)", sTrCode, sRQName, i, "종가"))

                self.calcul2_data.append(int(Kigwan_meme.strip()))
                self.calcul2_data2.append(abs(int(Jongga.strip())))
                self.calcul2_data2.append(abs(int(Kigwan_meme_ave.strip())))
                self.calcul2_data2.append(abs(int(Forgin_meme_ave.strip())))
                self.calcul2_data3.append(int(Forgin_meme.strip()))
                self.calcul2_data4.append(float(percentage.strip()))

                
            self.kigwan_meme_dong2(self.calcul2_data, self.calcul2_data3)

            self.detail_account_info_event_loop.exit()
