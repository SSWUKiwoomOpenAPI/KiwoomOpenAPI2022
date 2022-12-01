from PyQt5.QtCore import *           # eventloop/스레드를 사용 할 수 있는 함수 가져옴.
from kiwoom import Kiwoom            # 로그인을 위한 클래스
from PyQt5.QtWidgets import *        # PyQt import
from PyQt5.QtTest import *           # 시간관련 함수
from datetime import datetime, timedelta    # 특정 일자를 조회

<<<<<<< Updated upstream
class Thread2(Qthread):
=======
class Thread2(QThread):
>>>>>>> Stashed changes
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.k = Kiwoom() #키움서버함수사용 절대언어 참고


        self.Find_down_Screen = "1200"  # 계좌평가잔고내역을 받기위한 스크린
        self.code_in_all = None  # 1600개 코드 중 1개 코드, 쌓이지 않고 계속 갱신

        self.Predic_Screen = "1400"  #일봉차트를 가져오기위한 스크린
        self.calcul_data=[]          #받아온 종목의 값을 전부 저장(현재가/고가/저가)
        self.second_filter =[]       #역배열인지 확인
        self.Predict_star = []       #비교하기 위한 현재가만 넣어둠

        ###### 슬롯
        self.k.kiwoom.OnReceiveTrData.connect(self.trdata_slot)  # 내가 알고 있는 Tr 슬롯에다 특정 값을 던져 준다.

        ###### EventLoop
        self.detail_account_info_event_loop = QEventLoop()  # 계좌 이벤트루프

        ###### 기관외국인 평균가 가져오기
        self.C_K_F_class()

        ###### 역배열 평가
        self.Invers_arrangement()

    def C_K_F_class(self):

        code_list = []

        for code in self.k.acc_portfolio.keys():
            code_list.append(code)

<<<<<<< Updated upstream
        print("계좌 종목 개수 %s" % (code_list))
=======
        print("계좌 종목 개수 %s" % (code_list))

    
>>>>>>> Stashed changes
