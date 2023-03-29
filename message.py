from bs4 import BeautifulSoup

import datetime
import json
import random
import requests
import time
import xmltodict

def getReplyMessage(message):
    strResult = ""

    if "아.." in message:
        strResult = messageAh()
    elif "응애" in message:
        strResult = messageBaby()
    elif "불편" in message:
        strResult = messageBoolpyeon()
    elif "학사일정" in message:
        strResult = messageCAUCalendar()
    elif "열람실" in message:
        if "서울" in message:
            strResult = messageCAULibrary("1")
        elif "법학" in message:
            strResult = messageCAULibrary("2")
        elif "안성" in message:
            strResult = messageCAULibrary("3")
        else:
            strResult = messageCAULibrary("")
    elif "학식" in message:
        if "아침" in message or "조식" in message:
            strResult = messageCAUMeal("10")
        elif "점심" in message or "중식" in message:
            strResult = messageCAUMeal("20")
        elif "저녁" in message or "석식" in message:
            strResult = messageCAUMeal("40")
        elif "대림대" in message:
            strResult = messageDaelimMeal()
        else:
            strResult = messageCAUMeal("")
    elif "개발해야" in message or "코딩해야" in message or "과제해야" in message:
        strResult = messageCoding()
    elif ("코로나" in message or "확진자" in message) and "몇" in message:
        if "지역별" in message:
            strResult = messageCoronaCity()
        else:
            strResult = messageCorona()
    elif ("ㅠ" in message or "ㅜ" in message) and getCryCount(message) >= 3:
        strResult = messageCry()
    elif "뭐먹" in message:
        strResult = messageEat()
    elif ("제발" in message or "하고 싶다" in message) and "졸업" in message:
        strResult = messageGraduate()
    elif "하.." in message:
        strResult = messageHa()
    elif "호규" in message:
        if "전역" in message:
            strResult = messageHokyuGraduate()
        else:
            strResult = messageHokyu()
    elif "배고파" in message or "배고프" in message:
        strResult = messageHungry()
    elif "이런.." in message:
        strResult = messageIreon()
    elif "주형" in message:
        strResult = messageJoohyeong()
    elif ("ㅋ" in message or "ㅎ" in message) and getLaughCount(message) >= 10:
        strResult = messageLaugh()
    elif ("앎" in message or "아는사람" in message) or "알아" in message:
        strResult = messageMoloo()
    elif "무야호" in message:
        strResult = messageMooYaHo()
    elif "꺼라" in message:
        strResult = messageOff()
    elif "오호" in message or "호오" in message:
        strResult = messageOho(message)
    elif "오.." in message:
        strResult = messageOh()
    elif "오케이" in message:
        strResult = messageOkay()
    elif "ㄹㅇㅋㅋ" in message:
        strResult = messageReal()
    elif "^^7" in message:
        strResult = messageSalute()
    elif "나스" in message or "폴리오" in message:
        strResult = messageSaseyo()
    elif "슈슉" in message:
        strResult = messageShuk()
    elif "졸려" in message or "잠와" in message or "피곤해" in message:
        strResult = messageSleepy()
    elif "멈춰" in message:
        strResult = messageStop()
    elif ";" in message and getStressCount(message) >= 4:
        strResult = messageStress()
    elif "어.." in message:
        strResult = messageUh()
    elif "와.." in message:
        strResult = messageWa()
    elif "와!" in message:
        strResult = messageWaSans()
    elif "용민" in message:
        strResult = messageYongmin()
    elif "자라" in message:
        strResult = messageZara()
    elif "자야" in message:
        strResult = messageZayazi()

    return strResult

def getCryCount(message):
    count = message.count("ㅠ")
    count += message.count("ㅜ")

    return count

def getLaughCount(message):
    count = message.count("ㅋ")
    count += message.count("ㄱ")
    count += message.count("ㄲ")
    count += message.count("ㄴ")
    count += message.count("ㅌ")
    count += message.count("ㅎ")

    return count

def getStressCount(message):
    count = message.count(";")
    count += message.count(":")
    count += message.count(",")
    count += message.count(".")

    return count

