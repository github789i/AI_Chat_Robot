# -*- coding: utf-8 -*-

import os
import sys
import threading

import requests
import json
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence, QFont, QColor, QIcon
from PyQt5.QtWidgets import QShortcut, QAbstractItemView, QListWidgetItem, QMenu, QAction, QApplication


class Ui_MainWindow(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        # 新的聊天框是否存在
        self.count = 0
        self.messageList = None
        self.frame_3 = None
        self.frame_2 = None
        self.frame_1 = None
        self.sentButton = None
        self.inputEdit = None
        self.chatList = None
        self.newChatExist = True
        # 当前聊天的界面
        # self.curChat = 0
        self.title = None
        # 聊天历史保存的目录
        self.saveDir = 'ChatHistory'
        self.data = {
            "title": '',
            "content": []
        }
        self.robot = Robot()
        self.InitUi()

    def InitUi(self):
        self.setFixedSize(QtCore.QSize(1125, 800))
        self.setWindowTitle('文心一言')
        self.setMinimumSize(QtCore.QSize(1125, 800))
        self.setMaximumSize(QtCore.QSize(1125, 800))
        # 消息输入框
        self.inputEdit = QtWidgets.QLineEdit(self)
        self.inputEdit.setGeometry(QtCore.QRect(260, 695, 625, 51))
        self.inputEdit.setObjectName("inputEdit")
        self.inputEdit.setStyleSheet(
            "border-top-left-radius:15px;"
            " border-top-right-radius:15px;"
            "border-bottom-left-radius:15px; "
            "border-bottom-right-radius:15px;")
        # 设置字体
        self.inputEdit.setFont(QFont('Arial', 15))

        # 发送按钮
        self.sentButton = QtWidgets.QPushButton(self)
        self.sentButton.setGeometry(QtCore.QRect(910, 695, 101, 51))
        self.sentButton.setObjectName("sentButton")
        self.sentButton.setText('发送')
        self.sentButton.setStyleSheet(
            "QPushButton{background-color: rgb(25, 195, 125);border:0px groove gray;border-radius:10px;padding:2px 4px;"
            "border-style: outset;color: white}\n "
            "QPushButton:hover{background-color:rgb(229, 241, 251); color: black;}\n"
            "QPushButton:pressed{background-color:rgb(204, 228, 247);border-style: inset;}\n"
        )
        self.sentButton.clicked.connect(self.chatting)
        # 绑定快捷键
        shortcut = QShortcut(QKeySequence(Qt.Key_Return), self)
        shortcut.activated.connect(self.chatting)
        # 设置字体
        self.sentButton.setFont(QFont('Arial', 15))

        self.frame_1 = QtWidgets.QFrame(self)
        self.frame_1.setGeometry(QtCore.QRect(0, 0, 225, 800))
        self.frame_1.setMinimumSize(QtCore.QSize(225, 800))
        self.frame_1.setMaximumSize(QtCore.QSize(225, 800))
        self.frame_1.setAutoFillBackground(True)
        self.frame_1.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_1.setObjectName("frame_1")
        # 设置背景颜色
        self.frame_1.setStyleSheet("background-color: rgb(32,33,35)")

        # 左侧对话（无用）
        self.chatList = QtWidgets.QListWidget(self.frame_1)
        self.chatList.setGeometry(QtCore.QRect(0, 0, 230, 800))
        self.chatList.setMinimumSize(QtCore.QSize(230, 0))
        self.chatList.setMaximumSize(QtCore.QSize(230, 16777215))
        # 设置无边框
        self.chatList.setFrameShape(0)
        # 设置选择模式
        self.chatList.setSelectionMode(QAbstractItemView.SingleSelection)
        self.chatList.setStyleSheet("QListView {outline: none;}\n"
                                    "#chatList::item {background-color: rgb(32,33,35);color: #ffffff;border: "
                                    "transparent;padding: 8px;}\n "
                                    "#chatList::item:hover {background-color: #4e5465;}\n"
                                    "#chatList::item:selected {border-left: 5px solid #009688;}")

        self.chatList.setAutoScrollMargin(20)
        self.chatList.setTabKeyNavigation(False)
        self.chatList.setDragEnabled(False)
        self.chatList.setDragDropOverwriteMode(False)
        self.chatList.setAlternatingRowColors(True)
        self.chatList.setIconSize(QtCore.QSize(42, 42))
        self.chatList.setBatchSize(110)
        self.chatList.setObjectName("chatList")
        font = QtGui.QFont()
        font.setPointSize(16)
        self.chatList.setFont(font)
        item = QtWidgets.QListWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignBottom)
        item.setFont(font)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        item.setForeground(brush)
        item.setIcon(QIcon('images/add.png'))
        item.setText('New Chat')
        self.chatList.addItem(item)
        self.chatList.setCurrentItem(item)
        # 用户切换聊天记录
        self.chatList.itemClicked.connect(self.chatChanged)
        # 用户右键菜单
        self.chatList.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 禁止双击可编辑
        self.chatList.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 右键菜单
        self.chatList.setContextMenuPolicy(Qt.CustomContextMenu)
        self.chatList.customContextMenuRequested.connect(self.myListWidgetContext)

        self.frame_2 = QtWidgets.QFrame(self)
        self.frame_2.setGeometry(QtCore.QRect(225, 650, 900, 150))
        self.frame_2.setAcceptDrops(False)
        self.frame_2.setAutoFillBackground(True)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        # 设置背景颜色
        self.frame_2.setStyleSheet("background-color: rgb(52,53,65)")

        self.frame_3 = QtWidgets.QFrame(self)
        self.frame_3.setGeometry(QtCore.QRect(225, 0, 900, 650))
        self.frame_3.setAutoFillBackground(True)
        self.frame_3.setStyleSheet("")
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        # 设置背景颜色
        self.frame_3.setStyleSheet("background-color: rgb(52,53,65)")

        # 消息界面
        self.messageList = QtWidgets.QListWidget(self.frame_3)
        self.messageList.setGeometry(QtCore.QRect(0, 0, 900, 650))
        self.messageList.setMinimumSize(QtCore.QSize(900, 650))
        self.messageList.setMaximumSize(QtCore.QSize(900, 650))
        # 设置无边框
        self.messageList.setFrameShape(0)
        self.messageList.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.messageList.setTabKeyNavigation(False)
        self.messageList.setDragEnabled(False)
        self.messageList.setDragDropOverwriteMode(False)
        self.messageList.setAlternatingRowColors(True)
        self.messageList.setIconSize(QtCore.QSize(50, 50))
        self.messageList.setBatchSize(110)
        self.messageList.setObjectName("listWidget")
        self.messageList.setWordWrap(True)
        self.messageList.setContextMenuPolicy(Qt.CustomContextMenu)
        self.messageList.customContextMenuRequested.connect(self.CopyContext)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.messageList.setFont(font)

        self.inputEdit.raise_()
        self.sentButton.raise_()
        # 获取聊天历史列表
        self.getChatHistory()

    def copyText(self):
        # 获取选定的项的文本并将其复制到剪贴板
        selected_item = self.messageList.selectedIndexes()[0]
        text_to_copy = selected_item.data()
        clipboard = QApplication.clipboard()
        clipboard.setText(text_to_copy)

    def CopyContext(self, position):
        # 弹出菜单
        popMenu = QMenu()
        copyAction = QAction('复制信息', self)
        # 查看右键时是否在item上面,如果不在.就不显示删除和修改.
        copyAction.triggered.connect(self.copyText)
        popMenu.addAction(copyAction)
        popMenu.exec_(self.messageList.mapToGlobal(position))

    def myListWidgetContext(self, position):
        # 弹出菜单
        popMenu = QMenu()
        delAct = QAction("删除聊天", self)
        # 查看右键时是否在item上面,如果不在.就不显示删除和修改.
        if self.chatList.itemAt(position):
            popMenu.addAction(delAct)

        delAct.triggered.connect(self.DeleteItem)
        popMenu.exec_(self.chatList.mapToGlobal(position))

    # 删除聊天
    def DeleteItem(self):
        self.messageList.clear()
        os.remove(os.path.join(self.saveDir, f'{self.chatList.currentItem().text()}.json'))
        self.chatList.takeItem(self.chatList.currentRow())
        for i in range(len(os.listdir('ChatHistory'))):
            old_name = os.listdir('ChatHistory')[i]
            new_name = '[' + str(i + 1) + ']' + old_name[3:]
            os.rename(os.path.join(self.saveDir, old_name), os.path.join(self.saveDir, new_name))
            self.chatList.item(i + 1).setText(new_name[0:-5])
            # 打开新的文件
            try:
                with open(os.path.join(self.saveDir, new_name), 'r') as file:
                    self.data = json.load(file)
                    self.data['title'] = new_name[0: -5]
                    print(self.data)
                    file.close()
            except FileNotFoundError as e:
                print(e)
            # 将之前的聊天记录写入文件
            with open(os.path.join(self.saveDir, new_name), 'w') as file:
                json.dump(self.data, file)
                file.close()
            self.data = {"title": '', "content": []}

    def getChatHistory(self):
        if not os.path.exists(self.saveDir):
            os.makedirs(self.saveDir)
            return
        fileList = os.listdir(self.saveDir)
        for file in fileList:
            try:
                with open(os.path.join(self.saveDir, file), 'r') as f:
                    tmp = json.load(f)
                    print(tmp)
                    item = QtWidgets.QListWidgetItem()
                    item.setIcon(QIcon("images/question.jpg"))

                    item.setTextAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom)
                    font = QtGui.QFont()
                    font.setPointSize(14)
                    item.setFont(font)
                    brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
                    item.setForeground(brush)
                    item.setBackground(QColor(52, 53, 65))
                    item.setText(tmp['title'])
                    self.chatList.addItem(item)
                    f.close()
            except Exception as e:
                print(e)
                continue

    def chatChanged(self):
        print(self.title)
        indexes = self.chatList.selectedIndexes()
        # 清除消息框
        self.messageList.clear()

        # 将之前的聊天记录写入文件
        if self.title is not None and self.data != {"title": '', "content": []}:
            with open(os.path.join(self.saveDir, f'{self.title}.json'), 'w') as file:
                json.dump(self.data, file)
                file.close()

        if indexes[0].row() == 0:
            if self.newChatExist:
                return
            self.newChatExist = True
            return

        self.title = self.chatList.currentItem().text()

        # 打开新的文件
        try:
            with open(os.path.join(self.saveDir, f'{self.title}.json'), 'r') as file:
                self.data = json.load(file)
                # 恢复聊天记录
                self.recoverMessage()
                file.close()
        except FileNotFoundError as e:
            print(e)

    # 恢复以前的消息记录
    def recoverMessage(self):
        try:
            for content in self.data["content"]:
                self.addOneItem(content["text"], content["user"], mode='recover')
        except TypeError as e:
            print(e)

    def addOneItem(self, text, user, mode='add'):
        item = QListWidgetItem()
        if user == 'ME':
            item.setIcon(QIcon("images/user.png"))
        elif user == 'RT' or user == 'OT':
            item.setIcon(QIcon("images/robot.png"))
        item.setTextAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom)
        font = QtGui.QFont()
        font.setPointSize(12)
        item.setFont(font)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        item.setForeground(brush)
        item.setBackground(QColor(52, 53, 65))
        item.setText('\n' + text + '\n')
        if mode == 'add' and user == 'RT':
            item_count = self.messageList.count()
            if item_count > 0:
                last_item_index = item_count - 1
                # 删除最后一个项
                self.messageList.takeItem(last_item_index)
        self.messageList.addItem(item)

        last_item = self.messageList.item(self.messageList.count() - 1)
        if last_item:
            self.messageList.scrollToItem(last_item)

    def sentMessage(self, text):
        reply = self.robot.sent(text=text)
        # 回复的消息
        self.addOneItem(reply, user='RT')
        self.data["content"].append({'user': 'RT', 'text': reply})

    # 发送消息
    def chatting(self):
        text = self.inputEdit.text()
        self.inputEdit.setText('')
        # 用户输入信息添加到聊天框中
        self.addOneItem(text, user='ME')

        # 如果当前聊天框为新的聊天，且用户首次输入
        if self.chatList.selectedIndexes()[0].row() == 0 and self.newChatExist:
            self.count = len(os.listdir('ChatHistory')) + 1
            self.data = {
                "title": '',
                "content": []
            }
            self.title = '[' + str(self.count) + ']' + text[0:min(5, len(text))]
            print(self.title)
            self.data["title"] = self.title
            item = QtWidgets.QListWidgetItem()
            item.setIcon(QIcon('images/question.jpg'))
            font = QtGui.QFont()
            font.setPointSize(14)
            item.setFont(font)
            item.setText(self.title)
            self.chatList.insertItem(self.count, item)
            self.chatList.setCurrentItem(item)
            self.newChatExist = False

        self.data["content"].append({"user": 'ME', 'text': text})
        self.addOneItem('waiting...', user='OT')
        thread = threading.Thread(target=self.sentMessage, args=(text,))
        thread.start()


class Robot(object):
    def sent(self, text=''):
        # API_KEY = 'HpXttg7t71Y5t6qIn7kmQGUM'
        # SECRET_KEY = 'ivzPCvZ9DGSyWsAksUlx0wBQSEsA0npb'
        # url = "https://aip.baidubce.com/oauth/2.0/token"
        # params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
        # access_token = str(requests.post(url, params=params).json().get("access_token"))
        access_token = '24.43119cc5d8ac9d1375f1c8c10f3b6ba1.2592000.1697880688.282335-39737772'
        url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/eb-instant?access_token={access_token}"

        payload = json.dumps({
            "messages": [
                {
                    "role": "user",
                    "content": text
                }
            ]
        })
        headers = {
            'Content-Type': 'application/json'
        }
        try:
            response = requests.request("POST", url, headers=headers, data=payload).json()
            if response:
                return response['result']
        except requests.exceptions.ProxyError as e:
            print(e)
            return '连接出错了，请检查关闭代理功能是否关闭'


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.show()
    exit(app.exec_())
