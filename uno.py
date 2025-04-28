from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
import sys
import time

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QScrollArea
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget

import deck_of_cards as doc
import random

global deck, p1, p2
discard = []
deck, p1, p2 = doc.initialize_deck()
#p1 = ['yellow_2', 'blue_skip', 'red_5', 'WC']
#p2 = ['green_7', 'green_reverse', 'red_9', 'blue_3']
#deck = ['green_1', 'green_2', 'blue_draw2', 'yellow_5', 'green_5']
#print(deck, p1, p2, sep = '\n')

print("\nGame starts!")

begin = 0
player = p2
color = 'none'
move = 'none'
change = 0
click = 0
spcl = 0

print("\nDrawing Cards Until Number Card\n")

class UI(QMainWindow):
    def __init__(self):
        super(UI,self).__init__()

        #load the UI file
        uic.loadUi("uno_ui.ui",self)
        self.RED.clicked.connect(self.click_color)
        self.GREEN.clicked.connect(self.click_color)
        self.BLUE.clicked.connect(self.click_color)
        self.YELLOW.clicked.connect(self.click_color)

        win = 0
        while(win == 0):
            global move, click, color
            if not deck:
                self.clear_deck()
                self.result(2)
                break
            move = 'none'
            self.button_display(False)
            self.hand_update()
            self.play()
            self.pile_update()
            if spcl == 0:
                self.special_case()
            # print("DISCARD: \n", discard)
            print("\nLAST PLAYED: ", discard[-1])
            # print("DECK NOW: \n", deck)
            print("\nPLAYER 1: \n", p1)
            print("BOT: \n", p2)
            self.switch_players()
            win = self.checkwin()

            self.show()
        self.show()

    def result(self, flag):
        self.res = QtWidgets.QLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.res.sizePolicy().hasHeightForWidth())
        self.res.setSizePolicy(sizePolicy)
        self.res.setMinimumSize(QtCore.QSize(90, 150))
        self.res.setMaximumSize(QtCore.QSize(90, 150))
        if flag == 1:
            self.res.setText("YOU WIN!")
        elif flag == 2:
            self.res.setText("DECK EMPTY!")
        else:
            self.res.setText("YOU LOSE!")
        self.horizontalLayout.addWidget(self.res)
        self.res.show()

    def status_update(self, str):
        self.statusbar.showMessage(str)

    def clear_deck(self, type = True):
        if type == True:
            for i in reversed(range(self.horizontalLayout.count())):
                widgetToRemove = self.horizontalLayout.itemAt(i).widget()
                # remove it from the layout list
                self.horizontalLayout.removeWidget(widgetToRemove)
                # remove it from the gui
                widgetToRemove.setParent(None)
        else:
            for i in reversed(range(self.horizontalLayout.count())):
                widgetToDisable = self.horizontalLayout.itemAt(i).widget()
                widgetToDisable.setEnabled(False)

    def highlight(self, legal):
        for i in reversed(range(self.horizontalLayout.count())):
            widgetToDisable = self.horizontalLayout.itemAt(i).widget()
            if widgetToDisable.objectName() not in legal:
                widgetToDisable.setEnabled(False)

    def button_display(self, set = False):
        if set == False:
            self.RED.setEnabled(False)
            self.GREEN.setEnabled(False)
            self.BLUE.setEnabled(False)
            self.YELLOW.setEnabled(False)
        else:
            self.RED.setEnabled(True)
            self.GREEN.setEnabled(True)
            self.BLUE.setEnabled(True)
            self.YELLOW.setEnabled(True)
            self.clear_deck(False)

    def click_card(self):
        global move
        print(self.sender().objectName())
        move = self.sender().objectName()

    def click_color(self):
        global color, click
        clicked = self.sender().objectName()
        if clicked == 'RED':
            color = 'red_'
        elif clicked == 'YELLOW':
            color = 'yellow_'
        elif clicked == 'GREEN':
            color = 'green_'
        elif clicked == 'BLUE':
            color = 'blue_'
        click = 1


    def pile_update(self):
        self.discard.setPixmap(QtGui.QPixmap(f"img/{discard[-1]}.png"))

    def hand_update(self):
        self.clear_deck()
        for card in p1:
            self.new_card = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
            self.new_card.clicked.connect(self.click_card)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.new_card.sizePolicy().hasHeightForWidth())
            self.new_card.setSizePolicy(sizePolicy)
            self.new_card.setMinimumSize(QtCore.QSize(90, 150))
            self.new_card.setMaximumSize(QtCore.QSize(90, 150))
            self.new_card.setText("")
            self.new_card.setIcon(QtGui.QIcon(f"img/{card}.png"))
            self.new_card.setIconSize(QtCore.QSize(90, 150))
            self.new_card.setObjectName(f"{card}")
            self.horizontalLayout.addWidget(self.new_card)
            self.new_card.show()
        for card in p2:
            self.bot_count.setText(f"{len(p2)}")

    # to facilitate game flow
    def play(self):
        global begin, player, move, spcl
        if begin == 0:
            while True:
                self.draw_card()
                for word in ['reverse', 'skip', 'draw2', 'WC', 'W+4']:
                    if word in discard[-1]:
                        self.draw_card()
                    else:
                        continue
                begin = 1
                self.status_update(f"{discard[-1]} drawn from deck")
                break

        else:
            if player == p1:
                legal = self.legal_move()
                if legal == -1:
                    self.draw_card(deck, p1, legal)
                    if discard[-1] == 'W+4' or discard[-1] == 'WC':
                        spcl = 1
                        draw_card(deck, p1, legal)
                    if discard[-1].split('_')[1] == 'reverse' or \
                            discard[-1].split('_')[1] == 'skip' or \
                            discard[-1].split('_')[1] == 'draw2':
                        self.switch_players()
                else:
                    print('\nLEGAL MOVES: ', legal)
                    self.highlight(legal)
                    spcl = 0
                    while move == 'none':
                        QCoreApplication.processEvents()
                    num = p1.index(move)
                    self.draw_card(p1, discard, num)
            else:
                num = self.ai()
                if num == -1:
                    self.draw_card(deck, p2, num)
                    self.status_update("Card drawn from deck to BOT hand")
                    if discard[-1].split('_')[1] == 'reverse' or discard[-1].split('_')[1] == 'skip' or \
                            discard[-1].split('_')[1] == 'draw2':
                        self.switch_players()
                else:
                    self.draw_card(p2, discard, num)
                    self.status_update(f"{discard[-1]} played by BOT")


    def legal_move(self):
        global change, color, player
        legal = []

        if change == 1:
            played = color
            change = 0
        else:
            played = discard[-1]  # chooses last card played

        #print("PLAYED: ", played)
        if '_' in played:
            words = played.split('_')  # split the card name into color and number
            for available in player:  # check each card in player hand
                if words[0] in available:  # checks for matching color
                    legal.append(available)
                if words[1] in available:  # checks for matching number
                    if words[1] == '':
                        continue
                    flag = 0
                    for type in ['reverse', 'skip', 'draw2']:
                        if type in available:
                            flag = 1
                            break
                    if flag == 0:
                        legal.append(available)
                if 'WC' in available or 'W+4' in available:  # checks for wildcards
                    legal.append(available)
            legal = list(set(legal))  # removes duplicates by converting to set and back
        else:
            for card in player:
                legal.append(card)

        if not legal:
            return -1

        return legal

    def ai(self):
        legal = self.legal_move()
        print("LEGAL MOVES: ", legal)
        if legal == -1:
            return -1
        else:
            if 'W+4' in legal:
                return p2.index('W+4')
            elif 'WC' in legal:
                return p2.index('WC')
            for card in legal:
                for type in ['reverse', 'skip', 'draw2']:
                    if type in card:
                        return p2.index(card)
            for card in legal:
                for i in range(9, -1, -1):
                    if str(i) in card:
                        return p2.index(card)

    def switch_players(self):
        global player
        if player == p1:
            player = p2
        else:
            player = p1

    def draw_card(self, from_deck=deck, to_deck=discard, val=0):
        to_deck.append(from_deck.pop(val))
        return to_deck[-1]

    def checkwin(self):
        if len(p1) == 0:
            self.clear_deck()
            self.result(1)
            print("YOU WIN!")
            return 1
        elif len(p2) == 0:
            self.clear_deck()
            self.bot_count.setText(f"{len(p2)}")
            self.result(0)
            print("YOU LOSE!")
            return -1
        else:
            return 0

    # to choose color change
    def change_color(self, player):
        global click, discard
        click = 0
        ai_pick = []
        if player == p1:
            global color
            self.button_display(True)
            while click == 0:
                QCoreApplication.processEvents()
            click = 1
            return color
        else:
            for card in p2:
                if card.split('_')[0] == 'red':
                    ai_pick.append('red_')
                if card.split('_')[0] == 'yellow':
                    ai_pick.append('yellow_')
                if card.split('_')[0] == 'green':
                    ai_pick.append('green_')
                if card.split('_')[0] == 'blue':
                    ai_pick.append('blue_')

            ai_pick = list(set(ai_pick))
            color = random.choice(ai_pick)
            discard[-1] = color
            return color
        '''
        print(color)
        if color == 1:
            return 'red_'
        elif color == 2:
            return 'yellow_'
        elif color == 3:
            return 'green_'
        elif color == 4:
            return 'blue_'
        '''

    # to configure special card effects
    def special_case(self):
        global change, color, deck, discard, player
        if discard[-1] == 'W+4':
            color = self.change_color(player)
            change = 1
            self.switch_players()
            i = 4
            while (i > 0):
                self.draw_card(deck, player, 0)
                i = i - 1
        elif discard[-1] == 'WC':
            color = self.change_color(player)
            change = 1
        elif discard[-1].split('_')[1] == 'reverse' or discard[-1].split('_')[1] == 'skip':
            self.switch_players()
        elif discard[-1].split('_')[1] == 'draw2':
            self.switch_players()
            i = 2
            while (i > 0):
                self.draw_card(deck, player, 0)
                i = i - 1

        #print("COLOR INSIDE FUNCTION: ", color)
        if change == 1:
            discard[-1] = color




#initialize app
app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()