def messageAh():
    randInt = random.randrange(0, 6)
    strMessage = ""

    if randInt == 0:
        strMessage = "글쿤.."
    elif randInt == 1:
        strMessage = "그래요.."
    elif randInt == 2:
        strMessage = "그렇군요.."
    elif randInt == 3:
        strMessage = "안돼.."
    elif randInt == 4:
        strMessage = "..메리카노"
    elif randInt == 5:
        strMessage = "..에이오우"
    
    return strMessage

def messageBaby():
    randInt = random.randrange(0, 3)
    strMessage = ""
    
    if randInt == 0:
        strMessage = "귀여운척 하지 마세요;;"
    elif randInt == 1:
        strMessage = "응애 나 애기"
    elif randInt == 2:
        strMessage = "응애 나 코린이"

    return strMessage

def messageBoolpyeon():
    strMessage = "불편해?\\m불편하면 자세를 고쳐앉아!\\m보는 자세가 불편하니깐 그런거아냐!!"

    return strMessage

def messageCAUCalendar():
    strMessage = ""

    calData = datetime.date.today()
    calMonth = calData.month
    calYear = calData.year

    calData = {
        "active": True,
        "month": calMonth,
        "title": f"{calMonth}월",
        "year": calYear
    }
    calUrl = "https://mportal.cau.ac.kr/portlet/p014/p014List.ajax"

    requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = "ALL:@SECLEVEL=1"
    calResponse = eval(requests.post(calUrl, json=calData).json())
    calList = calResponse["data"]

    strMessage = f"중앙대학교 {calMonth}월 학사일정\n"
    for calItem in calList:
        strMessage += f"\n{calItem['TITLE']} : {calItem['TDAY']}"

    return strMessage

def messageCAULibrary(libTypeID):
    strMessage = libTypeID

    libData = {
       "tabNo": libTypeID
    }
    libType = ""
    libUrl = "https://mportal.cau.ac.kr/portlet/p017/p017.ajax"

    if libTypeID == "1":
       libType = "서울"
    elif libTypeID == "2":
       libType = "법학"
    elif libTypeID == "3":
       libType = "안성"
    else:
        strMessage = "중앙대학교 열람실 좌석현황\n\n사용법 : 열람실 키워드와 함께 서울 / 안성 / 법학 키워드 언급"
        return strMessage

    requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = "ALL:@SECLEVEL=1"
    libResponse = requests.post(libUrl, json=libData).json()

    libList = libResponse["gridData"]

    strMessage = f"중앙대학교 열람실 좌석현황({libType})\n"
    for libItem in libList:
       strMessage += f"\n{libItem['roomName']} : 여석 {libItem['remainCnt']}석 ({libItem['useCnt']}석 사용중)"

    return strMessage

def messageCAUMeal(mealTypeID):
    strMessage = mealTypeID

    mealData = {
        "daily": 0,
        "tabs": "1",
        "tabs2": mealTypeID
    }
    mealType = ""
    mealUrl = "https://mportal.cau.ac.kr/portlet/p005/p005.ajax"

    if mealTypeID == "10":
        mealType = "조식"
    elif mealTypeID == "20":
        mealType = "중식"
    elif mealTypeID == "40":
        mealType = "석식"
    else:
        strMessage = "중앙대학교 학식메뉴\n\n사용법 : 학식 키워드와 함께 아침 / 점심 / 저녁 / 조식 / 중식 / 석식 키워드 언급"
        return strMessage

    requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = "ALL:@SECLEVEL=1"
    mealResponse = requests.post(mealUrl, json=mealData).json()
    mealList = mealResponse["list"]

    strMessage = f"{mealList[0]['date']}. 중앙대학교 학식메뉴({mealType})\n"
    for mealItem in mealList:
        strMenu = mealItem['menuDetail']
        if strMenu == None:
            strMenu = "정보가 없습니다."
        strMessage += f"\n{mealItem['rest']} : {strMenu}"

    return strMessage

def messageCoding():
    randInt = random.randrange(0, 2)
    strMessage = ""

    if randInt == 0:
        strMessage = "구라ㅡㅡ;;"
    elif randInt == 1:
        strMessage = "ㅋ"

    return strMessage

