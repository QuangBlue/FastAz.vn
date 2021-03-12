from main_pyqt5 import *
from dashboard.dashboard import *
from backend.function import *

class ReplyRating:

    def unSaveReplyRating(self):
        self.btnSaveOneStar.setStyleSheet('background-color: rgb(217, 38, 0);')
        self.btnSaveTwoStar.setStyleSheet('background-color: rgb(217, 38, 0);')
        self.btnSaveThreeStar.setStyleSheet('background-color: rgb(217, 38, 0);')
        self.btnSaveFourStar.setStyleSheet('background-color: rgb(217, 38, 0);')
        self.btnSaveFiveStar.setStyleSheet('background-color: rgb(217, 38, 0);')

    def savedReplyRating(self):
        self.btnSaveOneStar.setStyleSheet('')
        self.btnSaveTwoStar.setStyleSheet('')
        self.btnSaveThreeStar.setStyleSheet('')
        self.btnSaveFourStar.setStyleSheet('')
        self.btnSaveFiveStar.setStyleSheet('')

    def setReplyRatingPlainText(self):
        try:
            with open('temp//data.json') as f:
                data = json.load(f)
            shop_choose = self.checkShopChoose()
            obj = [
            self.frameOneStar_obj,
            self.frameTwoStar_obj,
            self.frameThreeStar_obj,
            self.frameFourStar_obj,
            self.frameFiveStar_obj,
            ]
            layout = [
            self.frameOneStar,
            self.frameTwoStar,
            self.frameThreeStar,
            self.frameFourStar,
            self.frameFiveStar,
            ]         
            oneStar = data['shopee'][shop_choose]['replyRatingList']['textOneStar']
            twoStar = data['shopee'][shop_choose]['replyRatingList']['textTwoStar']
            threeStar = data['shopee'][shop_choose]['replyRatingList']['textThreeStar']
            fourStar = data['shopee'][shop_choose]['replyRatingList']['textFourStar']
            fiveStar = data['shopee'][shop_choose]['replyRatingList']['textFiveStar']
            dataText = [oneStar,twoStar,threeStar,fourStar,fiveStar]
            for o , l , d in zip(obj,layout,dataText):
                count = 1
                for i in d:
                    UIFunctions.addFrameText(self,count,o,l,i)
                    count += 1
            self.writeLog(f"Tải nội dung Đánh Giá cho account {data['shopee'][shop_choose]['shop_name']}")   
        except: 
            pass

    def btnSaveReplyRating(self):
        shop_choose = self.checkShopChoose()
        with open('temp//data.json') as f:
            data = json.load(f)

        textOneStar = []
        textTwoStar = []
        textThreeStar = []
        textFourStar = []
        textFiveStar = []

        obj = [
            self.frameOneStar_obj,
            self.frameTwoStar_obj,
            self.frameThreeStar_obj,
            self.frameFourStar_obj,
            self.frameFiveStar_obj,
        ]

        for frame in obj:
            for textData in frame.findChildren(QPlainTextEdit):
                if len(textData.toPlainText()) != 0:
                    if frame == self.frameOneStar_obj:
                        textOneStar.append(textData.toPlainText())
                    elif frame == self.frameTwoStar_obj:
                        textTwoStar.append(textData.toPlainText())
                    elif frame == self.frameThreeStar_obj:
                        textThreeStar.append(textData.toPlainText())
                    elif frame == self.frameFourStar_obj:
                        textFourStar.append(textData.toPlainText())
                    elif frame == self.frameFiveStar_obj:
                        textFiveStar.append(textData.toPlainText())

        r = Database_mongoDB.registered_Users_Collection.update(
            { '_id': data['id_wp'] },
            { '$set': { 
                f'shopee.{shop_choose}.replyRatingList.textOneStar': textOneStar, 
                f'shopee.{shop_choose}.replyRatingList.textTwoStar': textTwoStar,
                f'shopee.{shop_choose}.replyRatingList.textThreeStar': textThreeStar,
                f'shopee.{shop_choose}.replyRatingList.textFourStar': textFourStar,
                f'shopee.{shop_choose}.replyRatingList.textFiveStar': textFiveStar, 
                }},
            upsert=True  
            )     

        if len(textOneStar + textTwoStar + textThreeStar + textFourStar + textFiveStar) == 0 :
            self.btnReplyRatingSwitch.setChecked(False)
            UIFunctions.activeFunctions(self,self.btnReplyRatingSwitch.isChecked(),"replyRatingSwitch")
        
        if r['updatedExisting'] == True:
            self.updateToDataJson(data['id_wp'])
            ReplyRating.savedReplyRating(self)
            self.showPopup("Thành Công","Lưu nội dung Thành Công","Tất cả nội dung trả lời đã được lưu Thành Công",True)
            self.writeLog('Lưu thành công nội dụng Đánh Giá')
        else:
            self.showPopup("Không Thành Công","Không lưu được nội dung","Vui lòng liên hệ fanpage để được trợ giúp",False)
            self.writeLog('Không lưu thành công nội dụng Đánh Giá')     

    def setStyleButtonReplyRating(self,objectName):
        for w in self.frameButtonReplyRating.findChildren(QPushButton):
            if w.objectName() != objectName:
                w.setStyleSheet('')
            if w.objectName() == objectName:
                w.setStyleSheet('background-color: rgb(38, 166, 154);')


    def btnReplyRating(self):
        btn = self.sender()

        if btn.objectName() == 'btnOneStar':
            self.stackedWidgetReplyRating.setCurrentIndex(0)
            ReplyRating.setStyleButtonReplyRating(self,btn.objectName())

        elif btn.objectName() == 'btnTwoStar':
            self.stackedWidgetReplyRating.setCurrentIndex(1)
            ReplyRating.setStyleButtonReplyRating(self,btn.objectName())

        elif btn.objectName() == 'btnThreeStar':
            self.stackedWidgetReplyRating.setCurrentIndex(2)
            ReplyRating.setStyleButtonReplyRating(self,btn.objectName())

        elif btn.objectName() == 'btnFourStar':
            self.stackedWidgetReplyRating.setCurrentIndex(3)
            ReplyRating.setStyleButtonReplyRating(self,btn.objectName())

        elif btn.objectName() == 'btnFiveStar':
            self.stackedWidgetReplyRating.setCurrentIndex(4)
            ReplyRating.setStyleButtonReplyRating(self,btn.objectName())

