from main_pyqt5 import *
from dashboard.dashboard import *
from backend.function import *

class ChatBot:

    def unSaveChatBot(self):
        self.btnSaveOrderNew.setStyleSheet('background-color: rgb(217, 38, 0);')
        self.btnSaveOrderReady.setStyleSheet('background-color: rgb(217, 38, 0);')
        self.btnSaveOrderShipping.setStyleSheet('background-color: rgb(217, 38, 0);')
        self.btnSaveOrderSuccess.setStyleSheet('background-color: rgb(217, 38, 0);')
        self.btnSaveOrderCancel.setStyleSheet('background-color: rgb(217, 38, 0);')

    def savedChatBot(self):
        self.btnSaveOrderNew.setStyleSheet('')
        self.btnSaveOrderReady.setStyleSheet('')
        self.btnSaveOrderShipping.setStyleSheet('')
        self.btnSaveOrderSuccess.setStyleSheet('')
        self.btnSaveOrderCancel.setStyleSheet('')    

    def setChatBotPlainText(self):
        try:
            with open('temp//data.json') as f:
                data = json.load(f)
            shop_choose = self.checkShopChoose()
            obj = [
            self.frameOrderNew_obj,
            self.frameOrderReady_obj,
            self.frameOrderShipping_obj,
            self.frameOrderSuccess_obj,
            self.frameOrderCancel_obj,
            ]
            layout = [
            self.frameOrderNew,
            self.frameOrderReady,
            self.frameOrderShipping,
            self.frameOrderSuccess,
            self.frameOrderCancel,
            ]         
            new = data['shopee'][shop_choose]['orderChatBotList']['textOrderNew']
            ready = data['shopee'][shop_choose]['orderChatBotList']['textOrderReady']
            shipping = data['shopee'][shop_choose]['orderChatBotList']['textOrderShipping']
            success = data['shopee'][shop_choose]['orderChatBotList']['textOrderSuccess']
            cancel = data['shopee'][shop_choose]['orderChatBotList']['textOrderCancel']
            dataText = [new,ready,shipping,success,cancel]
            for o , l , d in zip(obj,layout,dataText):
                count = 1
                for i in d:
                    UIFunctions.addFrameText(self,count,o,l,i)
                    count += 1
            self.writeLog(f"Tải nội dung ChatBot cho account {data['shopee'][shop_choose]['shop_name']}")   
        except: 
            pass

    def btnSaveChatBot(self):
        shop_choose = self.checkShopChoose()
        with open('temp//data.json') as f:
            data = json.load(f)

        textOrderNew = []
        textOrderReady = []
        textOrderShipping = []
        textOrderSuccess = []
        textOrderCancel = []

        obj = [
            self.frameOrderNew_obj,
            self.frameOrderReady_obj,
            self.frameOrderShipping_obj,
            self.frameOrderSuccess_obj,
            self.frameOrderCancel_obj,
        ]

        for frame in obj:
            for textData in frame.findChildren(QPlainTextEdit):
                if len(textData.toPlainText()) != 0:
                    if frame == self.frameOrderNew_obj:
                        textOrderNew.append(textData.toPlainText())
                    elif frame == self.frameOrderReady_obj:
                        textOrderReady.append(textData.toPlainText())
                    elif frame == self.frameOrderShipping_obj:
                        textOrderShipping.append(textData.toPlainText())
                    elif frame == self.frameOrderSuccess_obj:
                        textOrderSuccess.append(textData.toPlainText())
                    elif frame == self.frameOrderCancel_obj:
                        textOrderCancel.append(textData.toPlainText())

        r = Database_mongoDB.registered_Users_Collection.update(
            { '_id': data['id_wp'] },
            { '$set': { 
                f'shopee.{shop_choose}.orderChatBotList.textOrderNew': textOrderNew, 
                f'shopee.{shop_choose}.orderChatBotList.textOrderReady': textOrderReady,
                f'shopee.{shop_choose}.orderChatBotList.textOrderShipping': textOrderShipping,
                f'shopee.{shop_choose}.orderChatBotList.textOrderSuccess': textOrderSuccess,
                f'shopee.{shop_choose}.orderChatBotList.textOrderCancel': textOrderCancel, 
                }},
            upsert=True  
            )     

        if len(textOrderNew + textOrderReady + textOrderShipping + textOrderSuccess + textOrderCancel) == 0 :
            self.btnChatBotSwitch.setChecked(False)
            UIFunctions.activeFunctions(self,self.btnChatBotSwitch.isChecked(),"chatBotSwitch")

        
        if r['updatedExisting'] == True:
            self.updateToDataJson(data['id_wp'])
            ChatBot.savedChatBot(self)
            self.showPopup("Thành Công","Lưu nội dung Thành Công","Tất cả nội dung trả lời đã được lưu Thành Công",True)
            self.writeLog('Lưu thành công nội dụng ChatBot')
        else:
            self.showPopup("Không Thành Công","Không lưu được nội dung","Vui lòng liên hệ fanpage để được trợ giúp",False)
            self.writeLog('Không lưu thành công nội dụng ChatBot')

    def setStyleButtonChatBot(self,objectName):
        for w in self.frameButtonChatBot.findChildren(QPushButton):
            if w.objectName() != objectName:
                w.setStyleSheet('')
            if w.objectName() == objectName:
                w.setStyleSheet('background-color: rgb(38, 166, 154);')

    def btnChatBot(self):
        btn = self.sender()

        if btn.objectName() == 'btnOrderNew':
            self.stackedWidgetChatBot.setCurrentIndex(0)
            ChatBot.setStyleButtonChatBot(self,btn.objectName())

        elif btn.objectName() == 'btnOrderReady':
            self.stackedWidgetChatBot.setCurrentIndex(4)
            ChatBot.setStyleButtonChatBot(self,btn.objectName())

        elif btn.objectName() == 'btnOrderShipping':
            self.stackedWidgetChatBot.setCurrentIndex(3)
            ChatBot.setStyleButtonChatBot(self,btn.objectName())

        elif btn.objectName() == 'btnOrderSuccess':
            self.stackedWidgetChatBot.setCurrentIndex(2)
            ChatBot.setStyleButtonChatBot(self,btn.objectName())

        elif btn.objectName() == 'btnOrderCancel':
            self.stackedWidgetChatBot.setCurrentIndex(1)
            ChatBot.setStyleButtonChatBot(self,btn.objectName())