def messageCorona():
    curDate = datetime.date.today().strftime("%Y년 %m월 %d일")
    curTimestamp = str(time.time())

    url = f"https://apiv3.corona-live.com/domestic/stat.json?timestamp={curTimestamp}"
    response = requests.get(url)
    jsonData = json.loads(response.content)["overview"]

    dataConfirmed = jsonData["confirmed"]
    dataCritical = jsonData["confirmedCritical"]
    dataDeceased = jsonData["deceased"]
    dataHospitalised = jsonData["hospitalised"]

    strConfirmed = f"확진자 : {format(dataConfirmed[1], ',')}명 (누적 {format(dataConfirmed[0], ',')}명)"
    strCritical = f"위중증 : {format(dataCritical[0], ',')}명 "
    if int(dataCritical[1]) < 0:
        strCritical += f"(-{format(int(dataCritical[1]) * -1, ',')})"
    else:
        strCritical += f"(+{format(dataCritical[1], ',')})"

    strDeceased = f"사망자 : {format(dataDeceased[0], ',')}명 "
    if int(dataDeceased[1]) < 0:
        strDeceased += f"(-{format(int(dataDeceased[1]) * -1, ',')})"
    else:
        strDeceased += f"(+{format(dataDeceased[1], ',')})"

    strHospitalised = f"입원환자 : {format(dataHospitalised[0], ',')}명 "
    if int(dataHospitalised[1]) < 0:
        strHospitalised += f"(-{format(int(dataHospitalised[1]) * -1, ',')})"
    else:
        strHospitalised += f"(+{format(dataHospitalised[1], ',')})"

    url = f"https://apiv3.corona-live.com/domestic/live.json?timestamp={curTimestamp}"
    response = requests.get(url)
    jsonData = json.loads(response.content)["live"]

    dataConfirmedLive = jsonData["today"]
    dataConfirmedLiveYesterday = jsonData["yesterday"]

    strConfirmedLive = f"실시간 : {format(dataConfirmedLive, ',')}명"
    strConfirmedLiveYesterday = f"어제 동시간대 : {format(dataConfirmedLiveYesterday, ',')}명"

    strMessage = f"{curDate} 코로나19 현황\n{strConfirmedLive}\n{strConfirmedLiveYesterday}\n\n어제까지\n{strConfirmed}\n{strCritical}\n{strHospitalised}\n{strDeceased}"

    return strMessage

def messageCoronaCity():
    curDate = datetime.date.today().strftime("%Y년 %m월 %d일")
    curTimestamp = str(time.time())

    url = f"https://apiv3.corona-live.com/domestic/live.json?timestamp={curTimestamp}"
    response = requests.get(url)
    jsonData = json.loads(response.content)["cities"]

    domesticList = ["서울", "부산", "인천", "대구", "광주", "대전", "울산", "세종", "경기", "강원", "충북", "충남", "경북", "경남", "전북", "전남", "제주", "입국 검역소"]

    strDomestic = ""
    for i in range(18):
        dataCurDomestic = jsonData[str(i)]
        strDomestic += f"{domesticList[i]} {format(dataCurDomestic[0], ',')}명 "
        if(int(dataCurDomestic[1]) < 0):
            strDomestic += f"(-{format(int(dataCurDomestic[1]) * -1, ',')})\n"
        else:
            strDomestic += f"(+{format(dataCurDomestic[1], ',')})\n"

    strMessage = f"{curDate} 코로나19 지역별 현황\n{strDomestic}".rstrip()

    return strMessage

def messageCry():
    strMessage = "뭘 울어요;;"

    return strMessage

def messageDaelimMeal():
    mealUrl = "https://www.daelim.ac.kr/ajaxf/FrBistroSvc/BistroCarteInfo.do"
    mealInput = "MENU_ID=1470&BISTRO_SEQ=1&START_DAY=2023.03.26&END_DAY=2023.03.26"

    mealHeader = {"Content-Type": "application/x-www-form-urlencoded"}
    mealResponse = requests.post(mealUrl, data=mealInput, headers=mealHeader).json()

    strDate = datetime.datetime.today().weekday() + 1
    strMessage = f"{datetime.date.today().strftime('%Y.%m.%d.')} 대림대학교 학식메뉴\n"
    if strDate < 6:
        strMessage += f"Corner1\n{mealResponse['data'][f'CCT{strDate}1'].strip()}\n"
        strMessage += f"Corner3\n{mealResponse['data'][f'CCT{strDate}3'].strip()}\n"
        strMessage += f"Corner6\n{mealResponse['data'][f'CCT{strDate}6'].strip()}\n"
        strMessage += f"Daelim Cook\n{mealResponse['data'][f'CCT{strDate}7'].strip()}\n"
    else:
        strMessage += "금일은 학식을 운영하지 않습니다"

    return strMessage

def messageEat():
    randInt = random.randrange(0, 5)
    if randInt == 0:
    	strMessage = "돼지"
    elif randInt == 1:
    	strMessage = "또 먹어?"
    elif randInt == 2:
    	strMessage = "살쪄"
    elif randInt == 3:
    	strMessage = "그만 먹어;;"
    elif randInt == 4:
        strMessage = "고기!!"

    return strMessage

def messageGraduate():
    randInt = random.randrange(0, 4)
    strMessage = ""
    
    if randInt == 0:
        strMessage = "대학원 가셔야죠 ㅋㅋ"
    elif randInt == 1:
        strMessage = "졸업은 무슨"
    elif randInt == 2:
        strMessage = "노예 하셔야죠 ㅋㅋ"
    elif randInt == 3:
        strMessage = "어림도 없지 ㅋㅋ"

    return strMessage

def messageHa():
    randInt = random.randrange(0, 2)
    strMessage = ""

    if randInt == 0:
        strMessage = "코딩하기 싫다.."
    elif randInt == 1:
        strMessage = "과제하기 싫다.."

    return strMessage
    
def messageHokyu():
    strMessage = ""
    
    randInt = random.randrange(0, 9)
    if randInt == 0:
        strMessage = "필승! 833기 일병 김호규입니다!"
    elif randInt == 1:
        strMessage = "예! 일병 김호규!"
    elif randInt == 2:
        strMessage = "필승!"
    elif randInt == 3:
        strMessage = "안녕하세요? 전역하고 싶은 김호규입니다."
    elif randInt == 4:
        strMessage = "팬택 핥짝"
    elif randInt == 5:
        strMessage = "베가 핥짝 핥짝"
    elif randInt == 6:
        strMessage = "호구"
    elif randInt == 7:
        strMessage = "K2C1 핥짝핥짝"
    elif randInt == 8:
        strMessage = "감사합니다. 314대대 통신반 일병 김호규입니다. 머슼타드일까요?"
    
    return strMessage

def messageHokyuGraduate():
    strMessage = ""
    dateStart = datetime.date(2021,12,6)
    dateEnd = datetime.date(2023,8,27)
    dateToday = datetime.date.today()

    leftDays = (dateEnd - dateToday).days - 1
    goneDays = (dateToday - dateStart).days

    randInt = random.randrange(0, 4)
    if randInt == 0:
        strMessage = "호규는 전역할 때까지 %d일 남았습니다"%(leftDays)
    elif randInt == 1:
        strMessage = "호규가 입대한 지 %d일 되었습니다."%(goneDays)
    elif randInt == 2:
        strMessage = "833기가 벌써 전역 따질 짬인가?"
    elif randInt == 3:
        strMessage = "404 Not Found"

    return strMessage

def messageHungry():
    strMessage = ""
    
    randInt = random.randrange(0, 4)
    if randInt == 0:
    	strMessage = "돼지"
    elif randInt == 1:
    	strMessage = "또 먹어?"
    elif randInt == 2:
    	strMessage = "살쪄"
    elif randInt == 3:
    	strMessage = "그만 먹어;;"
    	
    return strMessage

def messageIreon():
    randInt = random.randrange(0, 5)
    strMessage = ""

    if randInt == 0:
        strMessage = "안됐군요.."
    elif randInt == 1:
        strMessage = "안타깝네요.."
    elif randInt == 2:
        strMessage = "눈물이 납니다.."
    elif randInt == 3:
        strMessage = "유감입니다.."
    elif randInt == 4:
        strMessage = "불쌍하네요.."
    
    return strMessage

def messageJoohyeong():
    strMessage = "예! 2025년도 CECOM 회장 이주형!"

    return strMessage

def messageLaugh():
    randInt = random.randrange(0, 2)
    strMessage = ""

    if randInt == 0:
        strMessage = "뭘 웃어요;;"
    elif randInt == 1:
        strMessage = "안웃긴데;;"

    return strMessage

def messageMoloo():
    strMessage = "몰?루"

    return strMessage

def messageMooYaHo():
    strMessage = "그만큼 신나신다는거지~"

    return strMessage

def messageOff():
    strMessage = "전기세 아깝다ㅡㅡ;;"

    return strMessage

def messageOh():
    randInt = random.randrange(0, 2)
    strMessage = ""

    if randInt == 0:
        strMessage = "..레오"
    elif randInt == 1:
        strMessage = "..렌지쥬스"
    
    return strMessage

def messageOho(message):
    strMessage = message[::-1]
    
    return strMessage

def messageOkay():
    strMessage = "땡큐! 4딸라!"

    return strMessage

def messageReal():
    randInt = random.randrange(0, 2)
    strMessage = ""

    if randInt == 0:
        strMessage = "ㄹㅇㅋㅋ"
    elif randInt == 1:
        strMessage = "아닌데요"

    return strMessage

def messageSalute():
    randInt = random.randrange(0, 2)
    strMessage = ""

    if randInt == 0:
        strMessage = "필승! ^^7"
    elif randInt == 1:
        strMessage = "충성! ^^7"

    return strMessage

def messageSaseyo():
    randInt = random.randrange(0, 2)
    strMessage = ""

    if randInt == 0:
        strMessage = "사세요"
    elif randInt == 1:
        strMessage = "안 사도 돼요"

    return strMessage

def messageShuk():
    randInt = random.randrange(0, 4)
    strMessage = "슈슉"
    
    while randInt != 4:
        if randInt == 0:
            strMessage += ".슉.슈슉.시.발럼"
        elif randInt == 1:
            strMessage += ".슈슉.슉.슉시"
        elif randInt == 2:
            strMessage += ".슈발놈아.슉.시발.슈슉.슉"
        elif randInt == 3:
            strMessage += ".슈슉.시발.럼아.슉.슈슉.슉.슉슉.슈슉.시.발놈아"
        
        randInt = random.randrange(0, 5)

    strMessage += ".슉"

    return strMessage

def messageSleepy():
    randInt = random.randrange(0, 2)
    strMessage = ""
    
    if randInt == 0:
        strMessage = "자라;;"
    elif randInt == 1:
        strMessage = "구라;;"
    
    return strMessage

def messageStop():
    strMessage = "멈춰!!"

    return strMessage

def messageStress():
    strMessage = "어림도 없지"

    return strMessage

def messageUh():
    randInt = random.randrange(0, 3)
    strMessage = ""

    if randInt == 0:
        strMessage = "..이가없네;;"
    elif randInt == 1:
        strMessage = "..피치"
    elif randInt == 2:
        strMessage = "..기여차"

    return strMessage

def messageWa():
    randInt = random.randrange(0, 9)
    strMessage = ""

    if randInt == 0:
        strMessage = "갑부;;"
    elif randInt == 1:
        strMessage = "기만;;"
    elif randInt == 2:
        strMessage = "ㄹㅇ;;"
    elif randInt == 3:
        strMessage = "마스터;;"
    elif randInt == 4:
        strMessage = "역시;;"
    elif randInt == 5:
        strMessage = "이건 좀;;"
    elif randInt == 6:
        strMessage = "극혐;;"
    elif randInt == 7:
        strMessage = "플;;"
    elif randInt == 8:
        strMessage = "이파이;;"

    return strMessage

def messageWaSans():
    strMessage = "샌즈!\\m아시는구나!\\m이거 겁.나.어.렵.습.니.다."

    return strMessage

def messageYongmin():
    strMessage = "집가고싶다"
    
    return strMessage

def messageZara():
    randInt = random.randrange(0, 2)
    strMessage = ""
    
    if randInt == 0:
        strMessage = "전기세 아깝다ㅡㅡ;;"
    elif randInt == 1:
        strMessage = "거북이"
        
    return strMessage

def messageZayazi():
    strMessage = "구라ㅡㅡ;;"

    return strMessage