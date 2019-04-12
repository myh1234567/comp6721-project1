import tkinter as Tk
import threading
import time
from random import randint
frame = Tk.Tk()
frame.title("game board")

file=""
# 棋盘添加最下方label 设置A-H
lookup=["A","B","C","D","E","F","G","H"]
# 输出positon时用
lookup_dic={1:"A",2:"B",3:"C",4:"D",5:"E",6:"F",7:"G",8:"H"}
cardtype_dic={0:"4",1:"2",2:"6",3:"8",4:"1",5:"3",6:"7",7:"5"}
# 文字的棋盘和gui对应的
board=[]
# 记步
stepcount=1
hecallcount=0
level2he = []

# 记是reomove状态还是放置状态
after24remove=True
lastremovecardtype=-1
lastremovecardposition=[[0,0],[0,0]]
AI_lastremovecardposition=[[0,0],[0,0]]

# 保存棋盘
lablelist=[]

AI_minmax_status = False
# 查现在该谁下 and 上一步sei下的
current_player="A"

game_finished=False

# True  = player1 is AI
# False = player2 is AI
player1isAI = False

#False=Color True=Dot
playerA_Select=True

# True=PlayerB False=AI
playerBorAI = True

xycardtype = []
canclexy = []
cancle_list2 = []
nengxiana_list2 = []
en_result = 0

# 把横竖斜的数据统计过来，只是记述，返回list的一个长表
def check_winning_result(x,y):
    count_result=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]  #黑点,白点,红底,白底 顺序是 竖 横 左下又上 右下左上
    switch=[True,True,True,True] #初始化四个true，然后只要不一样就变false了，有false了后面就不会再记数了
    # switch的true false表还有count result合起来算赢没赢，单纯计数没用，中间穿插别的但是还计数，输出结果就是错的

    # startx y是计下的地方，和相关的，然后进行比较
    startx=x
    starty=y

    # 换坐标
    ax=12-x
    ay=y-1

    # j把ax ay换成label的下标
    j=ax*8+ay
    if lablelist[j].cget("text")=="●":
        count_result[0][0]+=1
        count_result[1][0]+=1
        count_result[2][0]+=1
        count_result[3][0]+=1
    elif lablelist[j].cget("text")=="○":
        count_result[0][1]+=1
        count_result[1][1]+=1
        count_result[2][1]+=1
        count_result[3][1]+=1
    if lablelist[j].cget("bg")=="red":
        count_result[0][2]+=1
        count_result[1][2]+=1
        count_result[2][2]+=1
        count_result[3][2]+=1
    elif lablelist[j].cget("bg")=="white":
        count_result[0][3]+=1
        count_result[1][3]+=1
        count_result[2][3]+=1
        count_result[3][3]+=1
    #开始计数了
    for i in range(1,4,1):
        if x+i>12:
            break
        ax=12-(x+i)
        ay=y-1
        j=ax*8+ay
        if board[j][1:3]=="00":
            break
        ax=12-startx
        ay=starty-1
        sj=ax*8+ay
        # j是扫描的点，sj是原始的点 start j
        if lablelist[j].cget("text")==lablelist[sj].cget("text"):
            if lablelist[j].cget("text")=="●":
                if switch[0]==True:
                    count_result[0][0]+=1
            elif lablelist[j].cget("text")=="○":
                if switch[1]==True:
                    count_result[0][1]+=1
        else:
            if lablelist[j].cget("text")=="●":
                switch[1]=False
            elif lablelist[j].cget("text")=="○":
                switch[0]=False
        if lablelist[j].cget("bg")==lablelist[sj].cget("bg"):
            if lablelist[j].cget("bg")=="red":
                if switch[2]==True:
                    count_result[0][2]+=1
            elif lablelist[j].cget("bg")=="white":
                if switch[3]==True:
                    count_result[0][3]+=1
        else:
            if lablelist[j].cget("bg")=="red":
                switch[3]=False
            elif lablelist[j].cget("bg")=="white":
                switch[2]=False

    switch=[True,True,True,True]
    for i in range(1,4,1):
        if x-i<1:
            break
        ax=12-(x-i)
        ay=y-1
        j=ax*8+ay
        if board[j][1:3]=="00":
            break
        ax=12-startx
        ay=starty-1
        sj=ax*8+ay
        if lablelist[j].cget("text")==lablelist[sj].cget("text"):
            if lablelist[j].cget("text")=="●":
                if switch[0]==True:
                    count_result[0][0]+=1
            elif lablelist[j].cget("text")=="○":
                if switch[1]==True:
                    count_result[0][1]+=1
        else:
            if lablelist[j].cget("text")=="●":
                switch[1]=False
            elif lablelist[j].cget("text")=="○":
                switch[0]=False
        if lablelist[j].cget("bg")==lablelist[sj].cget("bg"):
            if lablelist[j].cget("bg")=="red":
                if switch[2]==True:
                    count_result[0][2]+=1
            elif lablelist[j].cget("bg")=="white":
                if switch[3]==True:
                    count_result[0][3]+=1
        else:
            if lablelist[j].cget("bg")=="red":
                switch[3]=False
            elif lablelist[j].cget("bg")=="white":
                switch[2]=False
    switch=[True,True,True,True]
    for i in range(1,4,1):
        if y-i<1:
            break
        ax=12-x
        ay=(y-i)-1
        j=ax*8+ay
        if board[j][1:3]=="00":
            break
        ax=12-startx
        ay=starty-1
        sj=ax*8+ay
        if lablelist[j].cget("text")==lablelist[sj].cget("text"):
            if lablelist[j].cget("text")=="●":
                if switch[0]==True:
                    count_result[1][0]+=1
            elif lablelist[j].cget("text")=="○":
                if switch[1]==True:
                    count_result[1][1]+=1
        else:
            if lablelist[j].cget("text")=="●":
                switch[1]=False
            elif lablelist[j].cget("text")=="○":
                switch[0]=False
        if lablelist[j].cget("bg")==lablelist[sj].cget("bg"):
            if lablelist[j].cget("bg")=="red":
                if switch[2]==True:
                    count_result[1][2]+=1
            elif lablelist[j].cget("bg")=="white":
                if switch[3]==True:
                    count_result[1][3]+=1
        else:
            if lablelist[j].cget("bg")=="red":
                switch[3]=False
            elif lablelist[j].cget("bg")=="white":
                switch[2]=False
    switch=[True,True,True,True]
    for i in range(1,4,1):
        if y+i>8:
            break
        ax=12-x
        ay=(y+i)-1
        j=ax*8+ay
        if board[j][1:3]=="00":
            break
        ax=12-startx
        ay=starty-1
        sj=ax*8+ay
        if lablelist[j].cget("text")==lablelist[sj].cget("text"):
            if lablelist[j].cget("text")=="●":
                if switch[0]==True:
                    count_result[1][0]+=1
            elif lablelist[j].cget("text")=="○":
                if switch[1]==True:
                    count_result[1][1]+=1
        else:
            if lablelist[j].cget("text")=="●":
                switch[1]=False
            elif lablelist[j].cget("text")=="○":
                switch[0]=False
        if lablelist[j].cget("bg")==lablelist[sj].cget("bg"):
            if lablelist[j].cget("bg")=="red":
                if switch[2]==True:
                    count_result[1][2]+=1
            elif lablelist[j].cget("bg")=="white":
                if switch[3]==True:
                    count_result[1][3]+=1
        else:
            if lablelist[j].cget("bg")=="red":
                switch[3]=False
            elif lablelist[j].cget("bg")=="white":
                switch[2]=False
    switch=[True,True,True,True]
    for i in range(1,4,1):
        if y-i<1 or x-i<1:
            break
        ax=12-(x-i)
        ay=(y-i)-1
        j=ax*8+ay
        if board[j][1:3]=="00":
            break
        ax=12-startx
        ay=starty-1
        sj=ax*8+ay
        if lablelist[j].cget("text")==lablelist[sj].cget("text"):
            if lablelist[j].cget("text")=="●":
                if switch[0]==True:
                    count_result[2][0]+=1
            elif lablelist[j].cget("text")=="○":
                if switch[1]==True:
                    count_result[2][1]+=1
        else:
            if lablelist[j].cget("text")=="●":
                switch[1]=False
            elif lablelist[j].cget("text")=="○":
                switch[0]=False
        if lablelist[j].cget("bg")==lablelist[sj].cget("bg"):
            if lablelist[j].cget("bg")=="red":
                if switch[2]==True:
                    count_result[2][2]+=1
            elif lablelist[j].cget("bg")=="white":
                if switch[3]==True:
                    count_result[2][3]+=1
        else:
            if lablelist[j].cget("bg")=="red":
                switch[3]=False
            elif lablelist[j].cget("bg")=="white":
                switch[2]=False
    switch=[True,True,True,True]
    for i in range(1,4,1):
        if y+i>8 or x+i>12:
            break
        ax=12-(x+i)
        ay=(y+i)-1
        j=ax*8+ay
        if board[j][1:3]=="00":
            break
        ax=12-startx
        ay=starty-1
        sj=ax*8+ay
        if lablelist[j].cget("text")==lablelist[sj].cget("text"):
            if lablelist[j].cget("text")=="●":
                if switch[0]==True:
                    count_result[2][0]+=1
            elif lablelist[j].cget("text")=="○":
                if switch[1]==True:
                    count_result[2][1]+=1
        else:
            if lablelist[j].cget("text")=="●":
                switch[1]=False
            elif lablelist[j].cget("text")=="○":
                switch[0]=False
        if lablelist[j].cget("bg")==lablelist[sj].cget("bg"):
            if lablelist[j].cget("bg")=="red":
                if switch[2]==True:
                    count_result[2][2]+=1
            elif lablelist[j].cget("bg")=="white":
                if switch[3]==True:
                    count_result[2][3]+=1
        else:
            if lablelist[j].cget("bg")=="red":
                switch[3]=False
            elif lablelist[j].cget("bg")=="white":
                switch[2]=False
    switch=[True,True,True,True]
    for i in range(1,4,1):
        if y-i<1 or x+i>12:
            break
        ax=12-(x+i)
        ay=(y-i)-1
        j=ax*8+ay
        if board[j][1:3]=="00":
            break
        ax=12-startx
        ay=starty-1
        sj=ax*8+ay
        if lablelist[j].cget("text")==lablelist[sj].cget("text"):
            if lablelist[j].cget("text")=="●":
                if switch[0]==True:
                    count_result[3][0]+=1
            elif lablelist[j].cget("text")=="○":
                if switch[1]==True:
                    count_result[3][1]+=1
        else:
            if lablelist[j].cget("text")=="●":
                switch[1]=False
            elif lablelist[j].cget("text")=="○":
                switch[0]=False
        if lablelist[j].cget("bg")==lablelist[sj].cget("bg"):
            if lablelist[j].cget("bg")=="red":
                if switch[2]==True:
                    count_result[3][2]+=1
            elif lablelist[j].cget("bg")=="white":
                if switch[3]==True:
                    count_result[3][3]+=1
        else:
            if lablelist[j].cget("bg")=="red":
                switch[3]=False
            elif lablelist[j].cget("bg")=="white":
                switch[2]=False
    switch=[True,True,True,True]
    for i in range(1,4,1):
        if y+i>8 or x-i<1:
            break
        ax=12-(x-i)
        ay=(y+i)-1
        j=ax*8+ay
        if board[j][1:3]=="00":
            break
        ax=12-startx
        ay=starty-1
        sj=ax*8+ay
        if lablelist[j].cget("text")==lablelist[sj].cget("text"):
            if lablelist[j].cget("text")=="●":
                if switch[0]==True:
                    count_result[3][0]+=1
            elif lablelist[j].cget("text")=="○":
                if switch[1]==True:
                    count_result[3][1]+=1
        else:
            if lablelist[j].cget("text")=="●":
                switch[1]=False
            elif lablelist[j].cget("text")=="○":
                switch[0]=False
        if lablelist[j].cget("bg")==lablelist[sj].cget("bg"):
            if lablelist[j].cget("bg")=="red":
                if switch[2]==True:
                    count_result[3][2]+=1
            elif lablelist[j].cget("bg")=="white":
                if switch[3]==True:
                    count_result[3][3]+=1
        else:
            if lablelist[j].cget("bg")=="red":
                switch[3]=False
            elif lablelist[j].cget("bg")=="white":
                switch[2]=False
    return count_result

'''
def AI_check_winning_result(x,y,cardtype,board):
    count_result=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]  #黑点,白点,红底,白底 顺序是 竖 横 左下又上 右下左上
    switch=[True,True,True,True]

    startx=x
    starty=y

    ax=12-x
    ay=y-1
    j=ax*8+ay
    # if lablelist[j].cget("text")=="●":
    if cardtype in ["0","2","4","6"]:
        count_result[0][0]+=1
        count_result[1][0]+=1
        count_result[2][0]+=1
        count_result[3][0]+=1
    # elif lablelist[j].cget("text")=="○":
    elif cardtype in ["1","3","5","7"]:
        count_result[0][1]+=1
        count_result[1][1]+=1
        count_result[2][1]+=1
        count_result[3][1]+=1
    # if lablelist[j].cget("bg")=="red":
    if cardtype in ["0","3","4","7"]:
        count_result[0][2]+=1
        count_result[1][2]+=1
        count_result[2][2]+=1
        count_result[3][2]+=1
    # elif lablelist[j].cget("bg")=="white":
    elif cardtype in ["1","2","5","6"]:
        count_result[0][3]+=1
        count_result[1][3]+=1
        count_result[2][3]+=1
        count_result[3][3]+=1
    #开始计数了
    for i in range(1,4,1):
        if x+i>12:
            break
        ax=12-(x+i)
        ay=y-1
        j=ax*8+ay
        if board[j][1:3]=="00":
            break
        ax=12-startx
        ay=starty-1
        sj=ax*8+ay

        if board[j][3] == "0":
            if x+i == 12 or board[j] == board[j-8]:
                if cardtype == "0" or cardtype == "4":
                    if switch[0] == True:
                        count_result[0][0] += 1
                    if switch[2] == True:
                        count_result[0][2] += 1
                elif cardtype == "2" or cardtype == "6":
                    if switch[0] == True:
                        count_result[0][0] += 1
                    switch[3] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[2] == True:
                        count_result[0][2] += 1
                    switch[1] = False
                else:
                    switch[1] = False
                    switch[3] = False
            elif board[j] == board[j+8]:
                if cardtype == "0" or cardtype == "4":
                    switch[0] = False
                    switch[2] = False
                elif cardtype == "2" or cardtype == "6":
                    if switch[3] == True:
                        count_result[0][3] += 1
                    switch[0] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[1] == True:
                        count_result[0][1] += 1
                    switch[2] = False
                else:
                    if switch[1] == True:
                        count_result[0][1] += 1
                    if switch[3] == True:
                        count_result[0][3] += 1
        if board[j][3] == "1":
            if x+i == 12 or board[j] == board[j-8]:
                if cardtype == "0" or cardtype == "4":
                    switch[0] = False
                    switch[2] = False
                elif cardtype == "2" or cardtype == "6":
                    if switch[3] == True:
                        count_result[0][3] += 1
                    switch[0] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[1] == True:
                        count_result[0][1] += 1
                    switch[2] = False
                else:
                    if switch[1] == True:
                        count_result[0][1] += 1
                    if switch[3] == True:
                        count_result[0][3] += 1
            elif board[j] == board[j+8]:
                if cardtype == "0" or cardtype == "4":
                    if switch[0] == True:
                        count_result[0][0] += 1
                    if switch[2] == True:
                        count_result[0][2] += 1
                elif cardtype == "2" or cardtype == "6":
                    if switch[0] == True:
                        count_result[0][0] += 1
                    switch[3] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[2] == True:
                        count_result[0][2] += 1
                    switch[1] = False
                else:
                    switch[1] = False
                    switch[3] = False
        if board[j][3] == "2":
            if x+i == 12 or board[j] == board[j-8]:
                if cardtype == "0" or cardtype == "4":
                    if switch[0] == True:
                        count_result[0][0] += 1
                    switch[2] = False
                elif cardtype == "2" or cardtype == "6":
                    if switch[0] == True:
                        count_result[0][0] += 1
                    if switch[3] == True:
                        count_result[0][3] += 1
                elif cardtype == "3" or cardtype == "7":
                    switch[2] = False
                    switch[1] = False
                else:
                    switch[1] = False
                    if switch[3] == True:
                        count_result[0][3] += 1
            elif board[j] == board[j+8]:
                if cardtype == "0" or cardtype == "4":
                    if switch[2] == True:
                        count_result[0][2] += 1
                    switch[0] = False
                elif cardtype == "2" or cardtype == "6":
                    switch[3] = False
                    switch[0] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[1] == True:
                        count_result[0][1] += 1
                    if switch[2] == True:
                        count_result[0][2] += 1
                else:
                    if switch[1] == True:
                        count_result[0][1] += 1
                    switch[3] = False
        if board[j][3] == "3":
            if x+i == 12 or board[j] == board[j-8]:
                if cardtype == "0" or cardtype == "4":
                    if switch[2] == True:
                        count_result[0][2] += 1
                    switch[0] = False
                elif cardtype == "2" or cardtype == "6":
                    switch[0] = False
                    switch[3] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[1] == True:
                        count_result[0][1] += 1
                    if switch[2] == True:
                        count_result[0][2] += 1
                else:
                    if switch[1] == True:
                        count_result[0][1] += 1
                    switch[3] = False
            elif board[j] == board[j+8]:
                if cardtype == "0" or cardtype == "4":
                    if switch[0] == True:
                        count_result[0][0] += 1
                    switch[2] = False
                elif cardtype == "2" or cardtype == "6":
                    if switch[0] == True:
                        count_result[0][0] += 1
                    if switch[3] == True:
                        count_result[0][3] += 1
                elif cardtype == "3" or cardtype == "7":
                    switch[2] = False
                    switch[1] = False
                else:
                    switch[1] = False
                    if switch[3] == True:
                        count_result[0][3] += 1
        if board[j][3] == "4":
            if y == 1 or (y < 8 and board[j] == board[j + 1]):
                if cardtype == "0" or cardtype == "4":
                    if switch[0] == True:
                        count_result[0][0] += 1
                    if switch[2] == True:
                        count_result[0][2] += 1
                elif cardtype == "2" or cardtype == "6":
                    if switch[0] == True:
                        count_result[0][0] += 1
                    switch[3] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[2] == True:
                        count_result[0][2] += 1
                    switch[1] = False
                else:
                    switch[1] = False
                    switch[3] = False
            elif board[j] == board[j-1]:
                if cardtype == "0" or cardtype == "4":
                    switch[0] = False
                    switch[2] = False
                elif cardtype == "2" or cardtype == "6":
                    if switch[3] == True:
                        count_result[0][3] += 1
                    switch[0] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[1] == True:
                        count_result[0][1] += 1
                    switch[2] = False
                else:
                    if switch[1] == True:
                        count_result[0][1] += 1
                    if switch[3] == True:
                        count_result[0][3] += 1
        if board[j][3] == "5":
            if y == 1 or (y < 8 and board[j] == board[j + 1]):
                if cardtype == "0" or cardtype == "4":
                    switch[0] = False
                    switch[2] = False
                elif cardtype == "2" or cardtype == "6":
                    if switch[3] == True:
                        count_result[0][3] += 1
                    switch[0] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[1] == True:
                        count_result[0][1] += 1
                    switch[2] = False
                else:
                    if switch[1] == True:
                        count_result[0][1] += 1
                    if switch[3] == True:
                        count_result[0][3] += 1
            elif board[j] == board[j-1]:
                if cardtype == "0" or cardtype == "4":
                    if switch[0] == True:
                        count_result[0][0] += 1
                    if switch[2] == True:
                        count_result[0][2] += 1
                elif cardtype == "2" or cardtype == "6":
                    if switch[0] == True:
                        count_result[0][0] += 1
                    switch[3] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[2] == True:
                        count_result[0][2] += 1
                    switch[1] = False
                else:
                    switch[1] = False
                    switch[3] = False
        if board[j][3] == "6":
            if y == 1 or (y < 8 and board[j] == board[j + 1]):
                if cardtype == "0" or cardtype == "4":
                    if switch[0] == True:
                        count_result[0][0] += 1
                    switch[2] = False
                elif cardtype == "2" or cardtype == "6":
                    if switch[0] == True:
                        count_result[0][0] += 1
                    if switch[3] == True:
                        count_result[0][3] += 1
                elif cardtype == "3" or cardtype == "7":
                    switch[2] = False
                    switch[1] = False
                else:
                    switch[1] = False
                    if switch[3] == True:
                        count_result[0][3] += 1
            elif board[j] == board[j-1]:
                if cardtype == "0" or cardtype == "4":
                    if switch[2] == True:
                        count_result[0][2] += 1
                    switch[0] = False
                elif cardtype == "2" or cardtype == "6":
                    switch[3] = False
                    switch[0] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[1] == True:
                        count_result[0][1] += 1
                    if switch[2] == True:
                        count_result[0][2] += 1
                else:
                    if switch[1] == True:
                        count_result[0][1] += 1
                    switch[3] = False
        if board[j][3] == "7":
            if y == 1 or (y < 8 and board[j] == board[j + 1]):
                if cardtype == "0" or cardtype == "4":
                    if switch[2] == True:
                        count_result[0][2] += 1
                    switch[0] = False
                elif cardtype == "2" or cardtype == "6":
                    switch[0] = False
                    switch[3] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[1] == True:
                        count_result[0][1] += 1
                    if switch[2] == True:
                        count_result[0][2] += 1
                else:
                    if switch[1] == True:
                        count_result[0][1] += 1
                    switch[3] = False
            elif board[j] == board[j-1]:
                if cardtype == "0" or cardtype == "4":
                    if switch[0] == True:
                        count_result[0][0] += 1
                    switch[2] = False
                elif cardtype == "2" or cardtype == "6":
                    if switch[0] == True:
                        count_result[0][0] += 1
                    if switch[3] == True:
                        count_result[0][3] += 1
                elif cardtype == "3" or cardtype == "7":
                    switch[2] = False
                    switch[1] = False
                else:
                    switch[1] = False
                    if switch[3] == True:
                        count_result[0][3] += 1

    switch=[True,True,True,True]
    for i in range(1,4,1):
        if x-i<1:
            break
        ax=12-(x-i)
        ay=y-1
        j=ax*8+ay
        if board[j][1:3]=="00":
            break
        ax=12-startx
        ay=starty-1
        sj=ax*8+ay

        if board[j][3] == "0":
            if x-i == 1 or board[j] == board[j-8]:
                if cardtype == "0" or cardtype == "4":
                    if switch[0] == True:
                        count_result[0][0] += 1
                    if switch[2] == True:
                        count_result[0][2] += 1
                elif cardtype == "2" or cardtype == "6":
                    if switch[0] == True:
                        count_result[0][0] += 1
                    switch[3] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[2] == True:
                        count_result[0][2] += 1
                    switch[1] = False
                else:
                    switch[1] = False
                    switch[3] = False
            elif board[j] == board[j+8]:
                if cardtype == "0" or cardtype == "4":
                    switch[0] = False
                    switch[2] = False
                elif cardtype == "2" or cardtype == "6":
                    if switch[3] == True:
                        count_result[0][3] += 1
                    switch[0] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[1] == True:
                        count_result[0][1] += 1
                    switch[2] = False
                else:
                    if switch[1] == True:
                        count_result[0][1] += 1
                    if switch[3] == True:
                        count_result[0][3] += 1

        if board[j][3] == "1":
            if x-i == 1 or board[j] == board[j-8]:
                if cardtype == "0" or cardtype == "4":
                    switch[0] = False
                    switch[2] = False
                elif cardtype == "2" or cardtype == "6":
                    if switch[3] == True:
                        count_result[0][3] += 1
                    switch[0] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[1] == True:
                        count_result[0][1] += 1
                    switch[2] = False
                else:
                    if switch[1] == True:
                        count_result[0][1] += 1
                    if switch[3] == True:
                        count_result[0][3] += 1
            elif board[j] == board[j+8]:
                if cardtype == "0" or cardtype == "4":
                    if switch[0] == True:
                        count_result[0][0] += 1
                    if switch[2] == True:
                        count_result[0][2] += 1
                elif cardtype == "2" or cardtype == "6":
                    if switch[0] == True:
                        count_result[0][0] += 1
                    switch[3] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[2] == True:
                        count_result[0][2] += 1
                    switch[1] = False
                else:
                    switch[1] = False
                    switch[3] = False

        if board[j][3] == "2":
            if x-i == 1 or board[j] == board[j-8]:
                if cardtype == "0" or cardtype == "4":
                    if switch[0] == True:
                        count_result[0][0] += 1
                    switch[2] = False
                elif cardtype == "2" or cardtype == "6":
                    if switch[0] == True:
                        count_result[0][0] += 1
                    if switch[3] == True:
                        count_result[0][3] += 1
                elif cardtype == "3" or cardtype == "7":
                    switch[2] = False
                    switch[1] = False
                else:
                    switch[1] = False
                    if switch[3] == True:
                        count_result[0][3] += 1
            elif board[j] == board[j+8]:
                if cardtype == "0" or cardtype == "4":
                    if switch[2] == True:
                        count_result[0][2] += 1
                    switch[0] = False
                elif cardtype == "2" or cardtype == "6":
                    switch[3] = False
                    switch[0] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[1] == True:
                        count_result[0][1] += 1
                    if switch[2] == True:
                        count_result[0][2] += 1
                else:
                    if switch[1] == True:
                        count_result[0][1] += 1
                    switch[3] = False

        if board[j][3] == "3":
            if x-i == 1 or board[j] == board[j-8]:
                if cardtype == "0" or cardtype == "4":
                    if switch[2] == True:
                        count_result[0][2] += 1
                    switch[0] = False
                elif cardtype == "2" or cardtype == "6":
                    switch[0] = False
                    switch[3] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[1] == True:
                        count_result[0][1] += 1
                    if switch[2] == True:
                        count_result[0][2] += 1
                else:
                    if switch[1] == True:
                        count_result[0][1] += 1
                    switch[3] = False
            elif board[j] == board[j+8]:
                if cardtype == "0" or cardtype == "4":
                    if switch[0] == True:
                        count_result[0][0] += 1
                    switch[2] = False
                elif cardtype == "2" or cardtype == "6":
                    if switch[0] == True:
                        count_result[0][0] += 1
                    if switch[3] == True:
                        count_result[0][3] += 1
                elif cardtype == "3" or cardtype == "7":
                    switch[2] = False
                    switch[1] = False
                else:
                    switch[1] = False
                    if switch[3] == True:
                        count_result[0][3] += 1


        if board[j][3] == "4":
            if y == 1 or (y <8 and board[j] == board[j+1]):
                if cardtype == "0" or cardtype == "4":
                    if switch[0] == True:
                        count_result[0][0] += 1
                    if switch[2] == True:
                        count_result[0][2] += 1
                elif cardtype == "2" or cardtype == "6":
                    if switch[0] == True:
                        count_result[0][0] += 1
                    switch[3] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[2] == True:
                        count_result[0][2] += 1
                    switch[1] = False
                else:
                    switch[1] = False
                    switch[3] = False
            elif board[j] == board[j-1]:
                if cardtype == "0" or cardtype == "4":
                    switch[0] = False
                    switch[2] = False
                elif cardtype == "2" or cardtype == "6":
                    if switch[3] == True:
                        count_result[0][3] += 1
                    switch[0] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[1] == True:
                        count_result[0][1] += 1
                    switch[2] = False
                else:
                    if switch[1] == True:
                        count_result[0][1] += 1
                    if switch[3] == True:
                        count_result[0][3] += 1
        if board[j][3] == "5":
            if y == 1 or (y <8 and board[j] == board[j+1]):
                if cardtype == "0" or cardtype == "4":
                    switch[0] = False
                    switch[2] = False
                elif cardtype == "2" or cardtype == "6":
                    if switch[3] == True:
                        count_result[0][3] += 1
                    switch[0] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[1] == True:
                        count_result[0][1] += 1
                    switch[2] = False
                else:
                    if switch[1] == True:
                        count_result[0][1] += 1
                    if switch[3] == True:
                        count_result[0][3] += 1
            elif board[j] == board[j-1]:
                if cardtype == "0" or cardtype == "4":
                    if switch[0] == True:
                        count_result[0][0] += 1
                    if switch[2] == True:
                        count_result[0][2] += 1
                elif cardtype == "2" or cardtype == "6":
                    if switch[0] == True:
                        count_result[0][0] += 1
                    switch[3] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[2] == True:
                        count_result[0][2] += 1
                    switch[1] = False
                else:
                    switch[1] = False
                    switch[3] = False
        if board[j][3] == "6":
            if y == 1 or (y <8 and board[j] == board[j+1]):
                if cardtype == "0" or cardtype == "4":
                    if switch[0] == True:
                        count_result[0][0] += 1
                    switch[2] = False
                elif cardtype == "2" or cardtype == "6":
                    if switch[0] == True:
                        count_result[0][0] += 1
                    if switch[3] == True:
                        count_result[0][3] += 1
                elif cardtype == "3" or cardtype == "7":
                    switch[2] = False
                    switch[1] = False
                else:
                    switch[1] = False
                    if switch[3] == True:
                        count_result[0][3] += 1
            elif board[j] == board[j-1]:
                if cardtype == "0" or cardtype == "4":
                    if switch[2] == True:
                        count_result[0][2] += 1
                    switch[0] = False
                elif cardtype == "2" or cardtype == "6":
                    switch[3] = False
                    switch[0] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[1] == True:
                        count_result[0][1] += 1
                    if switch[2] == True:
                        count_result[0][2] += 1
                else:
                    if switch[1] == True:
                        count_result[0][1] += 1
                    switch[3] = False
        if board[j][3] == "7":
            if y == 1 or (y < 8 and board[j] == board[j + 1]):
                if cardtype == "0" or cardtype == "4":
                    if switch[2] == True:
                        count_result[0][2] += 1
                    switch[0] = False
                elif cardtype == "2" or cardtype == "6":
                    switch[0] = False
                    switch[3] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[1] == True:
                        count_result[0][1] += 1
                    if switch[2] == True:
                        count_result[0][2] += 1
                else:
                    if switch[1] == True:
                        count_result[0][1] += 1
                    switch[3] = False
            elif board[j] == board[j-1]:
                if cardtype == "0" or cardtype == "4":
                    if switch[0] == True:
                        count_result[0][0] += 1
                    switch[2] = False
                elif cardtype == "2" or cardtype == "6":
                    if switch[0] == True:
                        count_result[0][0] += 1
                    if switch[3] == True:
                        count_result[0][3] += 1
                elif cardtype == "3" or cardtype == "7":
                    switch[2] = False
                    switch[1] = False
                else:
                    switch[1] = False
                    if switch[3] == True:
                        count_result[0][3] += 1

    switch=[True,True,True,True]
    for i in range(1,4,1):
        if y-i<1:
            break
        ax=12-x
        ay=(y-i)-1
        j=ax*8+ay
        if board[j][1:3]=="00":
            break
        ax=12-startx
        ay=starty-1
        sj=ax*8+ay

        if board[j][3] == "0":
            if x == 1 or (x < 12 and board[j] == board[j - 8]):
                if cardtype == "0" or cardtype == "4":
                    if switch[0] == True:
                        count_result[1][0] += 1
                    if switch[2] == True:
                        count_result[1][2] += 1
                elif cardtype == "2" or cardtype == "6":
                    if switch[0] == True:
                        count_result[1][0] += 1
                    switch[3] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[2] == True:
                        count_result[1][2] += 1
                    switch[1] = False
                else:
                    switch[1] = False
                    switch[3] = False
            elif board[j] == board[j + 8]:
                if cardtype == "0" or cardtype == "4":
                    switch[0] = False
                    switch[2] = False
                elif cardtype == "2" or cardtype == "6":
                    if switch[3] == True:
                        count_result[1][3] += 1
                    switch[0] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[1] == True:
                        count_result[1][1] += 1
                    switch[2] = False
                else:
                    if switch[1] == True:
                        count_result[1][1] += 1
                    if switch[3] == True:
                        count_result[1][3] += 1

        if board[j][3] == "1":
            if x == 1 or (x < 12 and board[j] == board[j - 8]):
                if cardtype == "0" or cardtype == "4":
                    switch[0] = False
                    switch[2] = False
                elif cardtype == "2" or cardtype == "6":
                    if switch[3] == True:
                        count_result[1][3] += 1
                    switch[0] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[1] == True:
                        count_result[1][1] += 1
                    switch[2] = False
                else:
                    if switch[1] == True:
                        count_result[1][1] += 1
                    if switch[3] == True:
                        count_result[1][3] += 1
            elif board[j] == board[j+8]:
                if cardtype == "0" or cardtype == "4":
                    if switch[0] == True:
                        count_result[1][0] += 1
                    if switch[2] == True:
                        count_result[1][2] += 1
                elif cardtype == "2" or cardtype == "6":
                    if switch[0] == True:
                        count_result[1][0] += 1
                    switch[3] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[2] == True:
                        count_result[1][2] += 1
                    switch[1] = False
                else:
                    switch[1] = False
                    switch[3] = False
        if board[j][3] == "2":
            if x == 1 or (x < 12 and board[j] == board[j - 8]):
                if cardtype == "0" or cardtype == "4":
                    if switch[0] == True:
                        count_result[1][0] += 1
                    switch[2] = False
                elif cardtype == "2" or cardtype == "6":
                    if switch[0] == True:
                        count_result[1][0] += 1
                    if switch[3] == True:
                        count_result[1][3] += 1
                elif cardtype == "3" or cardtype == "7":
                    switch[2] = False
                    switch[1] = False
                else:
                    switch[1] = False
                    if switch[3] == True:
                        count_result[1][3] += 1
            elif board[j] == board[j+8]:
                if cardtype == "0" or cardtype == "4":
                    if switch[2] == True:
                        count_result[1][2] += 1
                    switch[0] = False
                elif cardtype == "2" or cardtype == "6":
                    switch[3] = False
                    switch[0] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[1] == True:
                        count_result[1][1] += 1
                    if switch[2] == True:
                        count_result[1][2] += 1
                else:
                    if switch[1] == True:
                        count_result[1][1] += 1
                    switch[3] = False
        if board[j][3] == "3":
            if x+i == 12 or board[j] == board[j-8]:
                if cardtype == "0" or cardtype == "4":
                    if switch[2] == True:
                        count_result[1][2] += 1
                    switch[0] = False
                elif cardtype == "2" or cardtype == "6":
                    switch[0] = False
                    switch[3] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[1] == True:
                        count_result[1][1] += 1
                    if switch[2] == True:
                        count_result[1][2] += 1
                else:
                    if switch[1] == True:
                        count_result[1][1] += 1
                    switch[3] = False
            elif board[j] == board[j+8]:
                if cardtype == "0" or cardtype == "4":
                    if switch[0] == True:
                        count_result[1][0] += 1
                    switch[2] = False
                elif cardtype == "2" or cardtype == "6":
                    if switch[0] == True:
                        count_result[1][0] += 1
                    if switch[3] == True:
                        count_result[1][3] += 1
                elif cardtype == "3" or cardtype == "7":
                    switch[2] = False
                    switch[1] = False
                else:
                    switch[1] = False
                    if switch[3] == True:
                        count_result[1][3] += 1

        if board[j][3] == "4":
            if y-i == 1 or (y < 8 and board[j] == board[j + 1]):
                if cardtype == "0" or cardtype == "4":
                    if switch[0] == True:
                        count_result[1][0] += 1
                    if switch[2] == True:
                        count_result[1][2] += 1
                elif cardtype == "2" or cardtype == "6":
                    if switch[0] == True:
                        count_result[1][0] += 1
                    switch[3] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[2] == True:
                        count_result[1][2] += 1
                    switch[1] = False
                else:
                    switch[1] = False
                    switch[3] = False
            elif y-i > 1 and board[j] == board[j - 1]:
                if cardtype == "0" or cardtype == "4":
                    switch[0] = False
                    switch[2] = False
                elif cardtype == "2" or cardtype == "6":
                    if switch[3] == True:
                        count_result[1][3] += 1
                    switch[0] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[1] == True:
                        count_result[1][1] += 1
                    switch[2] = False
                else:
                    if switch[1] == True:
                        count_result[1][1] += 1
                    if switch[3] == True:
                        count_result[1][3] += 1
        if board[j][3] == "5":
            if y-i == 1 or (y < 8 and board[j] == board[j + 1]):
                if cardtype == "0" or cardtype == "4":
                    switch[0] = False
                    switch[2] = False
                elif cardtype == "2" or cardtype == "6":
                    if switch[3] == True:
                        count_result[1][3] += 1
                    switch[0] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[1] == True:
                        count_result[1][1] += 1
                    switch[2] = False
                else:
                    if switch[1] == True:
                        count_result[1][1] += 1
                    if switch[3] == True:
                        count_result[1][3] += 1
            elif y - i > 1 and board[j] == board[j - 1]:
                if cardtype == "0" or cardtype == "4":
                    if switch[0] == True:
                        count_result[1][0] += 1
                    if switch[2] == True:
                        count_result[1][2] += 1
                elif cardtype == "2" or cardtype == "6":
                    if switch[0] == True:
                        count_result[1][0] += 1
                    switch[3] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[2] == True:
                        count_result[1][2] += 1
                    switch[1] = False
                else:
                    switch[1] = False
                    switch[3] = False
        if board[j][3] == "6":
            if y - i == 1 or (y < 8 and board[j] == board[j + 1]):
                if cardtype == "0" or cardtype == "4":
                    if switch[0] == True:
                        count_result[1][0] += 1
                    switch[2] = False
                elif cardtype == "2" or cardtype == "6":
                    if switch[0] == True:
                        count_result[1][0] += 1
                    if switch[3] == True:
                        count_result[1][3] += 1
                elif cardtype == "3" or cardtype == "7":
                    switch[2] = False
                    switch[1] = False
                else:
                    switch[1] = False
                    if switch[3] == True:
                        count_result[1][3] += 1
            elif y - i > 1 and board[j] == board[j - 1]:
                if cardtype == "0" or cardtype == "4":
                    if switch[2] == True:
                        count_result[1][2] += 1
                    switch[0] = False
                elif cardtype == "2" or cardtype == "6":
                    switch[3] = False
                    switch[0] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[1] == True:
                        count_result[1][1] += 1
                    if switch[2] == True:
                        count_result[1][2] += 1
                else:
                    if switch[1] == True:
                        count_result[1][1] += 1
                    switch[3] = False
        if board[j][3] == "7":
            if y - i == 1 or (y < 8 and board[j] == board[j + 1]):
                if cardtype == "0" or cardtype == "4":
                    if switch[2] == True:
                        count_result[1][2] += 1
                    switch[0] = False
                elif cardtype == "2" or cardtype == "6":
                    switch[0] = False
                    switch[3] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[1] == True:
                        count_result[1][1] += 1
                    if switch[2] == True:
                        count_result[1][2] += 1
                else:
                    if switch[1] == True:
                        count_result[1][1] += 1
                    switch[3] = False
            elif y - i > 1 and board[j] == board[j - 1]:
                if cardtype == "0" or cardtype == "4":
                    if switch[0] == True:
                        count_result[1][0] += 1
                    switch[2] = False
                elif cardtype == "2" or cardtype == "6":
                    if switch[0] == True:
                        count_result[1][0] += 1
                    if switch[3] == True:
                        count_result[1][3] += 1
                elif cardtype == "3" or cardtype == "7":
                    switch[2] = False
                    switch[1] = False
                else:
                    switch[1] = False
                    if switch[3] == True:
                        count_result[1][3] += 1

    switch=[True,True,True,True]
    for i in range(1,4,1):
        if y+i>8:
            break
        ax=12-x
        ay=(y+i)-1
        j=ax*8+ay
        if board[j][1:3]=="00":
            break
        ax=12-startx
        ay=starty-1
        sj=ax*8+ay

        if board[j][3] == "0":
            if x == 1 or (x < 12 and board[j] == board[j - 8]):
                if cardtype == "0" or cardtype == "4":
                    if switch[0] == True:
                        count_result[1][0] += 1
                    if switch[2] == True:
                        count_result[1][2] += 1
                elif cardtype == "2" or cardtype == "6":
                    if switch[0] == True:
                        count_result[1][0] += 1
                    switch[3] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[2] == True:
                        count_result[1][2] += 1
                    switch[1] = False
                else:
                    switch[1] = False
                    switch[3] = False
            elif board[j] == board[j + 8]:
                if cardtype == "0" or cardtype == "4":
                    switch[0] = False
                    switch[2] = False
                elif cardtype == "2" or cardtype == "6":
                    if switch[3] == True:
                        count_result[1][3] += 1
                    switch[0] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[1] == True:
                        count_result[1][1] += 1
                    switch[2] = False
                else:
                    if switch[1] == True:
                        count_result[1][1] += 1
                    if switch[3] == True:
                        count_result[1][3] += 1

        if board[j][3] == "1":
            if x == 1 or (x < 12 and board[j] == board[j - 8]):
                if cardtype == "0" or cardtype == "4":
                    switch[0] = False
                    switch[2] = False
                elif cardtype == "2" or cardtype == "6":
                    if switch[3] == True:
                        count_result[1][3] += 1
                    switch[0] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[1] == True:
                        count_result[1][1] += 1
                    switch[2] = False
                else:
                    if switch[1] == True:
                        count_result[1][1] += 1
                    if switch[3] == True:
                        count_result[1][3] += 1
            elif board[j] == board[j + 8]:
                if cardtype == "0" or cardtype == "4":
                    if switch[0] == True:
                        count_result[1][0] += 1
                    if switch[2] == True:
                        count_result[1][2] += 1
                elif cardtype == "2" or cardtype == "6":
                    if switch[0] == True:
                        count_result[1][0] += 1
                    switch[3] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[2] == True:
                        count_result[1][2] += 1
                    switch[1] = False
                else:
                    switch[1] = False
                    switch[3] = False
        if board[j][3] == "2":
            if x == 1 or (x < 12 and board[j] == board[j - 8]):
                if cardtype == "0" or cardtype == "4":
                    if switch[0] == True:
                        count_result[1][0] += 1
                    switch[2] = False
                elif cardtype == "2" or cardtype == "6":
                    if switch[0] == True:
                        count_result[1][0] += 1
                    if switch[3] == True:
                        count_result[1][3] += 1
                elif cardtype == "3" or cardtype == "7":
                    switch[2] = False
                    switch[1] = False
                else:
                    switch[1] = False
                    if switch[3] == True:
                        count_result[1][3] += 1
            elif board[j] == board[j + 8]:
                if cardtype == "0" or cardtype == "4":
                    if switch[2] == True:
                        count_result[1][2] += 1
                    switch[0] = False
                elif cardtype == "2" or cardtype == "6":
                    switch[3] = False
                    switch[0] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[1] == True:
                        count_result[1][1] += 1
                    if switch[2] == True:
                        count_result[1][2] += 1
                else:
                    if switch[1] == True:
                        count_result[1][1] += 1
                    switch[3] = False
        if board[j][3] == "3":
            if x + i == 12 or board[j] == board[j - 8]:
                if cardtype == "0" or cardtype == "4":
                    if switch[2] == True:
                        count_result[1][2] += 1
                    switch[0] = False
                elif cardtype == "2" or cardtype == "6":
                    switch[0] = False
                    switch[3] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[1] == True:
                        count_result[1][1] += 1
                    if switch[2] == True:
                        count_result[1][2] += 1
                else:
                    if switch[1] == True:
                        count_result[1][1] += 1
                    switch[3] = False
            elif board[j] == board[j + 8]:
                if cardtype == "0" or cardtype == "4":
                    if switch[0] == True:
                        count_result[1][0] += 1
                    switch[2] = False
                elif cardtype == "2" or cardtype == "6":
                    if switch[0] == True:
                        count_result[1][0] += 1
                    if switch[3] == True:
                        count_result[1][3] += 1
                elif cardtype == "3" or cardtype == "7":
                    switch[2] = False
                    switch[1] = False
                else:
                    switch[1] = False
                    if switch[3] == True:
                        count_result[1][3] += 1

        if board[j][3] == "4":
            if y + i == 1 or (y + i < 8 and board[j] == board[j + 1]):
                if cardtype == "0" or cardtype == "4":
                    if switch[0] == True:
                        count_result[1][0] += 1
                    if switch[2] == True:
                        count_result[1][2] += 1
                elif cardtype == "2" or cardtype == "6":
                    if switch[0] == True:
                        count_result[1][0] += 1
                    switch[3] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[2] == True:
                        count_result[1][2] += 1
                    switch[1] = False
                else:
                    switch[1] = False
                    switch[3] = False
            elif y + i > 1 and board[j] == board[j - 1]:
                if cardtype == "0" or cardtype == "4":
                    switch[0] = False
                    switch[2] = False
                elif cardtype == "2" or cardtype == "6":
                    if switch[3] == True:
                        count_result[1][3] += 1
                    switch[0] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[1] == True:
                        count_result[1][1] += 1
                    switch[2] = False
                else:
                    if switch[1] == True:
                        count_result[1][1] += 1
                    if switch[3] == True:
                        count_result[1][3] += 1
        if board[j][3] == "5":
            if y + i == 1 or (y + i < 8 and board[j] == board[j + 1]):
                if cardtype == "0" or cardtype == "4":
                    switch[0] = False
                    switch[2] = False
                elif cardtype == "2" or cardtype == "6":
                    if switch[3] == True:
                        count_result[1][3] += 1
                    switch[0] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[1] == True:
                        count_result[1][1] += 1
                    switch[2] = False
                else:
                    if switch[1] == True:
                        count_result[1][1] += 1
                    if switch[3] == True:
                        count_result[1][3] += 1
            elif y + i > 1 and board[j] == board[j - 1]:
                if cardtype == "0" or cardtype == "4":
                    if switch[0] == True:
                        count_result[1][0] += 1
                    if switch[2] == True:
                        count_result[1][2] += 1
                elif cardtype == "2" or cardtype == "6":
                    if switch[0] == True:
                        count_result[1][0] += 1
                    switch[3] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[2] == True:
                        count_result[1][2] += 1
                    switch[1] = False
                else:
                    switch[1] = False
                    switch[3] = False
        if board[j][3] == "6":
            if y + i == 1 or (y + i < 8 and board[j] == board[j + 1]):
                if cardtype == "0" or cardtype == "4":
                    if switch[0] == True:
                        count_result[1][0] += 1
                    switch[2] = False
                elif cardtype == "2" or cardtype == "6":
                    if switch[0] == True:
                        count_result[1][0] += 1
                    if switch[3] == True:
                        count_result[1][3] += 1
                elif cardtype == "3" or cardtype == "7":
                    switch[2] = False
                    switch[1] = False
                else:
                    switch[1] = False
                    if switch[3] == True:
                        count_result[1][3] += 1
            elif y + i > 1 and board[j] == board[j - 1]:
                if cardtype == "0" or cardtype == "4":
                    if switch[2] == True:
                        count_result[1][2] += 1
                    switch[0] = False
                elif cardtype == "2" or cardtype == "6":
                    switch[3] = False
                    switch[0] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[1] == True:
                        count_result[1][1] += 1
                    if switch[2] == True:
                        count_result[1][2] += 1
                else:
                    if switch[1] == True:
                        count_result[1][1] += 1
                    switch[3] = False
        if board[j][3] == "7":
            if y + i == 1 or (y + i < 8 and board[j] == board[j + 1]):
                if cardtype == "0" or cardtype == "4":
                    if switch[2] == True:
                        count_result[1][2] += 1
                    switch[0] = False
                elif cardtype == "2" or cardtype == "6":
                    switch[0] = False
                    switch[3] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[1] == True:
                        count_result[1][1] += 1
                    if switch[2] == True:
                        count_result[1][2] += 1
                else:
                    if switch[1] == True:
                        count_result[1][1] += 1
                    switch[3] = False
            elif y + i > 1 and board[j] == board[j - 1]:
                if cardtype == "0" or cardtype == "4":
                    if switch[0] == True:
                        count_result[1][0] += 1
                    switch[2] = False
                elif cardtype == "2" or cardtype == "6":
                    if switch[0] == True:
                        count_result[1][0] += 1
                    if switch[3] == True:
                        count_result[1][3] += 1
                elif cardtype == "3" or cardtype == "7":
                    switch[2] = False
                    switch[1] = False
                else:
                    switch[1] = False
                    if switch[3] == True:
                        count_result[1][3] += 1

    switch=[True,True,True,True]
    for i in range(1,4,1):
        if y-i<1 or x-i<1:
            break
        ax=12-(x-i)
        ay=(y-i)-1
        j=ax*8+ay
        if board[j][1:3]=="00":
            break
        ax=12-startx
        ay=starty-1
        sj=ax*8+ay

        if board[j][3] == "0":
            if x - i == 1 or (x - i < 12 and board[j] == board[j - 8]):
                if cardtype == "0" or cardtype == "4":
                    if switch[0] == True:
                        count_result[2][0] += 1
                    if switch[2] == True:
                        count_result[2][2] += 1
                elif cardtype == "2" or cardtype == "6":
                    if switch[0] == True:
                        count_result[2][0] += 1
                    switch[3] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[2] == True:
                        count_result[2][2] += 1
                    switch[1] = False
                else:
                    switch[1] = False
                    switch[3] = False
            elif board[j] == board[j + 8]:
                if cardtype == "0" or cardtype == "4":
                    switch[0] = False
                    switch[2] = False
                elif cardtype == "2" or cardtype == "6":
                    if switch[3] == True:
                        count_result[2][3] += 1
                    switch[0] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[1] == True:
                        count_result[2][1] += 1
                    switch[2] = False
                else:
                    if switch[1] == True:
                        count_result[2][1] += 1
                    if switch[3] == True:
                        count_result[2][3] += 1

        if board[j][3] == "1":
            if x - i == 1 or (x - i < 12 and board[j] == board[j - 8]):
                if cardtype == "0" or cardtype == "4":
                    switch[0] = False
                    switch[2] = False
                elif cardtype == "2" or cardtype == "6":
                    if switch[3] == True:
                        count_result[2][3] += 1
                    switch[0] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[1] == True:
                        count_result[2][1] += 1
                    switch[2] = False
                else:
                    if switch[1] == True:
                        count_result[2][1] += 1
                    if switch[3] == True:
                        count_result[2][3] += 1
            elif board[j] == board[j + 8]:
                if cardtype == "0" or cardtype == "4":
                    if switch[0] == True:
                        count_result[2][0] += 1
                    if switch[2] == True:
                        count_result[2][2] += 1
                elif cardtype == "2" or cardtype == "6":
                    if switch[0] == True:
                        count_result[2][0] += 1
                    switch[3] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[2] == True:
                        count_result[2][2] += 1
                    switch[1] = False
                else:
                    switch[1] = False
                    switch[3] = False
        if board[j][3] == "2":
            if x - i == 1 or (x - i < 12 and board[j] == board[j - 8]):
                if cardtype == "0" or cardtype == "4":
                    if switch[0] == True:
                        count_result[2][0] += 1
                    switch[2] = False
                elif cardtype == "2" or cardtype == "6":
                    if switch[0] == True:
                        count_result[2][0] += 1
                    if switch[3] == True:
                        count_result[2][3] += 1
                elif cardtype == "3" or cardtype == "7":
                    switch[2] = False
                    switch[1] = False
                else:
                    switch[1] = False
                    if switch[3] == True:
                        count_result[2][3] += 1
            elif board[j] == board[j + 8]:
                if cardtype == "0" or cardtype == "4":
                    if switch[2] == True:
                        count_result[2][2] += 1
                    switch[0] = False
                elif cardtype == "2" or cardtype == "6":
                    switch[3] = False
                    switch[0] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[1] == True:
                        count_result[2][1] += 1
                    if switch[2] == True:
                        count_result[2][2] += 1
                else:
                    if switch[1] == True:
                        count_result[2][1] += 1
                    switch[3] = False
        if board[j][3] == "3":
            if x - i == 1 or (x - i < 12 and board[j] == board[j - 8]):
                if cardtype == "0" or cardtype == "4":
                    if switch[2] == True:
                        count_result[2][2] += 1
                    switch[0] = False
                elif cardtype == "2" or cardtype == "6":
                    switch[0] = False
                    switch[3] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[1] == True:
                        count_result[2][1] += 1
                    if switch[2] == True:
                        count_result[2][2] += 1
                else:
                    if switch[1] == True:
                        count_result[2][1] += 1
                    switch[3] = False
            elif board[j] == board[j + 8]:
                if cardtype == "0" or cardtype == "4":
                    if switch[0] == True:
                        count_result[2][0] += 1
                    switch[2] = False
                elif cardtype == "2" or cardtype == "6":
                    if switch[0] == True:
                        count_result[2][0] += 1
                    if switch[3] == True:
                        count_result[2][3] += 1
                elif cardtype == "3" or cardtype == "7":
                    switch[2] = False
                    switch[1] = False
                else:
                    switch[1] = False
                    if switch[3] == True:
                        count_result[2][3] += 1

        if board[j][3] == "4":
            if y - i == 1 or (y - i < 8 and board[j] == board[j + 1]):
                if cardtype == "0" or cardtype == "4":
                    if switch[0] == True:
                        count_result[2][0] += 1
                    if switch[2] == True:
                        count_result[2][2] += 1
                elif cardtype == "2" or cardtype == "6":
                    if switch[0] == True:
                        count_result[2][0] += 1
                    switch[3] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[2] == True:
                        count_result[2][2] += 1
                    switch[1] = False
                else:
                    switch[1] = False
                    switch[3] = False
            elif y - i > 1 and board[j] == board[j - 1]:
                if cardtype == "0" or cardtype == "4":
                    switch[0] = False
                    switch[2] = False
                elif cardtype == "2" or cardtype == "6":
                    if switch[3] == True:
                        count_result[2][3] += 1
                    switch[0] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[1] == True:
                        count_result[2][1] += 1
                    switch[2] = False
                else:
                    if switch[1] == True:
                        count_result[2][1] += 1
                    if switch[3] == True:
                        count_result[2][3] += 1
        if board[j][3] == "5":
            if y - i == 1 or (y - i < 8 and board[j] == board[j + 1]):
                if cardtype == "0" or cardtype == "4":
                    switch[0] = False
                    switch[2] = False
                elif cardtype == "2" or cardtype == "6":
                    if switch[3] == True:
                        count_result[2][3] += 1
                    switch[0] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[1] == True:
                        count_result[2][1] += 1
                    switch[2] = False
                else:
                    if switch[1] == True:
                        count_result[2][1] += 1
                    if switch[3] == True:
                        count_result[2][3] += 1
            elif y - i > 1 and board[j] == board[j - 1]:
                if cardtype == "0" or cardtype == "4":
                    if switch[0] == True:
                        count_result[2][0] += 1
                    if switch[2] == True:
                        count_result[2][2] += 1
                elif cardtype == "2" or cardtype == "6":
                    if switch[0] == True:
                        count_result[2][0] += 1
                    switch[3] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[2] == True:
                        count_result[2][2] += 1
                    switch[1] = False
                else:
                    switch[1] = False
                    switch[3] = False
        if board[j][3] == "6":
            if y - i == 1 or (y - i < 8 and board[j] == board[j + 1]):
                if cardtype == "0" or cardtype == "4":
                    if switch[0] == True:
                        count_result[2][0] += 1
                    switch[2] = False
                elif cardtype == "2" or cardtype == "6":
                    if switch[0] == True:
                        count_result[2][0] += 1
                    if switch[3] == True:
                        count_result[2][3] += 1
                elif cardtype == "3" or cardtype == "7":
                    switch[2] = False
                    switch[1] = False
                else:
                    switch[1] = False
                    if switch[3] == True:
                        count_result[2][3] += 1
            elif y - i > 1 and board[j] == board[j - 1]:
                if cardtype == "0" or cardtype == "4":
                    if switch[2] == True:
                        count_result[2][2] += 1
                    switch[0] = False
                elif cardtype == "2" or cardtype == "6":
                    switch[3] = False
                    switch[0] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[1] == True:
                        count_result[2][1] += 1
                    if switch[2] == True:
                        count_result[2][2] += 1
                else:
                    if switch[1] == True:
                        count_result[2][1] += 1
                    switch[3] = False
        if board[j][3] == "7":
            if y - i == 1 or (y - i < 8 and board[j] == board[j + 1]):
                if cardtype == "0" or cardtype == "4":
                    if switch[2] == True:
                        count_result[2][2] += 1
                    switch[0] = False
                elif cardtype == "2" or cardtype == "6":
                    switch[0] = False
                    switch[3] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[1] == True:
                        count_result[2][1] += 1
                    if switch[2] == True:
                        count_result[2][2] += 1
                else:
                    if switch[1] == True:
                        count_result[2][1] += 1
                    switch[3] = False
            elif y - i > 1 and board[j] == board[j - 1]:
                if cardtype == "0" or cardtype == "4":
                    if switch[0] == True:
                        count_result[2][0] += 1
                    switch[2] = False
                elif cardtype == "2" or cardtype == "6":
                    if switch[0] == True:
                        count_result[2][0] += 1
                    if switch[3] == True:
                        count_result[2][3] += 1
                elif cardtype == "3" or cardtype == "7":
                    switch[2] = False
                    switch[1] = False
                else:
                    switch[1] = False
                    if switch[3] == True:
                        count_result[2][3] += 1

    switch=[True,True,True,True]
    for i in range(1,4,1):
        if y+i>8 or x+i>12:
            break
        ax=12-(x+i)
        ay=(y+i)-1
        j=ax*8+ay
        if board[j][1:3]=="00":
            break
        ax=12-startx
        ay=starty-1
        sj=ax*8+ay

        if board[j][3] == "0":
            if x + i == 1 or (x + i < 12 and board[j] == board[j - 8]):
                if cardtype == "0" or cardtype == "4":
                    if switch[0] == True:
                        count_result[2][0] += 1
                    if switch[2] == True:
                        count_result[2][2] += 1
                elif cardtype == "2" or cardtype == "6":
                    if switch[0] == True:
                        count_result[2][0] += 1
                    switch[3] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[2] == True:
                        count_result[2][2] += 1
                    switch[1] = False
                else:
                    switch[1] = False
                    switch[3] = False
            elif board[j] == board[j + 8]:
                if cardtype == "0" or cardtype == "4":
                    switch[0] = False
                    switch[2] = False
                elif cardtype == "2" or cardtype == "6":
                    if switch[3] == True:
                        count_result[2][3] += 1
                    switch[0] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[1] == True:
                        count_result[2][1] += 1
                    switch[2] = False
                else:
                    if switch[1] == True:
                        count_result[2][1] += 1
                    if switch[3] == True:
                        count_result[2][3] += 1

        if board[j][3] == "1":
            if x + i == 1 or (x + i < 12 and board[j] == board[j - 8]):
                if cardtype == "0" or cardtype == "4":
                    switch[0] = False
                    switch[2] = False
                elif cardtype == "2" or cardtype == "6":
                    if switch[3] == True:
                        count_result[2][3] += 1
                    switch[0] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[1] == True:
                        count_result[2][1] += 1
                    switch[2] = False
                else:
                    if switch[1] == True:
                        count_result[2][1] += 1
                    if switch[3] == True:
                        count_result[2][3] += 1
            elif board[j] == board[j + 8]:
                if cardtype == "0" or cardtype == "4":
                    if switch[0] == True:
                        count_result[2][0] += 1
                    if switch[2] == True:
                        count_result[2][2] += 1
                elif cardtype == "2" or cardtype == "6":
                    if switch[0] == True:
                        count_result[2][0] += 1
                    switch[3] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[2] == True:
                        count_result[2][2] += 1
                    switch[1] = False
                else:
                    switch[1] = False
                    switch[3] = False
        if board[j][3] == "2":
            if x + i == 1 or (x + i < 12 and board[j] == board[j - 8]):
                if cardtype == "0" or cardtype == "4":
                    if switch[0] == True:
                        count_result[2][0] += 1
                    switch[2] = False
                elif cardtype == "2" or cardtype == "6":
                    if switch[0] == True:
                        count_result[2][0] += 1
                    if switch[3] == True:
                        count_result[2][3] += 1
                elif cardtype == "3" or cardtype == "7":
                    switch[2] = False
                    switch[1] = False
                else:
                    switch[1] = False
                    if switch[3] == True:
                        count_result[2][3] += 1
            elif board[j] == board[j + 8]:
                if cardtype == "0" or cardtype == "4":
                    if switch[2] == True:
                        count_result[2][2] += 1
                    switch[0] = False
                elif cardtype == "2" or cardtype == "6":
                    switch[3] = False
                    switch[0] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[1] == True:
                        count_result[2][1] += 1
                    if switch[2] == True:
                        count_result[2][2] += 1
                else:
                    if switch[1] == True:
                        count_result[2][1] += 1
                    switch[3] = False
        if board[j][3] == "3":
            if x + i == 1 or (x + i < 12 and board[j] == board[j - 8]):
                if cardtype == "0" or cardtype == "4":
                    if switch[2] == True:
                        count_result[2][2] += 1
                    switch[0] = False
                elif cardtype == "2" or cardtype == "6":
                    switch[0] = False
                    switch[3] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[1] == True:
                        count_result[2][1] += 1
                    if switch[2] == True:
                        count_result[2][2] += 1
                else:
                    if switch[1] == True:
                        count_result[2][1] += 1
                    switch[3] = False
            elif board[j] == board[j + 8]:
                if cardtype == "0" or cardtype == "4":
                    if switch[0] == True:
                        count_result[2][0] += 1
                    switch[2] = False
                elif cardtype == "2" or cardtype == "6":
                    if switch[0] == True:
                        count_result[2][0] += 1
                    if switch[3] == True:
                        count_result[2][3] += 1
                elif cardtype == "3" or cardtype == "7":
                    switch[2] = False
                    switch[1] = False
                else:
                    switch[1] = False
                    if switch[3] == True:
                        count_result[2][3] += 1

        if board[j][3] == "4":
            if y + i == 1 or (y + i < 8 and board[j] == board[j + 1]):
                if cardtype == "0" or cardtype == "4":
                    if switch[0] == True:
                        count_result[2][0] += 1
                    if switch[2] == True:
                        count_result[2][2] += 1
                elif cardtype == "2" or cardtype == "6":
                    if switch[0] == True:
                        count_result[2][0] += 1
                    switch[3] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[2] == True:
                        count_result[2][2] += 1
                    switch[1] = False
                else:
                    switch[1] = False
                    switch[3] = False
            elif y + i > 1 and board[j] == board[j - 1]:
                if cardtype == "0" or cardtype == "4":
                    switch[0] = False
                    switch[2] = False
                elif cardtype == "2" or cardtype == "6":
                    if switch[3] == True:
                        count_result[2][3] += 1
                    switch[0] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[1] == True:
                        count_result[2][1] += 1
                    switch[2] = False
                else:
                    if switch[1] == True:
                        count_result[2][1] += 1
                    if switch[3] == True:
                        count_result[2][3] += 1
        if board[j][3] == "5":
            if y + i == 1 or (y + i < 8 and board[j] == board[j + 1]):
                if cardtype == "0" or cardtype == "4":
                    switch[0] = False
                    switch[2] = False
                elif cardtype == "2" or cardtype == "6":
                    if switch[3] == True:
                        count_result[2][3] += 1
                    switch[0] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[1] == True:
                        count_result[2][1] += 1
                    switch[2] = False
                else:
                    if switch[1] == True:
                        count_result[2][1] += 1
                    if switch[3] == True:
                        count_result[2][3] += 1
            elif y + i > 1 and board[j] == board[j - 1]:
                if cardtype == "0" or cardtype == "4":
                    if switch[0] == True:
                        count_result[2][0] += 1
                    if switch[2] == True:
                        count_result[2][2] += 1
                elif cardtype == "2" or cardtype == "6":
                    if switch[0] == True:
                        count_result[2][0] += 1
                    switch[3] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[2] == True:
                        count_result[2][2] += 1
                    switch[1] = False
                else:
                    switch[1] = False
                    switch[3] = False
        if board[j][3] == "6":
            if y + i == 1 or (y + i < 8 and board[j] == board[j + 1]):
                if cardtype == "0" or cardtype == "4":
                    if switch[0] == True:
                        count_result[2][0] += 1
                    switch[2] = False
                elif cardtype == "2" or cardtype == "6":
                    if switch[0] == True:
                        count_result[2][0] += 1
                    if switch[3] == True:
                        count_result[2][3] += 1
                elif cardtype == "3" or cardtype == "7":
                    switch[2] = False
                    switch[1] = False
                else:
                    switch[1] = False
                    if switch[3] == True:
                        count_result[2][3] += 1
            elif y + i > 1 and board[j] == board[j - 1]:
                if cardtype == "0" or cardtype == "4":
                    if switch[2] == True:
                        count_result[2][2] += 1
                    switch[0] = False
                elif cardtype == "2" or cardtype == "6":
                    switch[3] = False
                    switch[0] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[1] == True:
                        count_result[2][1] += 1
                    if switch[2] == True:
                        count_result[2][2] += 1
                else:
                    if switch[1] == True:
                        count_result[2][1] += 1
                    switch[3] = False
        if board[j][3] == "7":
            if y + i == 1 or (y + i < 8 and board[j] == board[j + 1]):
                if cardtype == "0" or cardtype == "4":
                    if switch[2] == True:
                        count_result[2][2] += 1
                    switch[0] = False
                elif cardtype == "2" or cardtype == "6":
                    switch[0] = False
                    switch[3] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[1] == True:
                        count_result[2][1] += 1
                    if switch[2] == True:
                        count_result[2][2] += 1
                else:
                    if switch[1] == True:
                        count_result[2][1] += 1
                    switch[3] = False
            elif y + i > 1 and board[j] == board[j - 1]:
                if cardtype == "0" or cardtype == "4":
                    if switch[0] == True:
                        count_result[2][0] += 1
                    switch[2] = False
                elif cardtype == "2" or cardtype == "6":
                    if switch[0] == True:
                        count_result[2][0] += 1
                    if switch[3] == True:
                        count_result[2][3] += 1
                elif cardtype == "3" or cardtype == "7":
                    switch[2] = False
                    switch[1] = False
                else:
                    switch[1] = False
                    if switch[3] == True:
                        count_result[2][3] += 1

    switch=[True,True,True,True]
    for i in range(1,4,1):
        if y-i<1 or x+i>12:
            break
        ax=12-(x+i)
        ay=(y-i)-1
        j=ax*8+ay
        if board[j][1:3]=="00":
            break
        ax=12-startx
        ay=starty-1
        sj=ax*8+ay

        if board[j][3] == "0":
            if x + i == 1 or (x + i < 12 and board[j] == board[j - 8]):
                if cardtype == "0" or cardtype == "4":
                    if switch[0] == True:
                        count_result[3][0] += 1
                    if switch[2] == True:
                        count_result[3][2] += 1
                elif cardtype == "2" or cardtype == "6":
                    if switch[0] == True:
                        count_result[3][0] += 1
                    switch[3] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[2] == True:
                        count_result[3][2] += 1
                    switch[1] = False
                else:
                    switch[1] = False
                    switch[3] = False
            elif board[j] == board[j + 8]:
                if cardtype == "0" or cardtype == "4":
                    switch[0] = False
                    switch[2] = False
                elif cardtype == "2" or cardtype == "6":
                    if switch[3] == True:
                        count_result[3][3] += 1
                    switch[0] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[1] == True:
                        count_result[3][1] += 1
                    switch[2] = False
                else:
                    if switch[1] == True:
                        count_result[3][1] += 1
                    if switch[3] == True:
                        count_result[3][3] += 1

        if board[j][3] == "1":
            if x + i == 1 or (x + i < 12 and board[j] == board[j - 8]):
                if cardtype == "0" or cardtype == "4":
                    switch[0] = False
                    switch[2] = False
                elif cardtype == "2" or cardtype == "6":
                    if switch[3] == True:
                        count_result[3][3] += 1
                    switch[0] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[1] == True:
                        count_result[3][1] += 1
                    switch[2] = False
                else:
                    if switch[1] == True:
                        count_result[3][1] += 1
                    if switch[3] == True:
                        count_result[3][3] += 1
            elif board[j] == board[j + 8]:
                if cardtype == "0" or cardtype == "4":
                    if switch[0] == True:
                        count_result[3][0] += 1
                    if switch[2] == True:
                        count_result[3][2] += 1
                elif cardtype == "2" or cardtype == "6":
                    if switch[0] == True:
                        count_result[3][0] += 1
                    switch[3] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[2] == True:
                        count_result[3][2] += 1
                    switch[1] = False
                else:
                    switch[1] = False
                    switch[3] = False
        if board[j][3] == "2":
            if x + i == 1 or (x + i < 12 and board[j] == board[j - 8]):
                if cardtype == "0" or cardtype == "4":
                    if switch[0] == True:
                        count_result[3][0] += 1
                    switch[2] = False
                elif cardtype == "2" or cardtype == "6":
                    if switch[0] == True:
                        count_result[3][0] += 1
                    if switch[3] == True:
                        count_result[3][3] += 1
                elif cardtype == "3" or cardtype == "7":
                    switch[2] = False
                    switch[1] = False
                else:
                    switch[1] = False
                    if switch[3] == True:
                        count_result[3][3] += 1
            elif board[j] == board[j + 8]:
                if cardtype == "0" or cardtype == "4":
                    if switch[2] == True:
                        count_result[3][2] += 1
                    switch[0] = False
                elif cardtype == "2" or cardtype == "6":
                    switch[3] = False
                    switch[0] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[1] == True:
                        count_result[3][1] += 1
                    if switch[2] == True:
                        count_result[3][2] += 1
                else:
                    if switch[1] == True:
                        count_result[3][1] += 1
                    switch[3] = False
        if board[j][3] == "3":
            if x + i == 1 or (x + i < 12 and board[j] == board[j - 8]):
                if cardtype == "0" or cardtype == "4":
                    if switch[2] == True:
                        count_result[3][2] += 1
                    switch[0] = False
                elif cardtype == "2" or cardtype == "6":
                    switch[0] = False
                    switch[3] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[1] == True:
                        count_result[3][1] += 1
                    if switch[2] == True:
                        count_result[3][2] += 1
                else:
                    if switch[1] == True:
                        count_result[3][1] += 1
                    switch[3] = False
            elif board[j] == board[j + 8]:
                if cardtype == "0" or cardtype == "4":
                    if switch[0] == True:
                        count_result[3][0] += 1
                    switch[2] = False
                elif cardtype == "2" or cardtype == "6":
                    if switch[0] == True:
                        count_result[3][0] += 1
                    if switch[3] == True:
                        count_result[3][3] += 1
                elif cardtype == "3" or cardtype == "7":
                    switch[2] = False
                    switch[1] = False
                else:
                    switch[1] = False
                    if switch[3] == True:
                        count_result[3][3] += 1

        if board[j][3] == "4":
            if y - i == 1 or (y - i < 8 and board[j] == board[j + 1]):
                if cardtype == "0" or cardtype == "4":
                    if switch[0] == True:
                        count_result[3][0] += 1
                    if switch[2] == True:
                        count_result[3][2] += 1
                elif cardtype == "2" or cardtype == "6":
                    if switch[0] == True:
                        count_result[3][0] += 1
                    switch[3] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[2] == True:
                        count_result[3][2] += 1
                    switch[1] = False
                else:
                    switch[1] = False
                    switch[3] = False
            elif y - i > 1 and board[j] == board[j - 1]:
                if cardtype == "0" or cardtype == "4":
                    switch[0] = False
                    switch[2] = False
                elif cardtype == "2" or cardtype == "6":
                    if switch[3] == True:
                        count_result[3][3] += 1
                    switch[0] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[1] == True:
                        count_result[3][1] += 1
                    switch[2] = False
                else:
                    if switch[1] == True:
                        count_result[3][1] += 1
                    if switch[3] == True:
                        count_result[3][3] += 1
        if board[j][3] == "5":
            if y - i == 1 or (y - i < 8 and board[j] == board[j + 1]):
                if cardtype == "0" or cardtype == "4":
                    switch[0] = False
                    switch[2] = False
                elif cardtype == "2" or cardtype == "6":
                    if switch[3] == True:
                        count_result[3][3] += 1
                    switch[0] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[1] == True:
                        count_result[3][1] += 1
                    switch[2] = False
                else:
                    if switch[1] == True:
                        count_result[3][1] += 1
                    if switch[3] == True:
                        count_result[3][3] += 1
            elif y - i > 1 and board[j] == board[j - 1]:
                if cardtype == "0" or cardtype == "4":
                    if switch[0] == True:
                        count_result[3][0] += 1
                    if switch[2] == True:
                        count_result[3][2] += 1
                elif cardtype == "2" or cardtype == "6":
                    if switch[0] == True:
                        count_result[3][0] += 1
                    switch[3] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[2] == True:
                        count_result[3][2] += 1
                    switch[1] = False
                else:
                    switch[1] = False
                    switch[3] = False
        if board[j][3] == "6":
            if y - i == 1 or (y - i < 8 and board[j] == board[j + 1]):
                if cardtype == "0" or cardtype == "4":
                    if switch[0] == True:
                        count_result[3][0] += 1
                    switch[2] = False
                elif cardtype == "2" or cardtype == "6":
                    if switch[0] == True:
                        count_result[3][0] += 1
                    if switch[3] == True:
                        count_result[3][3] += 1
                elif cardtype == "3" or cardtype == "7":
                    switch[2] = False
                    switch[1] = False
                else:
                    switch[1] = False
                    if switch[3] == True:
                        count_result[3][3] += 1
            elif y - i > 1 and board[j] == board[j - 1]:
                if cardtype == "0" or cardtype == "4":
                    if switch[2] == True:
                        count_result[3][2] += 1
                    switch[0] = False
                elif cardtype == "2" or cardtype == "6":
                    switch[3] = False
                    switch[0] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[1] == True:
                        count_result[3][1] += 1
                    if switch[2] == True:
                        count_result[3][2] += 1
                else:
                    if switch[1] == True:
                        count_result[3][1] += 1
                    switch[3] = False
        if board[j][3] == "7":
            if y - i == 1 or (y - i < 8 and board[j] == board[j + 1]):
                if cardtype == "0" or cardtype == "4":
                    if switch[2] == True:
                        count_result[3][2] += 1
                    switch[0] = False
                elif cardtype == "2" or cardtype == "6":
                    switch[0] = False
                    switch[3] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[1] == True:
                        count_result[3][1] += 1
                    if switch[2] == True:
                        count_result[3][2] += 1
                else:
                    if switch[1] == True:
                        count_result[3][1] += 1
                    switch[3] = False
            elif y - i > 1 and board[j] == board[j - 1]:
                if cardtype == "0" or cardtype == "4":
                    if switch[0] == True:
                        count_result[3][0] += 1
                    switch[2] = False
                elif cardtype == "2" or cardtype == "6":
                    if switch[0] == True:
                        count_result[3][0] += 1
                    if switch[3] == True:
                        count_result[3][3] += 1
                elif cardtype == "3" or cardtype == "7":
                    switch[2] = False
                    switch[1] = False
                else:
                    switch[1] = False
                    if switch[3] == True:
                        count_result[3][3] += 1

    switch=[True,True,True,True]
    for i in range(1,4,1):
        if y+i>8 or x-i<1:
            break
        ax=12-(x-i)
        ay=(y+i)-1
        j=ax*8+ay
        if board[j][1:3]=="00":
            break
        ax=12-startx
        ay=starty-1
        sj=ax*8+ay

        if board[j][3] == "0":
            if x - i == 1 or (x - i < 12 and board[j] == board[j - 8]):
                if cardtype == "0" or cardtype == "4":
                    if switch[0] == True:
                        count_result[3][0] += 1
                    if switch[2] == True:
                        count_result[3][2] += 1
                elif cardtype == "2" or cardtype == "6":
                    if switch[0] == True:
                        count_result[3][0] += 1
                    switch[3] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[2] == True:
                        count_result[3][2] += 1
                    switch[1] = False
                else:
                    switch[1] = False
                    switch[3] = False
            elif board[j] == board[j + 8]:
                if cardtype == "0" or cardtype == "4":
                    switch[0] = False
                    switch[2] = False
                elif cardtype == "2" or cardtype == "6":
                    if switch[3] == True:
                        count_result[3][3] += 1
                    switch[0] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[1] == True:
                        count_result[3][1] += 1
                    switch[2] = False
                else:
                    if switch[1] == True:
                        count_result[3][1] += 1
                    if switch[3] == True:
                        count_result[3][3] += 1

        if board[j][3] == "1":
            if x - i == 1 or (x - i < 12 and board[j] == board[j - 8]):
                if cardtype == "0" or cardtype == "4":
                    switch[0] = False
                    switch[2] = False
                elif cardtype == "2" or cardtype == "6":
                    if switch[3] == True:
                        count_result[3][3] += 1
                    switch[0] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[1] == True:
                        count_result[3][1] += 1
                    switch[2] = False
                else:
                    if switch[1] == True:
                        count_result[3][1] += 1
                    if switch[3] == True:
                        count_result[3][3] += 1
            elif board[j] == board[j + 8]:
                if cardtype == "0" or cardtype == "4":
                    if switch[0] == True:
                        count_result[3][0] += 1
                    if switch[2] == True:
                        count_result[3][2] += 1
                elif cardtype == "2" or cardtype == "6":
                    if switch[0] == True:
                        count_result[3][0] += 1
                    switch[3] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[2] == True:
                        count_result[3][2] += 1
                    switch[1] = False
                else:
                    switch[1] = False
                    switch[3] = False
        if board[j][3] == "2":
            if x - i == 1 or (x - i < 12 and board[j] == board[j - 8]):
                if cardtype == "0" or cardtype == "4":
                    if switch[0] == True:
                        count_result[3][0] += 1
                    switch[2] = False
                elif cardtype == "2" or cardtype == "6":
                    if switch[0] == True:
                        count_result[3][0] += 1
                    if switch[3] == True:
                        count_result[3][3] += 1
                elif cardtype == "3" or cardtype == "7":
                    switch[2] = False
                    switch[1] = False
                else:
                    switch[1] = False
                    if switch[3] == True:
                        count_result[3][3] += 1
            elif board[j] == board[j + 8]:
                if cardtype == "0" or cardtype == "4":
                    if switch[2] == True:
                        count_result[3][2] += 1
                    switch[0] = False
                elif cardtype == "2" or cardtype == "6":
                    switch[3] = False
                    switch[0] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[1] == True:
                        count_result[3][1] += 1
                    if switch[2] == True:
                        count_result[3][2] += 1
                else:
                    if switch[1] == True:
                        count_result[3][1] += 1
                    switch[3] = False
        if board[j][3] == "3":
            if x - i == 1 or (x - i < 12 and board[j] == board[j - 8]):
                if cardtype == "0" or cardtype == "4":
                    if switch[2] == True:
                        count_result[3][2] += 1
                    switch[0] = False
                elif cardtype == "2" or cardtype == "6":
                    switch[0] = False
                    switch[3] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[1] == True:
                        count_result[3][1] += 1
                    if switch[2] == True:
                        count_result[3][2] += 1
                else:
                    if switch[1] == True:
                        count_result[3][1] += 1
                    switch[3] = False
            elif board[j] == board[j + 8]:
                if cardtype == "0" or cardtype == "4":
                    if switch[0] == True:
                        count_result[3][0] += 1
                    switch[2] = False
                elif cardtype == "2" or cardtype == "6":
                    if switch[0] == True:
                        count_result[3][0] += 1
                    if switch[3] == True:
                        count_result[3][3] += 1
                elif cardtype == "3" or cardtype == "7":
                    switch[2] = False
                    switch[1] = False
                else:
                    switch[1] = False
                    if switch[3] == True:
                        count_result[3][3] += 1

        if board[j][3] == "4":
            if y + i == 1 or (y + i < 8 and board[j] == board[j + 1]):
                if cardtype == "0" or cardtype == "4":
                    if switch[0] == True:
                        count_result[3][0] += 1
                    if switch[2] == True:
                        count_result[3][2] += 1
                elif cardtype == "2" or cardtype == "6":
                    if switch[0] == True:
                        count_result[3][0] += 1
                    switch[3] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[2] == True:
                        count_result[3][2] += 1
                    switch[1] = False
                else:
                    switch[1] = False
                    switch[3] = False
            elif y + i > 1 and board[j] == board[j - 1]:
                if cardtype == "0" or cardtype == "4":
                    switch[0] = False
                    switch[2] = False
                elif cardtype == "2" or cardtype == "6":
                    if switch[3] == True:
                        count_result[3][3] += 1
                    switch[0] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[1] == True:
                        count_result[3][1] += 1
                    switch[2] = False
                else:
                    if switch[1] == True:
                        count_result[3][1] += 1
                    if switch[3] == True:
                        count_result[3][3] += 1
        if board[j][3] == "5":
            if y + i == 1 or (y + i < 8 and board[j] == board[j + 1]):
                if cardtype == "0" or cardtype == "4":
                    switch[0] = False
                    switch[2] = False
                elif cardtype == "2" or cardtype == "6":
                    if switch[3] == True:
                        count_result[3][3] += 1
                    switch[0] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[1] == True:
                        count_result[3][1] += 1
                    switch[2] = False
                else:
                    if switch[1] == True:
                        count_result[3][1] += 1
                    if switch[3] == True:
                        count_result[3][3] += 1
            elif y + i > 1 and board[j] == board[j - 1]:
                if cardtype == "0" or cardtype == "4":
                    if switch[0] == True:
                        count_result[3][0] += 1
                    if switch[2] == True:
                        count_result[3][2] += 1
                elif cardtype == "2" or cardtype == "6":
                    if switch[0] == True:
                        count_result[3][0] += 1
                    switch[3] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[2] == True:
                        count_result[3][2] += 1
                    switch[1] = False
                else:
                    switch[1] = False
                    switch[3] = False
        if board[j][3] == "6":
            if y + i == 1 or (y + i < 8 and board[j] == board[j + 1]):
                if cardtype == "0" or cardtype == "4":
                    if switch[0] == True:
                        count_result[3][0] += 1
                    switch[2] = False
                elif cardtype == "2" or cardtype == "6":
                    if switch[0] == True:
                        count_result[3][0] += 1
                    if switch[3] == True:
                        count_result[3][3] += 1
                elif cardtype == "3" or cardtype == "7":
                    switch[2] = False
                    switch[1] = False
                else:
                    switch[1] = False
                    if switch[3] == True:
                        count_result[3][3] += 1
            elif y + i > 1 and board[j] == board[j - 1]:
                if cardtype == "0" or cardtype == "4":
                    if switch[2] == True:
                        count_result[3][2] += 1
                    switch[0] = False
                elif cardtype == "2" or cardtype == "6":
                    switch[3] = False
                    switch[0] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[1] == True:
                        count_result[3][1] += 1
                    if switch[2] == True:
                        count_result[3][2] += 1
                else:
                    if switch[1] == True:
                        count_result[3][1] += 1
                    switch[3] = False
        if board[j][3] == "7":
            if y + i == 1 or (y + i < 8 and board[j] == board[j + 1]):
                if cardtype == "0" or cardtype == "4":
                    if switch[2] == True:
                        count_result[3][2] += 1
                    switch[0] = False
                elif cardtype == "2" or cardtype == "6":
                    switch[0] = False
                    switch[3] = False
                elif cardtype == "3" or cardtype == "7":
                    if switch[1] == True:
                        count_result[3][1] += 1
                    if switch[2] == True:
                        count_result[3][2] += 1
                else:
                    if switch[1] == True:
                        count_result[3][1] += 1
                    switch[3] = False
            elif y + i > 1 and board[j] == board[j - 1]:
                if cardtype == "0" or cardtype == "4":
                    if switch[0] == True:
                        count_result[3][0] += 1
                    switch[2] = False
                elif cardtype == "2" or cardtype == "6":
                    if switch[0] == True:
                        count_result[3][0] += 1
                    if switch[3] == True:
                        count_result[3][3] += 1
                elif cardtype == "3" or cardtype == "7":
                    switch[2] = False
                    switch[1] = False
                else:
                    switch[1] = False
                    if switch[3] == True:
                        count_result[3][3] += 1
    # print(count_result)
    return count_result

def AI_check_winning(x,y,cardtype,board):
    global game_finished
    ax=12-x
    ay=y-1
    j=ax*8+ay
    # 读哪种卡片 总共八种 0-7
    # cardtype=ct
    # 把上一步的数据带进来
    result=AI_check_winning_result(x,y,str(cardtype),board)
    # if board[j][0]=="A":
    if current_player == "A":
        # 判a玩的是啥， false是颜色
        if playerA_Select==False:
            for i in result:
                if i[2]>=4 or i[3]>=4:
                    # game_finished=True
                    # bottomlable.config(text="Player A Wins.")
                    return "A"
            # 先判断A玩的所有方向 之后才能判断B
            for i in result:
                if i[0]>=4 or i[1]>=4:
                    # game_finished=True
                    # bottomlable.config(text="Player B Wins.")
                    return "B"
        # 判断A 玩的是点的情况
        else:
            for i in result:
                if i[0]>=4 or i[1]>=4:
                    # game_finished=True
                    # bottomlable.config(text="Player A Wins.")
                    return "A"
            for i in result:
                if i[2]>=4 or i[3]>=4:
                    # game_finished=True
                    # bottomlable.config(text="Player B Wins.")
                    return "B"
    # 现在是B下的情况
    else:
        if playerA_Select==False:
            for i in result:
                if i[0]>=4 or i[1]>=4:
                    # game_finished=True
                    # bottomlable.config(text="Player B Wins.")
                    return "B"
            for i in result:
                if i[2]>=4 or i[3]>=4:
                    # game_finished=True
                    # bottomlable.config(text="Player A Wins.")
                    return "A"
        else:
            for i in result:
                if i[2]>=4 or i[3]>=4:
                    # game_finished=True
                    # bottomlable.config(text="Player B Wins.")
                    return "B"
            for i in result:
                if i[0]>=4 or i[1]>=4:
                    # game_finished=True
                    # bottomlable.config(text="Player A Wins.")
                    return "A"
    # 统计前四种卡片上面的数值
    print("cardtype")
    print(type(cardtype))
    if cardtype==0 or cardtype==1 or cardtype==2 or cardtype==3:
        result=AI_check_winning_result(x+1,y,str(cardtype),board)
    # 统计右边的
    elif cardtype==4 or cardtype==5 or cardtype==6 or cardtype==7:
        result=AI_check_winning_result(x,y+1,str(cardtype),board)
    # if board[j][0]=="A":
    if current_player == "A":
        if playerA_Select==False:
            for i in result:
                if i[2]>=4 or i[3]>=4:
                    # game_finished=True
                    # bottomlable.config(text="Player A Wins.")
                    return "A"
            for i in result:
                if i[0]>=4 or i[1]>=4:
                    # game_finished=True
                    # bottomlable.config(text="Player B Wins.")
                    return "B"
        else:
            for i in result:
                if i[0]>=4 or i[1]>=4:
                    # game_finished=True
                    # bottomlable.config(text="Player A Wins.")
                    return "A"
            for i in result:
                if i[2]>=4 or i[3]>=4:
                    # game_finished=True
                    # bottomlable.config(text="Player B Wins.")
                    return "B"
    else:
        if playerA_Select==False:
            for i in result:
                if i[0]>=4 or i[1]>=4:
                    # game_finished=True
                    # bottomlable.config(text="Player B Wins.")
                    return "B"
            for i in result:
                if i[2]>=4 or i[3]>=4:
                    # game_finished=True
                    # bottomlable.config(text="Player A Wins.")
                    return "A"
        else:
            for i in result:
                if i[2]>=4 or i[3]>=4:
                    # game_finished=True
                    # bottomlable.config(text="Player B Wins.")
                    return "B"
            for i in result:
                if i[0]>=4 or i[1]>=4:
                    # game_finished=True
                    # bottomlable.config(text="Player A Wins.")
                    return "A"
    return
    '''
# 根据上面的数据，计算谁赢了
def check_winning(x,y):
    global game_finished
    ax=12-x
    ay=y-1
    j=ax*8+ay
    # 读哪种卡片 总共八种 0-7
    cardtype=int(board[j][3])
    # 把上一步的数据带进来
    result=check_winning_result(x,y)
    if board[j][0]=="A":
        # 判a玩的是啥， false是颜色
        if playerA_Select==False:
            for i in result:
                if i[2]>=4 or i[3]>=4:
                    game_finished=True
                    bottomlable.config(text="Player A Wins.")
                    return "A"
            # 先判断A玩的所有方向 之后才能判断B
            for i in result:
                if i[0]>=4 or i[1]>=4:
                    game_finished=True
                    bottomlable.config(text="Player B Wins.")
                    return "B"
        # 判断A 玩的是点的情况
        else:
            for i in result:
                if i[0]>=4 or i[1]>=4:
                    game_finished=True
                    bottomlable.config(text="Player A Wins.")
                    return "A"
            for i in result:
                if i[2]>=4 or i[3]>=4:
                    game_finished=True
                    bottomlable.config(text="Player B Wins.")
                    return "B"
    # 现在是B下的情况
    else:
        if playerA_Select==False:
            for i in result:
                if i[0]>=4 or i[1]>=4:
                    game_finished=True
                    bottomlable.config(text="Player B Wins.")
                    return "B"
            for i in result:
                if i[2]>=4 or i[3]>=4:
                    game_finished=True
                    bottomlable.config(text="Player A Wins.")
                    return "A"
        else:
            for i in result:
                if i[2]>=4 or i[3]>=4:
                    game_finished=True
                    bottomlable.config(text="Player B Wins.")
                    return "B"
            for i in result:
                if i[0]>=4 or i[1]>=4:
                    game_finished=True
                    bottomlable.config(text="Player A Wins.")
                    return "A"
    # 统计前四种卡片上面的数值
    if cardtype==0 or cardtype==1 or cardtype==2 or cardtype==3:
        result=check_winning_result(x+1,y)
    # 统计右边的
    elif cardtype==4 or cardtype==5 or cardtype==6 or cardtype==7:
        result=check_winning_result(x,y+1)
    if board[j][0]=="A":
        if playerA_Select==False:
            for i in result:
                if i[2]>=4 or i[3]>=4:
                    game_finished=True
                    bottomlable.config(text="Player A Wins.")
                    return "A"
            for i in result:
                if i[0]>=4 or i[1]>=4:
                    game_finished=True
                    bottomlable.config(text="Player B Wins.")
                    return "B"
        else:
            for i in result:
                if i[0]>=4 or i[1]>=4:
                    game_finished=True
                    bottomlable.config(text="Player A Wins.")
                    return "A"
            for i in result:
                if i[2]>=4 or i[3]>=4:
                    game_finished=True
                    bottomlable.config(text="Player B Wins.")
                    return "B"
    else:
        if playerA_Select==False:
            for i in result:
                if i[0]>=4 or i[1]>=4:
                    game_finished=True
                    bottomlable.config(text="Player B Wins.")
                    return "B"
            for i in result:
                if i[2]>=4 or i[3]>=4:
                    game_finished=True
                    bottomlable.config(text="Player A Wins.")
                    return "A"
        else:
            for i in result:
                if i[2]>=4 or i[3]>=4:
                    game_finished=True
                    bottomlable.config(text="Player B Wins.")
                    return "B"
            for i in result:
                if i[0]>=4 or i[1]>=4:
                    game_finished=True
                    bottomlable.config(text="Player A Wins.")
                    return "A"

def cgetpoint(str,cont,isplacepoint):
    if str[3]=="0" or str[3]=="4":
        if cont=="text":
            if isplacepoint:
                return "●"
            else:
                return "○"
        elif cont=="bg":
            if isplacepoint:
                return "red"
            else:
                return "white"
    elif str[3]=="1" or str[3]=="5":
        if cont=="text":
            if isplacepoint:
                return "○"
            else:
                return "●"
        elif cont=="bg":
            if isplacepoint:
                return "white"
            else:
                return "red"
    elif str[3]=="2" or str[3]=="6":
        if cont=="text":
            if isplacepoint:
                return "●"
            else:
                return "○"
        elif cont=="bg":
            if isplacepoint:
                return "white"
            else:
                return "red"
    elif str[3]=="3" or str[3]=="7":
        if cont=="text":
            if isplacepoint:
                return "○"
            else:
                return "●"
        elif cont=="bg":
            if isplacepoint:
                return "red"
            else:
                return "white"

def cget(curs,cont,tmp_board):
    save=tmp_board[curs]
    if save=="X000":
        return
    if curs-8>0:
        if save==tmp_board[curs-8]:
            return cgetpoint(save,cont,True)
    if curs+8<12*8:
        if save==tmp_board[curs+8]:
            return cgetpoint(save,cont,False)
    if curs-1>0:
        if save==tmp_board[curs-1]:
            return cgetpoint(save,cont,False)
    if curs+1<12*8:
        if save==tmp_board[curs+1]:
            return cgetpoint(save,cont,True)


def AI_check_winning_result(x,y,tmp_board):
    count_result=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]  #黑点,白点,红底,白底 顺序是 竖 横 左下又上 右下左上
    switch=[True,True,True,True] #初始化四个true，然后只要不一样就变false了，有false了后面就不会再记数了
    # switch的true false表还有count result合起来算赢没赢，单纯计数没用，中间穿插别的但是还计数，输出结果就是错的

    # startx y是计下的地方，和相关的，然后进行比较
    startx=x
    starty=y

    # 换坐标
    ax=12-x
    ay=y-1

    # j把ax ay换成label的下标
    j=ax*8+ay
    if cget(j,"text",tmp_board)=="●":
        count_result[0][0]+=1
        count_result[1][0]+=1
        count_result[2][0]+=1
        count_result[3][0]+=1
    elif cget(j,"text",tmp_board)=="○":
        count_result[0][1]+=1
        count_result[1][1]+=1
        count_result[2][1]+=1
        count_result[3][1]+=1
    if cget(j,"bg",tmp_board)=="red":
        count_result[0][2]+=1
        count_result[1][2]+=1
        count_result[2][2]+=1
        count_result[3][2]+=1
    elif cget(j,"bg",tmp_board)=="white":
        count_result[0][3]+=1
        count_result[1][3]+=1
        count_result[2][3]+=1
        count_result[3][3]+=1
    #开始计数了
    for i in range(1,4,1):
        if x+i>12:
            break
        ax=12-(x+i)
        ay=y-1
        j=ax*8+ay
        if tmp_board[j][1:3]=="00":
            break
        ax=12-startx
        ay=starty-1
        sj=ax*8+ay
        # j是扫描的点，sj是原始的点 start j
        if cget(j,"text",tmp_board)==cget(sj,"text",tmp_board):
            if cget(j,"text",tmp_board)=="●":
                if switch[0]==True:
                    count_result[0][0]+=1
            elif cget(j,"text",tmp_board)=="○":
                if switch[1]==True:
                    count_result[0][1]+=1
        else:
            if cget(j,"text",tmp_board)=="●":
                switch[1]=False
            elif cget(j,"text",tmp_board)=="○":
                switch[0]=False
        if cget(j,"bg",tmp_board)==cget(sj,"bg",tmp_board):
            if cget(j,"bg",tmp_board)=="red":
                if switch[2]==True:
                    count_result[0][2]+=1
            elif cget(j,"bg",tmp_board)=="white":
                if switch[3]==True:
                    count_result[0][3]+=1
        else:
            if cget(j,"bg",tmp_board)=="red":
                switch[3]=False
            elif cget(j,"bg",tmp_board)=="white":
                switch[2]=False

    switch=[True,True,True,True]
    for i in range(1,4,1):
        if x-i<1:
            break
        ax=12-(x-i)
        ay=y-1
        j=ax*8+ay
        if board[j][1:3]=="00":
            break
        ax=12-startx
        ay=starty-1
        sj=ax*8+ay
        if cget(j,"text",tmp_board)==cget(sj,"text",tmp_board):
            if cget(j,"text",tmp_board)=="●":
                if switch[0]==True:
                    count_result[0][0]+=1
            elif cget(j,"text",tmp_board)=="○":
                if switch[1]==True:
                    count_result[0][1]+=1
        else:
            if cget(j,"text",tmp_board)=="●":
                switch[1]=False
            elif cget(j,"text",tmp_board)=="○":
                switch[0]=False
        if cget(j, "bg", tmp_board) == cget(sj, "bg", tmp_board):
            if cget(j, "bg", tmp_board)=="red":
                if switch[2]==True:
                    count_result[0][2]+=1
            elif cget(j, "bg", tmp_board)=="white":
                if switch[3]==True:
                    count_result[0][3]+=1
        else:
            if cget(j, "bg", tmp_board)=="red":
                switch[3]=False
            elif cget(j, "bg", tmp_board)=="white":
                switch[2]=False
    switch=[True,True,True,True]
    for i in range(1,4,1):
        if y-i<1:
            break
        ax=12-x
        ay=(y-i)-1
        j=ax*8+ay
        if tmp_board[j][1:3]=="00":
            break
        ax=12-startx
        ay=starty-1
        sj=ax*8+ay
        # if lablelist[j].cget("text")==lablelist[sj].cget("text"):
        if cget(j, "text", tmp_board) == cget(sj, "text", tmp_board):
            # if lablelist[j].cget("text")=="●":
            if cget(j, "text", tmp_board)=="●":
                if switch[0]==True:
                    count_result[1][0]+=1
            # elif lablelist[j].cget("text")=="○":
            elif cget(j, "text", tmp_board)=="○":
                if switch[1]==True:
                    count_result[1][1]+=1
        else:
            # if lablelist[j].cget("text")=="●":
            if cget(j, "text", tmp_board)=="●":
                switch[1]=False
            # elif lablelist[j].cget("text")=="○":
            elif cget(j, "text", tmp_board)=="○":
                switch[0]=False
        # if lablelist[j].cget("bg")==lablelist[sj].cget("bg"):
        if cget(j, "bg", tmp_board) == cget(sj, "bg", tmp_board):
            # if lablelist[j].cget("bg")=="red":
            if cget(j, "bg", tmp_board) == "red":
                if switch[2]==True:
                    count_result[1][2]+=1
            # elif lablelist[j].cget("bg")=="white":
            elif cget(j, "bg", tmp_board) == "white":
                if switch[3]==True:
                    count_result[1][3]+=1
        else:
            # if lablelist[j].cget("bg")=="red":
            if cget(j, "bg", tmp_board) == "red":
                switch[3]=False
            # elif lablelist[j].cget("bg")=="white":
            elif cget(j, "bg", tmp_board) == "white":
                switch[2]=False
    switch=[True,True,True,True]
    for i in range(1,4,1):
        if y+i>8:
            break
        ax=12-x
        ay=(y+i)-1
        j=ax*8+ay
        if tmp_board[j][1:3]=="00":
            break
        ax=12-startx
        ay=starty-1
        sj=ax*8+ay
        # if lablelist[j].cget("text")==lablelist[sj].cget("text"):
        if cget(j, "text", tmp_board) == cget(sj, "text", tmp_board):
            # if lablelist[j].cget("text")=="●":
            if cget(j, "text", tmp_board)=="●":
                if switch[0]==True:
                    count_result[1][0]+=1
            # elif lablelist[j].cget("text")=="○":
            elif cget(j, "text", tmp_board)=="○":
                if switch[1]==True:
                    count_result[1][1]+=1
        else:
            # if lablelist[j].cget("text")=="●":
            if cget(j, "text", tmp_board)=="●":
                switch[1]=False
            # elif lablelist[j].cget("text")=="○":
            elif cget(j, "text", tmp_board)=="○":
                switch[0]=False
        # if lablelist[j].cget("bg")==lablelist[sj].cget("bg"):
        if cget(j, "bg", tmp_board) == cget(sj, "bg", tmp_board):
            # if lablelist[j].cget("bg")=="red":
            if cget(j, "bg", tmp_board)=="red":
                if switch[2]==True:
                    count_result[1][2]+=1
            # elif lablelist[j].cget("bg")=="white":
            elif cget(j, "bg", tmp_board)=="white":
                if switch[3]==True:
                    count_result[1][3]+=1
        else:
            # if lablelist[j].cget("bg")=="red":
            if cget(j, "bg", tmp_board)=="red":
                switch[3]=False
            # elif lablelist[j].cget("bg")=="white":
            elif cget(j, "bg", tmp_board)=="white":
                switch[2]=False
    switch=[True,True,True,True]
    for i in range(1,4,1):
        if y-i<1 or x-i<1:
            break
        ax=12-(x-i)
        ay=(y-i)-1
        j=ax*8+ay
        if board[j][1:3]=="00":
            break
        ax=12-startx
        ay=starty-1
        sj=ax*8+ay
        # if lablelist[j].cget("text")==lablelist[sj].cget("text"):
        if cget(j, "text", tmp_board) == cget(sj, "text", tmp_board):
            # if lablelist[j].cget("text")=="●":
            if cget(j, "text", tmp_board)=="●":
                if switch[0]==True:
                    count_result[2][0]+=1
            # elif lablelist[j].cget("text")=="○":
            elif cget(j, "text", tmp_board)=="○":
                if switch[1]==True:
                    count_result[2][1]+=1
        else:
            # if lablelist[j].cget("text")=="●":
            if cget(j, "text", tmp_board)=="●":
                switch[1]=False
            # elif lablelist[j].cget("text")=="○":
            elif cget(j, "text", tmp_board)=="○":
                switch[0]=False
        # if lablelist[j].cget("bg")==lablelist[sj].cget("bg"):
        if cget(j, "bg", tmp_board) == cget(sj, "bg", tmp_board):
            # if lablelist[j].cget("bg")=="red":
            if cget(j, "bg", tmp_board)=="red":
                if switch[2]==True:
                    count_result[2][2]+=1
            # elif lablelist[j].cget("bg")=="white":
            elif cget(j, "bg", tmp_board)=="white":
                if switch[3]==True:
                    count_result[2][3]+=1
        else:
            # if lablelist[j].cget("bg")=="red":
            if cget(j, "bg", tmp_board)=="red":
                switch[3]=False
            # elif lablelist[j].cget("bg")=="white":
            elif cget(j, "bg", tmp_board)=="white":
                switch[2]=False
    switch=[True,True,True,True]
    for i in range(1,4,1):
        if y+i>8 or x+i>12:
            break
        ax=12-(x+i)
        ay=(y+i)-1
        j=ax*8+ay
        if tmp_board[j][1:3]=="00":
            break
        ax=12-startx
        ay=starty-1
        sj=ax*8+ay
        # if lablelist[j].cget("text")==lablelist[sj].cget("text"):
        if cget(j, "text", tmp_board) == cget(sj, "text", tmp_board):
            # if lablelist[j].cget("text")=="●":
            if cget(j, "text", tmp_board)=="●":
                if switch[0]==True:
                    count_result[2][0]+=1
            # elif lablelist[j].cget("text")=="○":
            elif cget(j, "text", tmp_board)=="○":
                if switch[1]==True:
                    count_result[2][1]+=1
        else:
            # if lablelist[j].cget("text")=="●":
            if cget(j, "text", tmp_board)=="●":
                switch[1]=False
            # elif lablelist[j].cget("text")=="○":
            elif cget(j, "text", tmp_board)=="○":
                switch[0]=False
        # if lablelist[j].cget("bg")==lablelist[sj].cget("bg"):
        if cget(j, "bg", tmp_board) == cget(sj, "bg", tmp_board):
            # if lablelist[j].cget("bg")=="red":
            if cget(j, "bg", tmp_board) =="red":
                if switch[2]==True:
                    count_result[2][2]+=1
            # elif lablelist[j].cget("bg")=="white":
            elif cget(j, "bg", tmp_board) =="white":
                if switch[3]==True:
                    count_result[2][3]+=1
        else:
            # if lablelist[j].cget("bg")=="red":
            if cget(j, "bg", tmp_board) =="red":
                switch[3]=False
            # elif lablelist[j].cget("bg")=="white":
            elif cget(j, "bg", tmp_board) =="white":
                switch[2]=False
    switch=[True,True,True,True]
    for i in range(1,4,1):
        if y-i<1 or x+i>12:
            break
        ax=12-(x+i)
        ay=(y-i)-1
        j=ax*8+ay
        if tmp_board[j][1:3]=="00":
            break
        ax=12-startx
        ay=starty-1
        sj=ax*8+ay
        # if lablelist[j].cget("text")==lablelist[sj].cget("text"):
        if cget(j, "text", tmp_board) == cget(sj, "text", tmp_board):
            # if lablelist[j].cget("text")=="●":
            if cget(j, "text", tmp_board)=="●":
                if switch[0]==True:
                    count_result[3][0]+=1
            # elif lablelist[j].cget("text")=="○":
            elif cget(j, "text", tmp_board)=="○":
                if switch[1]==True:
                    count_result[3][1]+=1
        else:
            # if lablelist[j].cget("text")=="●":
            if cget(j, "text", tmp_board)=="●":
                switch[1]=False
            # elif lablelist[j].cget("text")=="○":
            elif cget(j, "text", tmp_board)=="○":
                switch[0]=False
        # if lablelist[j].cget("bg")==lablelist[sj].cget("bg"):
        if cget(j, "bg", tmp_board) == cget(sj, "bg", tmp_board):
            # if lablelist[j].cget("bg")=="red":
            if cget(j, "bg", tmp_board)=="red":
                if switch[2]==True:
                    count_result[3][2]+=1
            # elif lablelist[j].cget("bg")=="white":
            elif cget(j, "bg", tmp_board)=="white":
                if switch[3]==True:
                    count_result[3][3]+=1
        else:
            # if lablelist[j].cget("bg")=="red":
            if cget(j, "bg", tmp_board)=="red":
                switch[3]=False
            # elif lablelist[j].cget("bg")=="white":
            elif cget(j, "bg", tmp_board)=="white":
                switch[2]=False
    switch=[True,True,True,True]
    for i in range(1,4,1):
        if y+i>8 or x-i<1:
            break
        ax=12-(x-i)
        ay=(y+i)-1
        j=ax*8+ay
        if board[j][1:3]=="00":
            break
        ax=12-startx
        ay=starty-1
        sj=ax*8+ay
        # if lablelist[j].cget("text")==lablelist[sj].cget("text"):
        if cget(j, "text", tmp_board) == cget(sj, "text", tmp_board):
            # if lablelist[j].cget("text")=="●":
            if cget(j, "text", tmp_board)=="●":
                if switch[0]==True:
                    count_result[3][0]+=1
            # elif lablelist[j].cget("text")=="○":
            elif cget(j, "text", tmp_board)=="○":
                if switch[1]==True:
                    count_result[3][1]+=1
        else:
            # if lablelist[j].cget("text")=="●":
            if cget(j, "text", tmp_board)=="●":
                switch[1]=False
            # elif lablelist[j].cget("text")=="○":
            elif cget(j, "text", tmp_board)=="○":
                switch[0]=False
        # if lablelist[j].cget("bg")==lablelist[sj].cget("bg"):
        if cget(j, "bg", tmp_board) == cget(sj, "bg", tmp_board):
            # if lablelist[j].cget("bg")=="red":
            if cget(j, "bg", tmp_board)=="red":
                if switch[2]==True:
                    count_result[3][2]+=1
            # elif lablelist[j].cget("bg")=="white":
            elif cget(j, "bg", tmp_board)=="white":
                if switch[3]==True:
                    count_result[3][3]+=1
        else:
            # if lablelist[j].cget("bg")=="red":
            if cget(j, "bg", tmp_board)=="red":
                switch[3]=False
            # elif lablelist[j].cget("bg")=="white":
            elif cget(j, "bg", tmp_board)=="white":
                switch[2]=False
    return count_result

def AI_check_winning(x,y,cardtype,board):
    global game_finished
    ax=12-x
    ay=y-1
    j=ax*8+ay
    # 读哪种卡片 总共八种 0-7
    # cardtype=ct
    # 把上一步的数据带进来
    result=AI_check_winning_result(x,y,board)
    # if board[j][0]=="A":
    if current_player == "A":
        # 判a玩的是啥， false是颜色
        if playerA_Select==False:
            for i in result:
                if i[2]>=4 or i[3]>=4:
                    # game_finished=True
                    # bottomlable.config(text="Player A Wins.")
                    return "A"
            # 先判断A玩的所有方向 之后才能判断B
            for i in result:
                if i[0]>=4 or i[1]>=4:
                    # game_finished=True
                    # bottomlable.config(text="Player B Wins.")
                    return "B"
        # 判断A 玩的是点的情况
        else:
            for i in result:
                if i[0]>=4 or i[1]>=4:
                    # game_finished=True
                    # bottomlable.config(text="Player A Wins.")
                    return "A"
            for i in result:
                if i[2]>=4 or i[3]>=4:
                    # game_finished=True
                    # bottomlable.config(text="Player B Wins.")
                    return "B"
    # 现在是B下的情况
    else:
        if playerA_Select==False:
            for i in result:
                if i[0]>=4 or i[1]>=4:
                    # game_finished=True
                    # bottomlable.config(text="Player B Wins.")
                    return "B"
            for i in result:
                if i[2]>=4 or i[3]>=4:
                    # game_finished=True
                    # bottomlable.config(text="Player A Wins.")
                    return "A"
        else:
            for i in result:
                if i[2]>=4 or i[3]>=4:
                    # game_finished=True
                    # bottomlable.config(text="Player B Wins.")
                    return "B"
            for i in result:
                if i[0]>=4 or i[1]>=4:
                    # game_finished=True
                    # bottomlable.config(text="Player A Wins.")
                    return "A"
    # 统计前四种卡片上面的数值
    if cardtype==0 or cardtype==1 or cardtype==2 or cardtype==3:
        result=AI_check_winning_result(x+1,y,board)
    # 统计右边的
    elif cardtype==4 or cardtype==5 or cardtype==6 or cardtype==7:
        result=AI_check_winning_result(x,y+1,board)
    # if board[j][0]=="A":
    if current_player == "A":
        if playerA_Select==False:
            for i in result:
                if i[2]>=4 or i[3]>=4:
                    # game_finished=True
                    # bottomlable.config(text="Player A Wins.")
                    return "A"
            for i in result:
                if i[0]>=4 or i[1]>=4:
                    # game_finished=True
                    # bottomlable.config(text="Player B Wins.")
                    return "B"
        else:
            for i in result:
                if i[0]>=4 or i[1]>=4:
                    # game_finished=True
                    # bottomlable.config(text="Player A Wins.")
                    return "A"
            for i in result:
                if i[2]>=4 or i[3]>=4:
                    # game_finished=True
                    # bottomlable.config(text="Player B Wins.")
                    return "B"
    else:
        if playerA_Select==False:
            for i in result:
                if i[0]>=4 or i[1]>=4:
                    # game_finished=True
                    # bottomlable.config(text="Player B Wins.")
                    return "B"
            for i in result:
                if i[2]>=4 or i[3]>=4:
                    # game_finished=True
                    # bottomlable.config(text="Player A Wins.")
                    return "A"
        else:
            for i in result:
                if i[2]>=4 or i[3]>=4:
                    # game_finished=True
                    # bottomlable.config(text="Player B Wins.")
                    return "B"
            for i in result:
                if i[0]>=4 or i[1]>=4:
                    # game_finished=True
                    # bottomlable.config(text="Player A Wins.")
                    return "A"
    return

def AIafter24checkremoveable(x,y,tmp_board,lastremovestepcount):
    ax = 12 - x
    ay = y - 1
    j = ax * 8 + ay
    cancelstep = tmp_board[j][1:3]
    if cancelstep == "00":
        return False
    if cancelstep == "%02d"%(lastremovestepcount-1):
        return False
    cardtype = int(tmp_board[j][3])
    if cardtype == 0 or cardtype == 1 or cardtype == 2 or cardtype == 3:
        if x == 12:
            return False
        if x > 1:
            if tmp_board[j + 8][1:3] == cancelstep:
                return False
            elif tmp_board[j-8][1:3] == cancelstep:
                if tmp_board[j-16][1:3] == "00" or j-16<0:
                    return True
                else:
                    return False
            else:
                return False
        if x == 1:
            if tmp_board[j - 8][1:3] == cancelstep:
                if tmp_board[j - 16][1:3] =="00":
                    return True
                else:
                    return False
            else:
                return False
        return False
    elif cardtype == 4 or cardtype == 5 or cardtype == 6 or cardtype == 7:
        if x==12:
            if y==8:
                return False
            else:
                if tmp_board[j+1][1:3] == cancelstep:
                    return True
                else:
                    return False
        else:
            if y==8:
                return False
            else:
                if tmp_board[j + 1][1:3] == cancelstep:
                    if tmp_board[j-8][1:3] == "00" and tmp_board[j+1-8][1:3] == "00":
                        return True
                    else:
                        return False
                else:
                    return False
        return False

# 24步以后
def fillboardafter24(x,y,placecardtype):
    global current_player
    global stepcount
    global after24remove
    global lastremovecardtype
    global lastremovecardposition
    global board
    ax=12-x
    ay=y-1
    j=ax*8+ay
    if after24remove==True:
        # 找这个卡是第几回合下的
        cancelstep=board[j][1:3]
        if cancelstep=="00":
            return False
        # 格式化输出
        if cancelstep=="%02d"%(stepcount-1):
            return False
        cardtype=int(board[j][3])
        if cardtype==0 or cardtype==1 or cardtype==2 or cardtype==3:
            if x==12:
                lastremovecardposition[0][0]=x
                lastremovecardposition[0][1]=y
                lastremovecardposition[1][0]=x-1
                lastremovecardposition[1][1]=y
                for i in range(0, len(board), 1):
                    if board[i][1:3] == cancelstep:
                        lastremovecardtype = int(board[i][3])
                        board[i] = "X000"
                        lablelist[i].config(text="", bg="grey")
                jianqu_en(x, y, cardtype)
                after24remove = False
                return True
            if x>1:
                if board[j+8][1:3]==cancelstep:
                    if board[j-8][1:3]=="00":
                        lastremovecardposition[0][0] = x
                        lastremovecardposition[0][1] = y
                        lastremovecardposition[1][0] = x-1
                        lastremovecardposition[1][1] = y
                        for i in range(0, len(board), 1):
                            if board[i][1:3] == cancelstep:
                                lastremovecardtype = int(board[i][3])
                                board[i] = "X000"
                                lablelist[i].config(text="", bg="grey")
                        jianqu_en(x, y, cardtype)
                        after24remove = False
                        return True
            if x<12:
                if board[j-8][1:3]==cancelstep:
                    if x==11:
                        lastremovecardposition[0][0] = x
                        lastremovecardposition[0][1] = y
                        lastremovecardposition[1][0] = x + 1
                        lastremovecardposition[1][1] = y
                        for i in range(0, len(board), 1):
                            if board[i][1:3] == cancelstep:
                                lastremovecardtype = int(board[i][3])
                                board[i] = "X000"
                                lablelist[i].config(text="", bg="grey")
                        jianqu_en(x, y, cardtype)
                        after24remove = False
                        return True
                    if board[j-16][1:3]=="00":
                        lastremovecardposition[0][0] = x
                        lastremovecardposition[0][1] = y
                        lastremovecardposition[1][0] = x+1
                        lastremovecardposition[1][1] = y
                        for i in range(0, len(board), 1):
                            if board[i][1:3] == cancelstep:
                                lastremovecardtype = int(board[i][3])
                                board[i] = "X000"
                                lablelist[i].config(text="", bg="grey")
                        jianqu_en(x, y, cardtype)
                        after24remove = False
                        return True
        elif cardtype==4 or cardtype==5 or cardtype==6 or cardtype==7:
            if x==12:
                lastremovecardposition[0][0] = x
                lastremovecardposition[0][1] = y
                lastremovecardposition[1][0] = x
                if board[j+1][1:3]==cancelstep:
                    lastremovecardposition[1][1] = y+1
                elif board[j-1][1:3]==cancelstep:
                    lastremovecardposition[1][1] = y-1
                # lastremovecardposition[1][1] = y+1
                for i in range(0, len(board), 1):
                    if board[i][1:3] == cancelstep:
                        lastremovecardtype = int(board[i][3])
                        board[i] = "X000"
                        lablelist[i].config(text="", bg="grey")
                jianqu_en(x, y, cardtype)
                after24remove = False
                return True
            if y==1:
                if board[j+1][1:3]==cancelstep:
                    if board[j-8][1:3]=="00" and board[j+1-8][1:3]=="00":
                        lastremovecardposition[0][0] = x
                        lastremovecardposition[0][1] = y
                        lastremovecardposition[1][0] = x
                        lastremovecardposition[1][1] = y+1
                        for i in range(0, len(board), 1):
                            if board[i][1:3] == cancelstep:
                                lastremovecardtype = int(board[i][3])
                                board[i] = "X000"
                                lablelist[i].config(text="", bg="grey")
                        jianqu_en(x, y, cardtype)
                        after24remove = False
                        return True
            elif y==8:
                if board[j-1][1:3]==cancelstep:
                    if board[j-8][1:3]=="00" and board[j-8-1][1:3]=="00":
                        lastremovecardposition[0][0] = x
                        lastremovecardposition[0][1] = y
                        lastremovecardposition[1][0] = x
                        lastremovecardposition[1][1] = y-1
                        for i in range(0, len(board), 1):
                            if board[i][1:3] == cancelstep:
                                lastremovecardtype = int(board[i][3])
                                board[i] = "X000"
                                lablelist[i].config(text="", bg="grey")
                        jianqu_en(x, y, cardtype)
                        after24remove = False
                        return True
            else:
                if board[j+1][1:3]==cancelstep:
                    if board[j-8][1:3]=="00" and board[j+1-8][1:3]=="00":
                        lastremovecardposition[0][0] = x
                        lastremovecardposition[0][1] = y
                        lastremovecardposition[1][0] = x
                        lastremovecardposition[1][1] = y+1
                        for i in range(0, len(board), 1):
                            if board[i][1:3] == cancelstep:
                                lastremovecardtype = int(board[i][3])
                                board[i] = "X000"
                                lablelist[i].config(text="", bg="grey")
                        jianqu_en(x, y, cardtype)
                        after24remove = False
                        return True
                elif board[j-1][1:3]==cancelstep:
                    if board[j-8][1:3]=="00" and board[j-8-1][1:3]=="00":
                        lastremovecardposition[0][0] = x
                        lastremovecardposition[0][1] = y
                        lastremovecardposition[1][0] = x
                        lastremovecardposition[1][1] = y-1
                        for i in range(0, len(board), 1):
                            if board[i][1:3] == cancelstep:
                                lastremovecardtype = int(board[i][3])
                                board[i] = "X000"
                                lablelist[i].config(text="", bg="grey")
                        jianqu_en(x, y, cardtype)
                        after24remove = False
                        return True

    elif after24remove==False:
        # movecardtype=board[j][3:]
        if (x ==lastremovecardposition[0][0] and y ==y==lastremovecardposition[0][1]) or (x ==lastremovecardposition[0][0] and y ==y==lastremovecardposition[0][1]):
                if lastremovecardtype==placecardtype:
                    bottomlable.config(text="Can't same card at same place.")
                    return False
        if lastremovecardtype==0 or lastremovecardtype==1 or lastremovecardtype==4 or lastremovecardtype==5:
            if placecardtype==0 or placecardtype==1 or placecardtype==4 or placecardtype==5:
                if fillboardbefore24andmovecard(x, y, placecardtype):
                    after24remove=True
                return True
            else:
                bottomlable.config(text="Must be rotate card.")
                return False
        elif lastremovecardtype==2 or lastremovecardtype==3 or lastremovecardtype==6 or lastremovecardtype==7:
            if placecardtype==2 or placecardtype==3 or placecardtype==6 or placecardtype==7:
                # if fillboardbefore24andmovecard(x, y, placecardtype, False):
                if fillboardbefore24andmovecard(x, y, placecardtype):
                    after24remove=True
                return True
            else:
                bottomlable.config(text="Must be rotate card.")
                return False
        # if fillboardbefore24andmovecard(x,y,int(movecardtype),False):
        #     after24remove=True



def fillboardbefore24andmovecard(x,y,cardtype):
    global current_player
    global stepcount
    ax=12-x
    ay=y-1
    j=ax*8+ay
    if cardtype==0:
        if x==12:
            return False
        if not board[j][0]=="X" or not board[j-8][0]=="X":
            return False
        #  true 是24步之前
        # if isfill==True:
        if not x==1:
            if board[j+8][0]=="X":
                return False
        # 填gui对应的板子
        jia_en(x, y, cardtype)
        board[j]=current_player+"%02d"%(stepcount)+"0"
        board[j-8]=current_player+"%02d"%(stepcount)+"0"
        lablelist[j].config(text="●",bg="red")
        lablelist[j-8].config(text="○",bg="white")
        print("Position:\n",lookup_dic.get(y)," ",x)
        print("Cardtype:", cardtype_dic.get(cardtype))

    elif cardtype==1:
        if x==12:
            return False
        if not board[j][0]=="X" or not board[j-8][0]=="X":
            return False
        # if isfill==True:
        if not x==1:
            if board[j+8][0]=="X":
                return False
        jia_en(x, y, cardtype)
        board[j-8]=current_player+"%02d"%(stepcount)+"1"
        board[j]=current_player+"%02d"%(stepcount)+"1"
        lablelist[j-8].config(text="●",bg="red")
        lablelist[j].config(text="○",bg="white")
        print("Position:\n",lookup_dic.get(y)," ",x)
        print("Cardtype:", cardtype_dic.get(cardtype))

    elif cardtype==2:
        if x==12:
            return False
        if not board[j][0]=="X" or not board[j-8][0]=="X":
            return False
        # if isfill==True:
        if not x==1:
            if board[j+8][0]=="X":
                return False
        jia_en(x, y, cardtype)
        board[j]=current_player+"%02d"%(stepcount)+"2"
        board[j-8]=current_player+"%02d"%(stepcount)+"2"
        lablelist[j].config(text="●",bg="white")
        lablelist[j-8].config(text="○",bg="red")
        print("Position:\n",lookup_dic.get(y)," ",x)
        print("Cardtype:", cardtype_dic.get(cardtype))

    elif cardtype==3:
        if x==12:
            return False
        if not board[j][0]=="X" or not board[j-8][0]=="X":
            return False
        # if isfill==True:
        if not x==1:
            if board[j+8][0]=="X":
                return False
        jia_en(x, y, cardtype)
        board[j-8]=current_player+"%02d"%(stepcount)+"3"
        board[j]=current_player+"%02d"%(stepcount)+"3"
        lablelist[j-8].config(text="●",bg="white")
        lablelist[j].config(text="○",bg="red")
        print("Position:\n",lookup_dic.get(y)," ",x)
        print("Cardtype:", cardtype_dic.get(cardtype))

    elif cardtype==4:
        if y==8:
            return False
        if not board[j][0]=="X" or not board[j+1][0]=="X":
            return False
        # if isfill==True:
        if not x==1:
            if board[j+8][0]=="X" or board[j+8+1][0]=="X":
                return False
        jia_en(x, y, cardtype)
        board[j]=current_player+"%02d"%(stepcount)+"4"
        board[j+1]=current_player+"%02d"%(stepcount)+"4"
        lablelist[j].config(text="●",bg="red")
        lablelist[j+1].config(text="○",bg="white")
        print("Position:\n",lookup_dic.get(y)," ",x)
        print("Cardtype:", cardtype_dic.get(cardtype))

    elif cardtype==5:
        if y==8:
            return False
        if not board[j][0]=="X" or not board[j+1][0]=="X":
            return False
        # if isfill==True:
        if not x==1:
            if board[j+8][0]=="X" or board[j+8+1][0]=="X":
                return False
        jia_en(x, y, cardtype)
        board[j+1]=current_player+"%02d"%(stepcount)+"5"
        board[j]=current_player+"%02d"%(stepcount)+"5"
        lablelist[j+1].config(text="●",bg="red")
        lablelist[j].config(text="○",bg="white")
        print("Position:\n",lookup_dic.get(y)," ",x)
        print("Cardtype:", cardtype_dic.get(cardtype))

    elif cardtype==6:
        if y==8:
            return False
        if not board[j][0]=="X" or not board[j+1][0]=="X":
            return False
        # if isfill==True:
        if not x==1:
            if board[j+8][0]=="X" or board[j+8+1][0]=="X":
                return False
        jia_en(x, y, cardtype)
        board[j]=current_player+"%02d"%(stepcount)+"6"
        board[j+1]=current_player+"%02d"%(stepcount)+"6"
        lablelist[j].config(text="●",bg="white")
        lablelist[j+1].config(text="○",bg="red")
        print("Position:\n",lookup_dic.get(y)," ",x)
        print("Cardtype:", cardtype_dic.get(cardtype))

    elif cardtype==7:
        if y==8:
            return False
        if not board[j][0]=="X" or not board[j+1][0]=="X":
            return False
        # if isfill==True:
        if not x==1:
            if board[j+8][0]=="X" or board[j+8+1][0]=="X":
                return False
        jia_en(x, y, cardtype)
        board[j+1]=current_player+"%02d"%(stepcount)+"7"
        board[j]=current_player+"%02d"%(stepcount)+"7"
        lablelist[j+1].config(text="●",bg="white")
        lablelist[j].config(text="○",bg="red")
        print("Position:\n",lookup_dic.get(y)," ",x)
        print("Cardtype:", cardtype_dic.get(cardtype))

    if current_player=="A":
        current_player="B"
        bottomlable.config(text="Player B Turn.")
    else:
        current_player="A"
        bottomlable.config(text="Player A Turn.")
    stepcount+=1
    bottomlable2.config(text="Step: "+str(stepcount-1))
    check_winning(x,y)
    return True

def AI_fillboardafter24(x,y,x2,y2,cardtype,tmp_board):
    cardtype=int(cardtype)
    AI_after24_list = []
    ax=12-x
    ay=y-1
    j=ax*8+ay
    tt_board = []
    for i in range(0,len(tmp_board),1):
        tt_board.append(tmp_board[i])
    cancelstep=tmp_board[j][1:3]
    opposite={"0":"1","1":"0","2":"3","3":"2","4":"5","5":"4","6":"7","7":"6"}
    for a in range(1,13,1):
        for b in range(1,9,1):
            for c in range(0,8,1):
                if cardtype == 0 or cardtype == 1 or cardtype == 4 or cardtype == 5:
                    if c == 0 or c == 1 or c == 4 or c == 5:
                        if a == min(x,x2) and b == min(y,y2) and c == cardtype:
                            pass
                        elif AI_check_card(a, b, c, tt_board):
                            AI_after24_list.append([a,b,c,x,y,x2,y2])
                elif cardtype == 2 or cardtype == 3 or cardtype == 6 or cardtype == 7:
                    if c == 2 or c == 3 or c == 6 or c == 7:
                        if a == min(x,x2) and b ==min(y,y2) and c == cardtype:
                            pass
                        elif AI_check_card(a, b, c, tt_board):
                            AI_after24_list.append([a,b,c,ax,ay,x2,y2])
    return AI_after24_list

def AI_can_cancle_step(x,y,tmp_board):
    global AI_minmax_status
    AI_minmax_status = False
    ax = 12 - x
    ay = y - 1
    j = ax * 8 + ay
    canclestep = tmp_board[j][1:3]

    if canclestep == "00":
        return
    # 格式化输出
    if canclestep == "%02d" % (stepcount - 1):
        return
    cardtype = int(tmp_board[j][3])
    if cardtype == 0 or cardtype == 1 or cardtype == 2 or cardtype == 3:
        if x == 12:
            tmp_board[j]="X000"
            tmp_board[j+8]="X000"
            AI_minmax_status = True
            return tmp_board
        if x > 1:
            if tmp_board[j + 8][1:3] == canclestep:
                if tmp_board[j - 8][1:3] == "00":
                    tmp_board[j]="X000"
                    tmp_board[j+8]="X000"
                    AI_minmax_status = True
                    return tmp_board
        if x < 12:
            if tmp_board[j - 8][1:3] == canclestep:
                if x == 11:
                    tmp_board[j]="X000"
                    tmp_board[j-8]="X000"
                    AI_minmax_status = True
                    return tmp_board
                if tmp_board[j - 16][1:3] == "00":
                    tmp_board[j]="X000"
                    tmp_board[j-8]="X000"
                    AI_minmax_status = True
                    return tmp_board
    elif cardtype == 4 or cardtype == 5 or cardtype == 6 or cardtype == 7:
        if x == 12:
            if tmp_board[j + 1][1:3] == canclestep:
                tmp_board[j]="X000"
                tmp_board[j+1]="X000"
            elif tmp_board[j - 1][1:3] == canclestep:
                tmp_board[j]="X000"
                tmp_board[j-1]="X000"
            AI_minmax_status = True
            return tmp_board
        if y == 1:
            if tmp_board[j + 1][1:3] == canclestep:
                if tmp_board[j - 8][1:3] == "00" and tmp_board[j + 1 - 8][1:3] == "00":
                    tmp_board[j]= "X000"
                    AI_minmax_status = True
                    return tmp_board
        elif y == 8:
            if tmp_board[j - 1][1:3] == canclestep:
                if tmp_board[j - 8][1:3] == "00" and tmp_board[j - 8 - 1][1:3] == "00":
                    tmp_board[j]="X000"
                    tmp_board[j-1]="X000"
                    AI_minmax_status = True
                    return tmp_board
        else:
            if tmp_board[j + 1][1:3] == canclestep:
                if tmp_board[j - 8][1:3] == "00" and tmp_board[j + 1 - 8][1:3] == "00":
                    tmp_board[j]="X000"
                    tmp_board[j+1]="X000"
                    AI_minmax_status = True
                    return tmp_board
            elif tmp_board[j - 1][1:3] == canclestep:
                if tmp_board[j - 8][1:3] == "00" and tmp_board[j - 8 - 1][1:3] == "00":
                    tmp_board[j]="X000"
                    tmp_board[j-1]="X000"
                    AI_minmax_status = True
                    return tmp_board

def AI_remove_card(x,y,tmp_board):
    ax = 12 - x
    ay = y - 1
    j = ax * 8 + ay
    cancelstep = tmp_board[j][1:3]
    result=[]
    for x2 in range(1,13,1):
        for y2 in range(1,9,1):
            ax2 = 12 - x2
            ay2 = y2 - 1
            j2 = ax2 * 8 + ay2
            if tmp_board[j2][1:3] == cancelstep:
                tmp_board[j2]="X000"
                result.append([x2,y2])
    return [tmp_board,result[0],result[1]]


# def AIfillboard(x,y,cardtype):
#     if game_finished==True:
#         return
#     if stepcount<=24:
#         fillboardbefore24andmovecard(x,y,cardtype,True)
#     elif stepcount<=60:
#         fillboardafter24(x,y,cardtype) #   kkkkkkkk
#     else:
#         bottomlable.config(text="Game end with a draw.")
#         return



def fillboard(x, y):
    # print("fill board")
    global hecallcount
    global level2he
    if game_finished == True:
        return
    if stepcount <= 24:
        if fillboardbefore24andmovecard(x, y, rbvar.get()) == False:
            return
    elif stepcount <= 40:
        if fillboardafter24(x, y, rbvar.get())==False:
            frame.update()
            return
        if after24remove==False:
            return
    else:
        bottomlable.config(text="Game end with a draw.")
        return
    if playerBorAI == False:
        frame.update()
        tmp_board=[]
        for i in board:
            tmp_board.append(i)
        if stepcount<=24:
            if game_finished == True:
                return
            # alpha_beta(0, "computer", float("-inf"), float("inf"), board)
            if player1isAI==True:
                if MiniOrAlpha==True:
                    hecallcount = 0
                    level2he = []
                    start = time.time()
                    resss = minimax("max", 0, 0, 2, tmp_board, stepcount)
                    end = time.time()
                    print (end - start)
                    if var2.get()==1:
                        file.writelines(str(hecallcount)+"\r\n")
                        file.writelines(str(resss) + "\r\n")
                        file.writelines("\r\n")
                        for i in level2he:
                            file.writelines(str(i) + "\r\n")
                        file.writelines("\r\n")
                    # print(str(hecallcount))
                    # print(str(resss))
                else:
                    hecallcount = 0
                    level2he = []
                    start = time.time()
                    resss = AI_alphabeta("max",0,0,2,tmp_board,stepcount,float("-inf"),float("inf"))
                    end = time.time()
                    print (end - start)
                    if var2.get()==1:
                        file.writelines(str(hecallcount)+"\r\n")
                        file.writelines(str(resss) + "\r\n")
                        file.writelines("\r\n")
                        for i in level2he:
                            file.writelines(str(i) + "\r\n")
                        file.writelines("\r\n")
            else:
                if MiniOrAlpha==True:
                    hecallcount = 0
                    level2he = []
                    start = time.time()
                    resss = minimax("min",0,0,2,tmp_board,stepcount)
                    end = time.time()
                    print (end - start)
                    if var2.get()==1:
                        file.writelines(str(hecallcount)+"\r\n")
                        file.writelines(str(resss) + "\r\n")
                        file.writelines("\r\n")
                        for i in level2he:
                            file.writelines(str(i) + "\r\n")
                        file.writelines("\r\n")
                else:
                    hecallcount = 0
                    level2he = []
                    start = time.time()
                    resss = AI_alphabeta("min",0,0,2,tmp_board,stepcount,float("-inf"),float("inf"))
                    end = time.time()
                    print (end - start)
                    if var2.get()==1:
                        file.writelines(str(hecallcount)+"\r\n")
                        file.writelines(str(resss) + "\r\n")
                        file.writelines("\r\n")
                        for i in level2he:
                            file.writelines(str(i) + "\r\n")
                        file.writelines("\r\n")
            a = xycardtype[0]
            b = xycardtype[1]
            c = xycardtype[2]
            fillboardbefore24andmovecard(a, b, c)
            frame.update()
        elif stepcount<=40:
            exchange = {False: "A", True: "B"}
            if not current_player==exchange.get(player1isAI):
                if game_finished == True:
                    return
                tmp_board=[]
                for i in board:
                    tmp_board.append(i)
                # if selrbvar3.get() == 0:
                #     if player1isAI
                #     minimax()

                if player1isAI == True:
                    if MiniOrAlpha == True:
                        hecallcount = 0
                        level2he = []
                        start = time.time()
                        resss = minimaxafter24("max", 0, 0, 2, tmp_board, stepcount)
                        end = time.time()
                        print (end - start)
                        if var2.get() == 1:
                            file.writelines(str(hecallcount) + "\r\n")
                            file.writelines(str(resss) + "\r\n")
                            file.writelines("\r\n")
                            for i in level2he:
                                file.writelines(str(i) + "\r\n")
                            file.writelines("\r\n")
                    else:
                        hecallcount = 0
                        level2he = []
                        start = time.time()
                        resss = AI_alphabetaafter24("max", 0, 0, 2, tmp_board, stepcount, float("-inf"), float("inf"))
                        end = time.time()
                        print (end - start)
                        if var2.get() == 1:
                            file.writelines(str(hecallcount) + "\r\n")
                            file.writelines(str(resss) + "\r\n")
                            file.writelines("\r\n")
                            for i in level2he:
                                file.writelines(str(i) + "\r\n")
                            file.writelines("\r\n")
                else:
                    if MiniOrAlpha == True:
                        hecallcount = 0
                        level2he = []
                        start = time.time()
                        resss = minimaxafter24("min", 0, 0, 1, tmp_board, stepcount)
                        end = time.time()
                        print (end - start)
                        if var2.get() == 1:
                            file.writelines(str(hecallcount) + "\r\n")
                            file.writelines(str(resss) + "\r\n")
                            file.writelines("\r\n")
                            for i in level2he:
                                file.writelines(str(i) + "\r\n")
                            file.writelines("\r\n")
                    else:
                        hecallcount = 0
                        level2he = []
                        start = time.time()
                        resss = AI_alphabetaafter24("min", 0, 0, 2, tmp_board, stepcount, float("-inf"), float("inf"))
                        end = time.time()
                        print (end - start)
                        if var2.get() == 1:
                            file.writelines(str(hecallcount) + "\r\n")
                            file.writelines(str(resss) + "\r\n")
                            file.writelines("\r\n")
                            for i in level2he:
                                file.writelines(str(i) + "\r\n")
                            file.writelines("\r\n")

                x = removecard[0]
                y = removecard[1]
                z = removecard[2]
                fillboardafter24(x,y,z)
                print("Remove position:\n",lookup_dic.get(y),x)
                print("Remoce cardtype:",cardtype_dic.get(z))

                a = placecard[0]
                b = placecard[1]
                c = placecard[2]
                fillboardafter24(a, b, c)
                frame.update()
                # print("potion:\n",lookup_dic.get(b),a)
                # print("cardtype:",cardtype_dic.get(c))



# # 3 seconds counter
# def counter():
#     global timer
#     global counter_stop
#     counter_stop = False
#
#     # print('3 seconds timer start!')
#     timer = threading.Timer(3,counter)
#     # timer.start()
#
#     time.sleep(3)  # stop the timer in 3 seconds
#     timer.cancel()
#     # print("timer stop")
#     counter_stop = True
#
# #  game start 选择 玩啥
def gamestart():
    global playerA_Select
    global player1isAI
    global playerBorAI
    global MiniOrAlpha
    global hecallcount
    global level2he
    global file
    # 点了选颜色的按键
    if var2.get()==1:
        file=open("./out.txt","w")
    if selrbvar.get() == 0:
        playerA_Select = True
    else:
        playerA_Select = False
    # if selrbvar2.get() == 0:
    #     playerBorAI = True
    # else:
    #     playerBorAI = False
    if var1.get() == 1:
        # False == 选AI
        playerBorAI = False
        if selrbvar2.get() == 0:
            player1isAI = True
        else:
            player1isAI = False
        if selrbvar3.get() == 0:
            MiniOrAlpha = True
        else:
            MiniOrAlpha = False
        if playerBorAI==False:
            if player1isAI==True:
                if MiniOrAlpha==True:
                    hecallcount = 0
                    level2he = []
                    resss = minimax("max", 0, 0, 1, board, stepcount)
                    if var2.get()==1:
                        file.writelines(str(hecallcount)+"\r\n")
                        file.writelines(str(resss) + "\r\n")
                        file.writelines("\r\n")
                        for i in level2he:
                            file.writelines(str(i) + "\r\n")
                        file.writelines("\r\n")
                else:
                    hecallcount = 0
                    level2he = []
                    resss = AI_alphabeta("max",0,0,2,board,stepcount,float("-inf"),float("inf"))
                    if var2.get()==1:
                        file.writelines(str(hecallcount)+"\r\n")
                        file.writelines(str(resss) + "\r\n")
                        file.writelines("\r\n")
                        for i in level2he:
                            file.writelines(str(i) + "\r\n")
                        file.writelines("\r\n")
                fillboardbefore24andmovecard(xycardtype[0], xycardtype[1], xycardtype[2])

    # 把大的掉出来
    frame.update()
    frame.deiconify()
    # 把小的删除
    select.destroy()

# 退出事件改掉
def selectexit():
    exit(0)

def selectexit2():
    exit(0)


def AI_check_card_after24(x,y,cardtype,board,lastremove):
    #global gcount
    #print(gcount)
    #gcount+=1
    ax=12-x
    ay=y-1
    j=ax*8+ay
    if cardtype==0:
        if x==12:
            return False
        if x==lastremove[0] and y==lastremove[1]:
            if not lastremove[2]==1 and not lastremove[2]==4 and not lastremove[2]==5:
                return False
        else:
            if not lastremove[2]==0 and not lastremove[2]==1 and not lastremove[2]==4 and not lastremove[2]==5:
                return False
        if not board[j][0]=="X" or not board[j-8][0]=="X":
            return False
        if not x==1:
            if board[j+8][0]=="X":
                return False
        return True

    elif cardtype==1:
        if x==12:
            return False
        if x==lastremove[0] and y==lastremove[1]:
            if not lastremove[2]==0 and not lastremove[2]==4 and not lastremove[2]==5:
                return False
        else:
            if not lastremove[2]==0 and not lastremove[2]==1 and not lastremove[2]==4 and not lastremove[2]==5:
                return False
        if not board[j][0]=="X" or not board[j-8][0]=="X":
            return False
        if not x==1:
            if board[j+8][0]=="X":
                return False
        return True

    elif cardtype==2:
        if x==12:
            return False
        if x==lastremove[0] and y==lastremove[1]:
            if not lastremove[2]==3 and not lastremove[2]==6 and not lastremove[2]==7:
                return False
        else:
            if not lastremove[2]==2 and not lastremove[2]==3 and not lastremove[2]==6 and not lastremove[2]==7:
                return False
        if not board[j][0]=="X" or not board[j-8][0]=="X":
            return False
        if not x==1:
            if board[j+8][0]=="X":
                return False
        return True

    elif cardtype==3:
        if x==12:
            return False
        if x==lastremove[0] and y==lastremove[1]:
            if not lastremove[2]==2 and not lastremove[2]==6 and not lastremove[2]==7:
                return False
        else:
            if not lastremove[2]==2 and not lastremove[2]==3 and not lastremove[2]==6 and not lastremove[2]==7:
                return False
        if not board[j][0]=="X" or not board[j-8][0]=="X":
            return False
        if not x==1:
            if board[j+8][0]=="X":
                return False
        return True

    elif cardtype == 4:
        if y == 8:
            return False
        if x==lastremove[0] and y==lastremove[1]:
            if not lastremove[2]==0 and not lastremove[2]==1 and not lastremove[2]==5:
                return False
        else:
            if not lastremove[2]==0 and not lastremove[2]==1 and not lastremove[2]==4 and not lastremove[2]==5:
                return False
        if not board[j][0] == "X" or not board[j + 1][0] == "X":
            return False
        if not x == 1:
            if board[j + 8][0] == "X" or board[j + 8 + 1][0] == "X":
                return False
        return True

    elif cardtype == 5:
        if y == 8:
            return False
        if x==lastremove[0] and y==lastremove[1]:
            if not lastremove[2]==0 and not lastremove[2]==1 and not lastremove[2]==4:
                return False
        else:
            if not lastremove[2]==0 and not lastremove[2]==1 and not lastremove[2]==4 and not lastremove[2]==5:
                return False
        if not board[j][0] == "X" or not board[j + 1][0] == "X":
            return False
        if not x == 1:
            if board[j + 8][0] == "X" or board[j + 8 + 1][0] == "X":
                return False
        return True

    elif cardtype == 6:
        if y == 8:
            return False
        if x==lastremove[0] and y==lastremove[1]:
            if not lastremove[2]==2 and not lastremove[2]==3 and not lastremove[2]==7:
                return False
        else:
            if not lastremove[2]==2 and not lastremove[2]==3 and not lastremove[2]==6 and not lastremove[2]==7:
                return False
        if not board[j][0] == "X" or not board[j + 1][0] == "X":
            return False
        if not x == 1:
            if board[j + 8][0] == "X" or board[j + 8 + 1][0] == "X":
                return False
        return True

    elif cardtype == 7:
        if y == 8:
            return False
        if x==lastremove[0] and y==lastremove[1]:
            if not lastremove[2]==2 and not lastremove[2]==3 and not lastremove[2]==6:
                return False
        else:
            if not lastremove[2]==2 and not lastremove[2]==3 and not lastremove[2]==6 and not lastremove[2]==7:
                return False
        if not board[j][0] == "X" or not board[j + 1][0] == "X":
            return False
        if not x == 1:
            if board[j + 8][0] == "X" or board[j + 8 + 1][0] == "X":
                return False
        return True

# check card
def AI_check_card(x,y,cardtype,board):
    #global gcount
    #print(gcount)
    #gcount+=1
    ax=12-x
    ay=y-1
    j=ax*8+ay
    if cardtype==0:
        if x==12:
            return False
        if not board[j][0]=="X" or not board[j-8][0]=="X":
            return False
        if not x==1:
            if board[j+8][0]=="X":
                return False
        return True

    elif cardtype==1:
        if x==12:
            return False
        if not board[j][0]=="X" or not board[j-8][0]=="X":
            return False
        # if isfill==True:
        if not x==1:
            if board[j+8][0]=="X":
                return False
        return True

    elif cardtype==2:
        if x==12:
            return False
        if not board[j][0]=="X" or not board[j-8][0]=="X":
            return False
        # if isfill==True:
        if not x==1:
            if board[j+8][0]=="X":
                return False
        return True

    elif cardtype==3:
        if x==12:
            return False
        if not board[j][0]=="X" or not board[j-8][0]=="X":
            return False
        # if isfill==True:
        if not x==1:
            if board[j+8][0]=="X":
                return False
        return True

    elif cardtype==4:
        if y==8:
            return False
        if not board[j][0]=="X" or not board[j+1][0]=="X":
            return False
        # if isfill==True:
        if not x==1:
            if board[j+8][0]=="X" or board[j+8+1][0]=="X":
                return False
        return True

    elif cardtype==5:
        if y==8:
            return False
        if not board[j][0]=="X" or not board[j+1][0]=="X":
            return False
        # if isfill==True:
        if not x==1:
            if board[j+8][0]=="X" or board[j+8+1][0]=="X":
                return False
        return True

    elif cardtype==6:
        if y==8:
            return False
        if not board[j][0]=="X" or not board[j+1][0]=="X":
            return False
        # if isfill==True:
        if not x==1:
            if board[j+8][0]=="X" or board[j+8+1][0]=="X":
                return False
        return True

    elif cardtype==7:
        if y==8:
            return False
        if not board[j][0]=="X" or not board[j+1][0]=="X":
            return False
        # if isfill==True:
        if not x==1:
            if board[j+8][0]=="X" or board[j+8+1][0]=="X":
                return False
        return True

    # if current_player=="A":
    #     current_player="B"
    #     bottomlable.config(text="Player B Turn.")
    # else:
    #     current_player="A"
    #     bottomlable.config(text="Player A Turn.")
    # stepcount+=1
    # bottomlable2.config(text="Step: "+str(stepcount-1))
    # check_winning(x,y)

# check where can I put cards
def AI_card_list(board):
    available_list = []
    for x in range(1,13,1):
        for y in range(1,9,1):
            for cardtype in range(0,8,1):
                if AI_check_card(x, y, cardtype,board) == True:
                    available_list.append([x,y,cardtype])
    return available_list

def AI_card_list_after24(board,lastremove):
    available_list = []
    for x in range(1,13,1):
        for y in range(1,9,1):
            for cardtype in range(0,8,1):
                if AI_check_card_after24(x, y, cardtype,board,lastremove) == True:
                    available_list.append([x,y,cardtype])
    return available_list

#alpha belta
# Initial call with alpha=-inf and beta=inf
# minimax(currentlevel == 0, player:computer or oppenent, alpha == -inf, beta == +inf)
# player may be "computer" or "opponent"
# 
# def alpha_beta(level, player, alpha, beta,tmp_board):
#     global xycardtype
#     global en_result
#     score = 0
#     x = -1
#     y = -1
#     cardtype = -1
#     if game_finished==True or level == 3:
#         score = en_result
#         return ([score,x,y,cardtype])
#     else:
#         children = AI_card_list(tmp_board)
#         for i in children:
#             tmp_board2 = minimax_tmpboard(i, tmp_board)
#             if player == "computer":
#                 score = alpha_beta(level + 1, "human", str(alpha), str(beta),tmp_board2)
#                 if str(score) > str(alpha):
#                     alpha = score
#                     # print("asdsdasdasd")
#                     # print(i)
#                     # print(i[0])
#                     # print(i[1])
#                     # print(i[2])
#                     # xycardtype = i
#             elif player == "human":
#                 score = alpha_beta(level + 1, "computer", str(alpha), str(beta),tmp_board2)
#                 if str(score) < str(beta):
#                     beta = score
#                     # xycardtype = i
#
#             # fillboardbefore24andmovecard(xycardtype[0],xycardtype[1],xycardtype[2],True)
#             if str(alpha)>= str(beta):
#                 break
#             xycardtype = i
#         return beta







# AI_main function
# def AI_function():
#     # shuchu deishi xy cardtype
#     minimax();
#     rbvar.set(xycardtype[2])
#     fillboard(xycardtype[0],xycardtype[1])


# heuristics
# def heuristics(list):
#     return randint(0,200)


def informed_heuristics(x,y,cardtype,board):
    informed_result = 0
    count_result = AI_check_winning_result(x,y,board)
    if current_player == "A":
        # False=Color True=Dot
        if playerA_Select==True:
            for i in count_result:
                # count_result = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]  # 黑点,白点,红底,白底 顺序是 竖 横 左下又上 右下左上
                if i[0]== 4 or i[1] == 4:
                    informed_result += 100000
                elif i[2] == 4 or i[3] == 4:
                    informed_result -= 100000
                elif i[0] == 3 or i[1] == 3:
                    informed_result += 1000
                elif i[2] == 3 or i[3] == 3:
                    informed_result -= 1000
                elif i[0] == 2 or i[1] == 2:
                    informed_result += 10
                elif i[2] == 2 or i[3] == 2:
                    informed_result -= 10
                elif i[0] == 1 or i[1] == 1:
                    informed_result += 1
                elif i[2] == 1 or i[3] == 1:
                    informed_result -= 1
            return informed_result
        elif playerA_Select== False:
            for i in count_result:
                # count_result = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]  # 黑点,白点,红底,白底 顺序是 竖 横 左下又上 右下左上
                if i[2]== 4 or i[3] == 4:
                    informed_result += 100000
                elif i[0] == 4 or i[1] == 4:
                    informed_result -= 100000
                elif i[2] == 3 or i[3] == 3:
                    informed_result += 1000
                elif i[0] == 3 or i[1] == 3:
                    informed_result -= 1000
                elif i[2] == 2 or i[3] == 2:
                    informed_result += 10
                elif i[0] == 2 or i[1] == 2:
                    informed_result -= 10
                elif i[2] == 1 or i[3] == 1:
                    informed_result += 1
                elif i[0] == 1 or i[1] == 1:
                    informed_result -= 1
            return informed_result
    elif current_player =="B":
            # False=Color True=Dot
        if playerA_Select == True:
            for i in count_result:
                # count_result = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]  # 黑点,白点,红底,白底 顺序是 竖 横 左下又上 右下左上
                if i[2] == 4 or i[3] == 4:
                    informed_result += 100000
                elif i[0] == 4 or i[1] == 4:
                    informed_result -= 100000
                elif i[2] == 3 or i[3] == 3:
                    informed_result += 1000
                elif i[0] == 3 or i[1] == 3:
                    informed_result -= 1000
                elif i[2] == 2 or i[3] == 2:
                    informed_result += 10
                elif i[0] == 2 or i[1] == 2:
                    informed_result -= 10
                elif i[2] == 1 or i[3] == 1:
                    informed_result += 1
                elif i[0] == 1 or i[1] == 1:
                    informed_result -= 1
            return informed_result

        elif playerA_Select == False:
            for i in count_result:
                if i[0] == 4 or i[1] == 4:
                    informed_result += 100000
                elif i[2] == 4 or i[3] == 4:
                    informed_result -= 100000
                elif i[0] == 3 or i[1] == 3:
                    informed_result += 1000
                elif i[2] == 3 or i[3] == 3:
                    informed_result -= 1000
                elif i[0] == 2 or i[1] == 2:
                    informed_result += 10
                elif i[2] == 2 or i[3] == 2:
                    informed_result -= 10
                elif i[0] == 1 or i[1] == 1:
                    informed_result += 1
                elif i[2] == 1 or i[3] == 1:
                    informed_result -= 1
            return informed_result

def informed_heu2(x,y,cardtype,board):
    en_result = 0
    ax = 12 - x
    ay = y - 1
    j = ax * 8 + ay
    if current_player == "A" or "B":
        print("XXXXXXAAAAA")
        print(board[j])
        # False=Color True=Dot
        if playerA_Select == True:
            if y <= 5:
                if cardtype == board[j+1][3] == board[j+2][3] == board[j+3][3]:
                    en_result += 1000
                    return en_result
                if cardtype == board[j+1][3] == board[j+2][3]:
                    en_result += 100
                    return en_result
                if cardtype == board[j+1][3]:
                    en_result += 10
                    return en_result
            if y >= 4:
                if cardtype == board[j-1][3] == board[j-2][3] == board[j-3][3]:
                    en_result += 1000
                    return en_result
                if cardtype == board[j-1][3] == board[j-2][3]:
                    en_result += 100
                    return en_result
                if cardtype == board[j-1][3]:
                    en_result += 10
                    return en_result
            if x <= 9:
                if cardtype == board[j-8][3] == board[j-16][3] == board[j-24][3]:
                    en_result += 1000
                    return en_result
                if cardtype == board[j-8][3] == board[j-16][3]:
                    en_result += 100
                    return en_result
                if cardtype == board[j-8][3]:
                    en_result += 10
                    return en_result
            if x >= 4:
                if cardtype == board[j+8][3] == board[j+16][3] == board[j+24][3]:
                    en_result += 1000
                    return en_result
                if cardtype == board[j+8][3] == board[j+16][3]:
                    en_result += 100
                    return en_result
                if cardtype == board[j+8][3]:
                    en_result += 10
                    return en_result
    return en_result
 # def heuristics(board):
#     result = 0
#     for x in range(1,13,1):
#         for y in range(1,9,1):
#             ax = 12 - x
#             ay = y - 1
#             j = ax * 8 + ay
#             z = (x-1)*10+y
#             if lablelist[j].cget("text")=="●" and lablelist[j].cget("bg")=="red":
#                 result -= 2*z
#             if lablelist[j].cget("text")=="●" and lablelist[j].cget("bg")=="white":
#                 result += 3*z
#             if lablelist[j].cget("text")=="○" and lablelist[j].cget("bg")=="red":
#                 result -= 1.5*z
#             if lablelist[j].cget("text")=="○" and lablelist[j].cget("bg")=="white":
#                 result += z
#     # print(result)
#     return result

def jianqu_en(x,y,cardtype):
    global en_result
    if cardtype == 0:
        z1 = (x-1)*10 +y
        z2 = x*10 +y
        en_result -= (-2*z1 + z2)
    if cardtype == 1:
        z1 = (x-1)*10 +y
        z2 = x*10 +y
        en_result -= (z1 + -2*z2)
    if cardtype == 2:
        z1 = (x - 1) * 10 + y
        z2 = x * 10 + y
        en_result -= (3*z1 + -1.5*z2)
    if cardtype == 3:
        z1 = (x - 1) * 10 + y
        z2 = x * 10 + y
        en_result -= (-1.5 * z1 + 3 * z2)
    if cardtype == 4:
        z1 = (x - 1) * 10 + y
        z2 = (x - 1) * 10 + y+1
        en_result -= (-2 * z1 + z2)
    if cardtype == 5:
        z1 = (x - 1) * 10 + y
        z2 = (x - 1) * 10 + y+1
        en_result -= (z1 + -2* z2)
    if cardtype == 6:
        z1 = (x - 1) * 10 + y
        z2 = (x - 1) * 10 + y+1
        en_result -= (3 * z1 + -1.5*z2)
    if cardtype == 7:
        z1 = (x - 1) * 10 + y
        z2 = (x - 1) * 10 + y+1
        en_result -= (-1.5 * z1 + 3*z2)
    return en_result



def jia_en(x,y,cardtype):
    global en_result
    if cardtype == 0:
        z1 = (x-1)*10 +y
        z2 = x*10 +y
        en_result += (-2*z1 + z2)
    if cardtype == 1:
        z1 = (x-1)*10 +y
        z2 = x*10 +y
        en_result += (z1 + -2*z2)
    if cardtype == 2:
        z1 = (x - 1) * 10 + y
        z2 = x * 10 + y
        en_result += (3*z1 + -1.5*z2)
    if cardtype == 3:
        z1 = (x - 1) * 10 + y
        z2 = x * 10 + y
        en_result += (-1.5 * z1 + 3 * z2)
    if cardtype == 4:
        z1 = (x - 1) * 10 + y
        z2 = (x - 1) * 10 + y+1
        en_result += (-2 * z1 + z2)
    if cardtype == 5:
        z1 = (x - 1) * 10 + y
        z2 = (x - 1) * 10 + y+1
        en_result += (z1 + -2* z2)
    if cardtype == 6:
        z1 = (x - 1) * 10 + y
        z2 = (x - 1) * 10 + y+1
        en_result += (3 * z1 + -1.5*z2)
    if cardtype == 7:
        z1 = (x - 1) * 10 + y
        z2 = (x - 1) * 10 + y+1
        en_result += (-1.5 * z1 + 3*z2)
    return en_result

# minimax
def minimax_tmpboard(list,tmp_board,currentstep):
    global en_result

    x = list[0]
    y = list[1]
    cardtype = list[2]
    ax = 12 - x
    ay = y - 1
    j = ax * 8 + ay
    if cardtype == 0:
        tmp_board[j] = current_player + "%02d" % (currentstep) + "0"
        tmp_board[j - 8] = current_player + "%02d" % (currentstep) + "0"
    elif cardtype == 1:
        tmp_board[j - 8] = current_player + "%02d" % (currentstep) + "1"
        tmp_board[j] = current_player + "%02d" % (currentstep) + "1"
    elif cardtype == 2:
        tmp_board[j] = current_player + "%02d" % (currentstep) + "2"
        tmp_board[j - 8] = current_player + "%02d" % (currentstep) + "2"
    elif cardtype == 3:
        tmp_board[j - 8] = current_player + "%02d" % (currentstep) + "3"
        tmp_board[j] = current_player + "%02d" % (currentstep) + "3"
    elif cardtype == 4:
        tmp_board[j] = current_player + "%02d" % (currentstep) + "4"
        tmp_board[j + 1] = current_player + "%02d" % (currentstep) + "4"
    elif cardtype == 5:
        tmp_board[j + 1] = current_player + "%02d" % (currentstep) + "5"
        tmp_board[j] = current_player + "%02d" % (currentstep) + "5"
    elif cardtype == 6:
        tmp_board[j] = current_player + "%02d" % (currentstep) + "6"
        tmp_board[j + 1] = current_player + "%02d" % (currentstep) + "6"
    elif cardtype == 7:
        tmp_board[j + 1] = current_player + "%02d" % (currentstep) + "7"
        tmp_board[j] = current_player + "%02d" % (currentstep) + "7"
    return tmp_board


def AI_alphabeta(maxmin,beginlayer,currentlayer,maxlayer,tmp_board,currentstepcount,alpha,beta):
    global en_result
    global hecallcount
    global level2he
    AIlist=AI_card_list(tmp_board)
    if len(AIlist)==0:
        return None
    global xycardtype
    save = []
    for i in tmp_board:
        save.append(i)
    gethe=None
    saveen = en_result
    for i in AIlist:
        tmp_board = []
        for l in save:
            tmp_board.append(l)
        tmp_board = minimax_tmpboard(i, tmp_board, currentstepcount)
        if beginlayer == currentlayer:
            x = i[0]
            y = i[1]
            cardtype = i[2]
            if current_player == "A":
                if AI_check_winning(x,y,cardtype,tmp_board) == "A":
                    # fillboardbefore24andmovecard(x,y,cardtype)
                    xycardtype = i
                    return
            elif current_player == "B":
                if AI_check_winning(x,y,cardtype,tmp_board) == "B":
                    # fillboardbefore24andmovecard(x,y,cardtype)
                    xycardtype = i
                    return
        # jia_en(i[0],i[1],i[2])
        if maxmin == "max":
            if beta<alpha:
                continue
            else:
                if not currentlayer==maxlayer:
                    result=AI_alphabeta("min",beginlayer,currentlayer+1,maxlayer,tmp_board,currentstepcount+1,alpha,beta)
                    if result==None:
                        # he=en_result
                        # hecallcount += 1
                        # if gethe==None:
                        #     if alpha<he:
                        #         alpha=he
                        #         gethe = he
                        #         if currentlayer == beginlayer:
                        #             xycardtype = i
                        # else:
                        #     if gethe<he:
                        #         if alpha < he:
                        #             alpha = he
                        #             gethe = he
                        #             if currentlayer == beginlayer:
                        #                 xycardtype = i
                        continue
                    else:
                        if gethe==None:
                            if alpha<result:
                                alpha=result
                                gethe = result
                                if currentlayer == beginlayer:
                                    xycardtype = i
                        else:
                            if gethe<result:
                                if alpha < result:
                                    alpha = result
                                    gethe = result
                                    if currentlayer == beginlayer:
                                        xycardtype = i
                else:
                    hecallcount += 1
                    x = i[0]
                    y = i[1]
                    cardtype = i[2]
                    he = informed_heuristics(x, y, cardtype, tmp_board)
                    # he = en_result
                    if gethe == None:
                        if alpha < he:
                            alpha = he
                            gethe = he
                            if currentlayer == beginlayer:
                                xycardtype = i
                    else:
                        if gethe < he:
                            if alpha < he:
                                alpha = he
                                gethe = he
                                if currentlayer == beginlayer:
                                    xycardtype = i
        else:
            if beta<alpha:
                continue
            else:
                if not currentlayer==maxlayer:
                    result=AI_alphabeta("max",beginlayer,currentlayer+1,maxlayer,tmp_board,currentstepcount+1,alpha,beta)
                    if result==None:
                        he=en_result
                        hecallcount += 1
                        if gethe==None:
                            if beta>he:
                                beta=he
                                gethe = he
                                if currentlayer == beginlayer:
                                    xycardtype = i
                        else:
                            if gethe>he:
                                if beta > he:
                                    beta = he
                                    gethe = he
                                    if currentlayer == beginlayer:
                                        xycardtype = i
                    else:
                        if gethe==None:
                            if beta>result:
                                beta=result
                                gethe = result
                                if currentlayer == beginlayer:
                                    xycardtype = i
                        else:
                            if gethe>result:
                                if beta > result:
                                    beta = result
                                    gethe = result
                                    if currentlayer == beginlayer:
                                        xycardtype = i
                else:
                    # he = en_result
                    x = i[0]
                    y = i[1]
                    cardtype = i[2]
                    he = informed_heuristics(x, y, cardtype, tmp_board)
                    hecallcount += 1
                    if gethe == None:
                        if beta > he:
                            beta = he
                            gethe = he
                            if currentlayer == beginlayer:
                                xycardtype = i
                    else:
                        if gethe > he:
                            if beta > he:
                                beta = he
                                gethe = he
                                if currentlayer == beginlayer:
                                    xycardtype = i
        en_result=saveen
    # print("%d : Alpha %f, Beta %f, Heristic "%(currentlayer,alpha,beta)+str(gethe)+".")
    if currentlayer==beginlayer:
        en_result=saveen
    if currentlayer==1:
        level2he.append(gethe)
    return gethe

def AI_alphabetaafter24(maxmin,beginlayer,currentlayer,maxlayer,tmp_board,currentstepcount,alpha,beta):
    global removecard
    global placecard
    global en_result
    global hecallcount
    global level2he
    save = []
    saveen = en_result
    for i in tmp_board:
        save.append(i)
    AIremovelist = AI_removecardlist(tmp_board, currentstepcount)
    if len(AIremovelist) == 0:
        return None
    tophe = None
    for i in AIremovelist:
        jianqu_en(i[0],i[1],i[2])
        tmp_board = []
        for l in save:
            tmp_board.append(l)
        tmp_board = AI_remove_card(i[0], i[1], tmp_board)[0]
        AIplacelist = AI_card_list_after24(tmp_board, i)
        gethe = None
        saveplacecard=None
        saveen2 = en_result
        for j in AIplacelist:
            jia_en(j[0],j[1],j[2])
            tmp_board2 = []
            for l in tmp_board:
                tmp_board2.append(l)
            tmp_board2 = minimax_tmpboard(j, tmp_board2, currentstepcount)
            if beginlayer == currentlayer:
                x = j[0]
                y = j[1]
                cardtype = j[2]
                if current_player == "A":
                    if AI_check_winning(x, y, cardtype, tmp_board2) == "A":
                        # fillboardbefore24andmovecard(x,y,cardtype)
                        removecard = i
                        placecard = j
                        return
                elif current_player == "B":
                    if AI_check_winning(x, y, cardtype, tmp_board2) == "B":
                        # fillboardbefore24andmovecard(x,y,cardtype)
                        removecard = i
                        placecard = j
                        return
            if maxmin == "max":
                if beta < alpha:
                    continue
                else:
                    if not currentlayer == maxlayer:
                        result = AI_alphabetaafter24("min", beginlayer, currentlayer + 1, maxlayer, tmp_board2,
                                              currentstepcount + 1, alpha, beta)
                        if result == None:
                            # hecallcount += 1
                            # he = en_result
                            # if gethe == None:
                            #     if alpha < he:
                            #         alpha = he
                            #         gethe = he
                            #         if currentlayer == beginlayer:
                            #             saveplacecard=j
                            # else:
                            #     if gethe < he:
                            #         if alpha < he:
                            #             alpha = he
                            #             gethe = he
                            #             if currentlayer == beginlayer:
                            #                 saveplacecard = j
                            continue
                        else:
                            if gethe == None:
                                if alpha < result:
                                    alpha = result
                                    gethe = result
                                    if currentlayer == beginlayer:
                                        saveplacecard = j
                            else:
                                if gethe < result:
                                    if alpha < result:
                                        alpha = result
                                        gethe = result
                                        if currentlayer == beginlayer:
                                            saveplacecard = j
                    else:
                        hecallcount += 1
                        he = en_result
                        if gethe == None:
                            if alpha < he:
                                alpha = he
                                gethe = he
                                if currentlayer == beginlayer:
                                    saveplacecard = j
                        else:
                            if gethe < he:
                                if alpha < he:
                                    alpha = he
                                    gethe = he
                                    if currentlayer == beginlayer:
                                        saveplacecard = j
            else:
                if beta < alpha:
                    continue
                else:
                    if not currentlayer == maxlayer:
                        result = AI_alphabetaafter24("max", beginlayer, currentlayer + 1, maxlayer, tmp_board2,
                                              currentstepcount + 1, alpha, beta)
                        if result == None:
                            hecallcount += 1
                            he = en_result
                            if gethe == None:
                                if beta > he:
                                    beta = he
                                    gethe = he
                                    if currentlayer == beginlayer:
                                        saveplacecard = j
                            else:
                                if gethe > he:
                                    if beta > he:
                                        beta = he
                                        gethe = he
                                        if currentlayer == beginlayer:
                                            saveplacecard = j
                        else:
                            if gethe == None:
                                if beta > result:
                                    beta = result
                                    gethe = result
                                    if currentlayer == beginlayer:
                                        saveplacecard = j
                            else:
                                if gethe > result:
                                    if beta > result:
                                        beta = result
                                        gethe = result
                                        if currentlayer == beginlayer:
                                            saveplacecard = j
                    else:
                        hecallcount += 1
                        he = en_result
                        if gethe == None:
                            if beta > he:
                                beta = he
                                gethe = he
                                if currentlayer == beginlayer:
                                    saveplacecard = j
                        else:
                            if gethe > he:
                                if beta > he:
                                    beta = he
                                    gethe = he
                                    if currentlayer == beginlayer:
                                        saveplacecard = j
            en_result=saveen2
        if gethe==None:
            continue
        if tophe==None:
            tophe=gethe
            if maxmin=="max":
                alpha=gethe
            else:
                beta=gethe
            if currentlayer == beginlayer:
                placecard = saveplacecard
                removecard = i
        if maxmin=="max":
            if tophe<gethe:
                tophe=gethe
                alpha=gethe
                if currentlayer==beginlayer:
                    placecard=saveplacecard
                    removecard=i
        else:
            if tophe>gethe:
                tophe=gethe
                beta=gethe
                if currentlayer==beginlayer:
                    placecard=saveplacecard
                    removecard=i
        en_result = saveen
    # print("%d : Alpha %f, Beta %f, Heristic " % (currentlayer, alpha, beta) + str(gethe) + ".")
    if currentlayer == 1:
        level2he.append(tophe)
    return tophe


'''
def AI_alphabetaafter24(maxmin,beginlayer,currentlayer,maxlayer,tmp_board,currentstepcount,alpha,beta):
    global removecard
    global placecard
    save = []
    for i in tmp_board:
        save.append(i)
    AIremovelist = AI_removecardlist(tmp_board, currentstepcount)
    if len(AIremovelist) == 0:
        return None
    tophe = None
    for i in AIremovelist:
        tmp_board = []
        for l in save:
            tmp_board.append(l)
        tmp_board = AI_remove_card(i[0], i[1], tmp_board)[0]
        AIplacelist = AI_card_list_after24(tmp_board, i)
        gethe = None
        for j in AIplacelist:
            tmp_board2 = []
            for l in tmp_board:
                tmp_board2.append(l)
            tmp_board2 = minimax_tmpboard(j, tmp_board2, currentstepcount)
            if maxmin == "max":
                if beta < alpha:
                    continue
                else:
                    if not currentlayer == maxlayer:
                        result=AI_alphabetaafter24("min",beginlayer,currentlayer+1,maxlayer,tmp_board2,currentstepcount+1,alpha,beta)
                        if result==None:
                            he = heuristics(i)
                            if gethe==None:
                                if alpha<he:
                                    alpha=he
                                    gethe=he
                                    if currentlayer == beginlayer:
                                        placecard=j
                            else:
                                if gethe<he:
                                    if alpha<he:
                                        alpha=he
                                        gethe=he
                                        if currentlayer == beginlayer:
                                            placecard=j
                        else:
                            if gethe==None:
                                if alpha<result:
                                    alpha=result
                                    gethe=result
                                    if currentlayer == beginlayer:
                                        placecard=j
                            else:
                                if gethe<result:
                                    if alpha<result:
                                        alpha=result
                                        gethe=result
                                        if currentlayer == beginlayer:
                                            placecard=j
                    else:
                        he = heuristics(i)
                        if gethe == None:
                            if alpha < he:
                                alpha = he
                                gethe = he
                                if currentlayer == beginlayer:
                                    placecard = j
                        else:
                            if gethe < he:
                                if alpha < he:
                                    alpha = he
                                    gethe = he
                                    if currentlayer == beginlayer:
                                        placecard = j
            else:
                if beta < alpha:
                    continue
                else:
                    if not currentlayer == maxlayer:
                        result=AI_alphabetaafter24("max",beginlayer,currentlayer+1,maxlayer,tmp_board2,currentstepcount+1,alpha,beta)
                        if result==None:
                            he = heuristics(i)
                            if gethe==None:
                                if beta>he:
                                    beta=he
                                    gethe=he
                                    if currentlayer == beginlayer:
                                        placecard=j
                            else:
                                if gethe>he:
                                    if beta>he:
                                        beta=he
                                        gethe=he
                                        if currentlayer == beginlayer:
                                            placecard=j
                        else:
                            if gethe==None:
                                if beta>result:
                                    beta=result
                                    gethe=result
                                    if currentlayer == beginlayer:
                                        placecard=j
                            else:
                                if gethe>result:
                                    if beta>result:
                                        beta=result
                                        gethe=result
                                        if currentlayer == beginlayer:
                                            placecard=j
                    else:
                        he = heuristics(i)
                        if gethe == None:
                            if beta > he:
                                beta = he
                                gethe = he
                                if currentlayer == beginlayer:
                                    placecard = j
                        else:
                            if gethe > he:
                                if beta> he:
                                    beta = he
                                    gethe = he
                                    if currentlayer == beginlayer:
                                        placecard = j
            if currentlayer==beginlayer:
                if tophe==None:
                    tophe=gethe
                    removecard=i
                else:
                    if gethe==None:
                        continue
                    if maxmin=="max":
                        if tophe<gethe:
                            if alpha<gethe:
                                alpha=gethe
                                tophe=gethe
                                removecard=i
                        else:
                            if beta>gethe:
                                beta=gethe
                                tophe=gethe
                                removecard=i
                    else:
                        if tophe>gethe:
                            if alpha>gethe:
                                alpha=gethe
                                tophe=gethe
                                removecard=i
                        else:
                            if beta<gethe:
                                beta=gethe
                                tophe=gethe
                                removecard=i
    print("%d : Alpha %f, Beta %f, Heristic " % (currentlayer, alpha, beta) + str(gethe) + ".")
    return tophe
'''

def minimax(maxmin,beginlayer,currentlayer,maxlayer,tmp_board,currentstepcount):
    global hecallcount
    global level2he
    helist=[]
    AIlist=AI_card_list(tmp_board)
    if len(AIlist)==0:
        return None
    global xycardtype
    global en_result
    save=[]
    for i in tmp_board:
        save.append(i)
    saveen = en_result
    for i in AIlist:
        tmp_board=[]
        for l in save:
            tmp_board.append(l)
        jia_en(i[0],i[1],i[2])
        tmp_board=minimax_tmpboard(i,tmp_board,currentstepcount)
        if beginlayer == currentlayer:
            x = i[0]
            y = i[1]
            cardtype = i[2]
            if current_player == "A":
                if AI_check_winning(x,y,cardtype,tmp_board) == "A":
                    # fillboardbefore24andmovecard(x,y,cardtype)
                    xycardtype = i
                    return
            elif current_player == "B":
                if AI_check_winning(x,y,cardtype,tmp_board) == "B":
                    # fillboardbefore24andmovecard(x,y,cardtype)
                    xycardtype = i
                    return
        if maxmin=="max":
            if not currentlayer == maxlayer:
                result = minimax("min",beginlayer, currentlayer + 1, maxlayer, tmp_board, currentstepcount+1)
                if result==None:
                    # hecallcount+=1
                    # helist.append(en_result)
                    # x = i[0]
                    # y = i[1]
                    # cardtype = i[2]
                    # helist.append(informed_heuristics(x,y,cardtype,tmp_board))
                    continue
                else:
                    helist.append(result)

                    # helist.append(en_result)
            else:
                hecallcount += 1
                # helist.append(en_result)
                x = i[0]
                y = i[1]
                cardtype = i[2]
                helist.append(informed_heuristics(x, y, cardtype, tmp_board))
        else:
            if not currentlayer==maxlayer:
                result = minimax("max",beginlayer, currentlayer + 1, maxlayer, tmp_board, currentstepcount+1)
                if result==None:
                    # hecallcount += 1
                    # helist.append(en_result)
                    # x = i[0]
                    # y = i[1]
                    # cardtype = i[2]
                    # helist.append(informed_heuristics(x, y, cardtype, tmp_board))
                    continue
                else:
                    helist.append(result)
                    # helist.append(en_result)
            else:
                hecallcount += 1
                # helist.append(en_result)
                x = i[0]
                y = i[1]
                cardtype = i[2]
                helist.append(informed_heuristics(x, y, cardtype, tmp_board))
        # en_result = saveen
    if maxmin=="max":
        if beginlayer == currentlayer:
            for i in range(0, len(helist), 1):
                if helist[i] == max(helist):
                    xycardtype = AIlist[i]
                    break
        # print(helist)
        if currentlayer == beginlayer:
            en_result = saveen
        if currentlayer ==1 :
            level2he.append(max(helist))
        return max(helist)
    else:
        if beginlayer == currentlayer:
            for i in range(0, len(helist), 1):
                if helist[i] == min(helist):
                    xycardtype = AIlist[i]
                    break
        # print(helist)
        if currentlayer == beginlayer:
            en_result = saveen
        if currentlayer == 1:
            level2he.append(min(helist))
        return min(helist)

def canclelist(tmp_board):
    tmp_board2 = []
    for i in tmp_board:
        tmp_board2.append(i)
    list = []
    for x in range(1,12,1):
        for y in range(1,9,1):
            ax = 12 - x
            ay = y - 1
            j = ax * 8 + ay
            if tmp_board[j][0]=="X":
                continue
            result=AI_can_cancle_step(x,y,tmp_board2)
            if not result==None:
                cardtype = board[j][3]
                tmp_board2=result
                list.append([x,y,cardtype])
    return list


def AI_removecardlist(tmp_board,laststep):
    copytmp_board=[]
    for i in tmp_board:
        copytmp_board.append(i)
    remove_list=[]
    for x in range(1,13,1):
        for y in range(1,9,1):
            if AIafter24checkremoveable(x,y,copytmp_board,laststep):
                ax = 12 - x
                ay = y - 1
                j = ax * 8 + ay
                cardtype=int(tmp_board[j][3])
                remove_list.append([x,y,cardtype])
                if cardtype==0 or cardtype==1 or cardtype==2 or cardtype==3:
                    tmp_board[j]="X000"
                    tmp_board[j-8]="X000"
                else:
                    tmp_board[j]="X000"
                    tmp_board[j+1]="X000"
    return remove_list

removecard=None
placecard=None

def minimaxafter24(maxmin,beginlayer,currentlayer,maxlayer,tmp_board,currentstepcount):
    global hecallcount
    global removecard
    global placecard
    global en_result
    global level2he
    save=[]
    removehelist=[]
    rplist=[]
    saveen = en_result
    for i in tmp_board:
        save.append(i)
    AIremovelist=AI_removecardlist(tmp_board,currentstepcount)
    if len(AIremovelist)==0:
        return None
    for i in AIremovelist:
        jianqu_en(i[0],i[1],i[2])
        tmp_board=[]
        for l in save:
            tmp_board.append(l)
        tmp_board=AI_remove_card(i[0],i[1],tmp_board)[0]
        AIplacelist=AI_card_list_after24(tmp_board,i)
        saveplacecard=None
        helist=[]
        saveen2=en_result
        for j in AIplacelist:
            tmp_board2 = []
            for l in tmp_board:
                tmp_board2.append(l)
            jia_en(j[0],j[1],j[2])
            tmp_board2 = minimax_tmpboard(j, tmp_board2, currentstepcount)
            if beginlayer == currentlayer:
                x = j[0]
                y = j[1]
                cardtype = j[2]
                if current_player == "A":
                    if AI_check_winning(x, y, cardtype, tmp_board2) == "A":
                        # fillboardbefore24andmovecard(x,y,cardtype)
                        # print("xxxxx")
                        # print(removecard)
                        # print("ssss")
                        # print(placecard)
                        removecard = i
                        placecard = j
                        return
                elif current_player == "B":
                    if AI_check_winning(x, y, cardtype, tmp_board2) == "B":
                        # fillboardbefore24andmovecard(x,y,cardtype)
                        removecard = i
                        placecard = j
                        return
            if maxmin == "max":
                if not currentlayer == maxlayer:
                    result=minimaxafter24("min",beginlayer,currentlayer+1,maxlayer,tmp_board2,currentstepcount+1)
                    if result==None:
                        hecallcount += 1
                        helist.append(en_result)
                        continue
                    else:
                        helist.append(result)
                else:
                    hecallcount += 1
                    helist.append(en_result)
            else:
                if not currentlayer == maxlayer:
                    result=minimaxafter24("max",beginlayer,currentlayer+1,maxlayer,tmp_board2,currentstepcount+1)
                    if result == None:
                        hecallcount += 1
                        helist.append(en_result)
                        continue
                    else:
                        helist.append(result)
                else:
                    hecallcount += 1
                    helist.append(en_result)
            en_result=saveen2
        if maxmin=="max":
            removehelist.append(max(helist))
            if currentlayer==beginlayer:
                for l in range(0,len(helist),1):
                    if helist[l]==max(helist):
                        rplist.append(AIplacelist[l])
                        break
        else:
            removehelist.append(min(helist))
            if currentlayer==beginlayer:
                for l in range(0,len(helist),1):
                    if helist[l]==min(helist):
                        rplist.append(AIplacelist[l])
                        break
        en_result=saveen
    if currentlayer == beginlayer:
        en_result=saveen
    if maxmin == "max":
        if currentlayer == beginlayer:
            for l in range(0, len(removehelist), 1):
                if removehelist[l] == max(removehelist):
                    removecard=AIremovelist[l]
                    placecard=rplist[l]
        if currentlayer == 1:
            level2he.append(max(removehelist))
        return max(removehelist)
    else:
        if currentlayer == beginlayer:
            for l in range(0, len(removehelist), 1):
                if removehelist[l] == min(removehelist):
                    removecard=AIremovelist[l]
                    placecard=rplist[l]
        if currentlayer == 1:
            level2he.append(min(removehelist))
        return min(removehelist)





for i in range(0,12,1):
    lable=Tk.Label(frame,bg="white",text=str(i+1),width=5,height=2)
    lable.grid(row=11-i,column=0)
    for k in range(1,9,1):
        lable=Tk.Label(frame,bg="grey",text="",width=5,height=2,borderwidth=2,relief="groove")
        lable.grid(row=i,column=k)
        lable.bind("<Button-1>",lambda event,x=12-i,y=k:fillboard(x,y))
        lablelist.append(lable)
        board.append("X000")

# 最下面A-H
lable=Tk.Label(frame,bg="white",text="",width=5,height=2)
lable.grid(row=13,column=0)
for i in range(1,9,1):
    lable=Tk.Label(frame,bg="white",text=lookup[i-1],width=5,height=2)
    lable.grid(row=13,column=i)

# 保存radio button 选的那个
rbvar=Tk.IntVar()

# draw the first row cards
lable=Tk.Label(frame,bg="white",text="○",width=5,height=2,borderwidth=2,relief="groove")
lable.grid(row=14,column=0)
lable=Tk.Label(frame,bg="white",text="4")
lable.grid(row=16,column=0)
radiobutton=Tk.Radiobutton(frame,variable=rbvar,value=0)
radiobutton.grid(row=15,column=1)
lable=Tk.Label(frame,text="●",bg="red",width=5,height=2,borderwidth=2,relief="groove")
lable.grid(row=14,column=3)
lable=Tk.Label(frame,bg="white",text="2")
lable.grid(row=16,column=3)
radiobutton=Tk.Radiobutton(frame,variable=rbvar,value=1)
radiobutton.grid(row=15,column=4)
lable=Tk.Label(frame,text="○",bg="red",width=5,height=2,borderwidth=2,relief="groove")
lable.grid(row=14,column=6)
lable=Tk.Label(frame,bg="white",text="6")
lable.grid(row=16,column=6)
radiobutton=Tk.Radiobutton(frame,variable=rbvar,value=2)
radiobutton.grid(row=15,column=7)
lable=Tk.Label(frame,bg="white",text="●",width=5,height=2,borderwidth=2,relief="groove")
lable.grid(row=14,column=9)
lable=Tk.Label(frame,bg="white",text="8")
lable.grid(row=16,column=9)
radiobutton=Tk.Radiobutton(frame,variable=rbvar,value=3)
radiobutton.grid(row=15,column=10)
lable=Tk.Label(frame,text="●",bg="red",width=5,height=2,borderwidth=2,relief="groove")
lable.grid(row=15,column=0)
lable=Tk.Label(frame,bg="white",text="○",width=5,height=2,borderwidth=2,relief="groove")
lable.grid(row=15,column=3)
lable=Tk.Label(frame,bg="white",text="●",width=5,height=2,borderwidth=2,relief="groove")
lable.grid(row=15,column=6)
lable=Tk.Label(frame,text="○",bg="red",width=5,height=2,borderwidth=2,relief="groove")
lable.grid(row=15,column=9)

# 16行分开 空白
lable=Tk.Label(frame,text="")
lable.grid(row=18,column=0)
# draw the second row cards
lable=Tk.Label(frame,text="●",bg="red",width=5,height=2,borderwidth=2,relief="groove")
lable.grid(row=18,column=0)
lable=Tk.Label(frame,bg="white",text="○",width=5,height=2,borderwidth=2,relief="groove")
lable.grid(row=18,column=1)
lable=Tk.Label(frame,bg="white",text="1")
lable.grid(row=19,column=0)
radiobutton=Tk.Radiobutton(frame,variable=rbvar,value=4)
radiobutton.grid(row=18,column=2)
lable=Tk.Label(frame,bg="white",text="○",width=5,height=2,borderwidth=2,relief="groove")
lable.grid(row=18,column=3)
lable=Tk.Label(frame,text="●",bg="red",width=5,height=2,borderwidth=2,relief="groove")
lable.grid(row=18,column=4)
lable=Tk.Label(frame,bg="white",text="3")
lable.grid(row=19,column=3)
radiobutton=Tk.Radiobutton(frame,variable=rbvar,value=5)
radiobutton.grid(row=18,column=5)
lable=Tk.Label(frame,bg="white",text="●",width=5,height=2,borderwidth=2,relief="groove")
lable.grid(row=18,column=6)
lable=Tk.Label(frame,text="○",bg="red",width=5,height=2,borderwidth=2,relief="groove")
lable.grid(row=18,column=7)
lable=Tk.Label(frame,bg="white",text="7")
lable.grid(row=19,column=6)
radiobutton=Tk.Radiobutton(frame,variable=rbvar,value=6)
radiobutton.grid(row=18,column=8)
lable=Tk.Label(frame,text="○",bg="red",width=5,height=2,borderwidth=2,relief="groove")
lable.grid(row=18,column=9)
lable=Tk.Label(frame,bg="white",text="●",width=5,height=2,borderwidth=2,relief="groove")
lable.grid(row=18,column=10)
lable=Tk.Label(frame,bg="white",text="5")
lable.grid(row=19,column=9)
radiobutton=Tk.Radiobutton(frame,variable=rbvar,value=7)
radiobutton.grid(row=18,column=11)
lable=Tk.Label(frame,text="")
lable.grid(row=20,column=0)
bottomlable=Tk.Label(frame,text="Player A Turn.")
bottomlable.grid(row=21,column=0,columnspan=4,sticky="W")
bottomlable2=Tk.Label(frame, text="Step: ")
bottomlable2.grid(row=21,column=6,columnspan=4,sticky="W")



# 主窗口隐藏
frame.withdraw()
# 选择玩啥的窗口

select=Tk.Toplevel()
select.protocol('WM_DELETE_WINDOW', selectexit)

# 小窗口的定义1
lable=Tk.Label(select,text="Player A: ")
lable.grid(row=0,column=0)
selrbvar=Tk.IntVar()
padradiobutton=Tk.Radiobutton(select,text="Dot",variable=selrbvar,value=0)
padradiobutton.grid(row=0,column=6,sticky='w')
pacradiobutton=Tk.Radiobutton(select,text="Color",variable=selrbvar,value=1)
pacradiobutton.grid(row=0,column=8,sticky='w')

lable=Tk.Label(select,text="AI: ")
lable.grid(row=2,column=0)
var1 = Tk.IntVar()
check = Tk.Checkbutton(select,text= "yes",variable=var1)
check.grid(row=2,column=3,sticky='w')
selrbvar2=Tk.IntVar()
padradiobutton=Tk.Radiobutton(select,text="Player1",variable=selrbvar2,value=0)
padradiobutton.grid(row=2,column=6,sticky='w')
pacradiobutton=Tk.Radiobutton(select,text="Player2",variable=selrbvar2,value=1)
pacradiobutton.grid(row=2,column=8,sticky='w')

selrbvar3=Tk.IntVar()
padradiobutton=Tk.Radiobutton(select,text="Minimax",variable=selrbvar3,value=0)
padradiobutton.grid(row=3,column=6,sticky='w')
pacradiobutton=Tk.Radiobutton(select,text="AlphaBeta",variable=selrbvar3,value=1)
pacradiobutton.grid(row=3,column=8,sticky='w')

selectbutton=Tk.Button(select,text="Start Game", command=gamestart)
selectbutton.grid(row=11,column=6,sticky='w')

lable=Tk.Label(select,text="trace mode: ")
lable.grid(row=8,column=0)
var2 = Tk.IntVar()
check = Tk.Checkbutton(select,text= "yes",variable=var2)
check.grid(row=8,column=3,sticky='w')

# board = []
# for a in range(1,13,1):
#     for b in range(1,9,1):
#         board.append("X000")

# fillboardbefore24andmovecard(1,1,5,True)
# fillboardbefore24andmovecard(1,5,5,True)
# fillboardbefore24andmovecard(2,5,5,True)
# fillboardbefore24andmovecard(1,3,3,True)
# fillboardbefore24andmovecard(1,4,3,True)
# fillboardbefore24andmovecard(2,1,7,True)
# fillboardbefore24andmovecard(3,3,0,True)
# fillboardbefore24andmovecard(3,4,0,True)
# fillboardbefore24andmovecard(3,5,4,True)
# pass one
# fillboardbefore24andmovecard(1,1,5,True)
# fillboardbefore24andmovecard(1,5,5,True)
# fillboardbefore24andmovecard(2,5,4,True)
# fillboardbefore24andmovecard(1,3,3,True)
# fillboardbefore24andmovecard(1,4,3,True)
# fillboardbefore24andmovecard(2,1,7,True)
# fillboardbefore24andmovecard(3,3,0,True)
# fillboardbefore24andmovecard(3,4,0,True)
# fillboardbefore24andmovecard(3,1,1,True)
# pass two


#
# print(board)
# heuristics(board)
# ax = 12 - 2
# j = ax * 8 + ay
# board[j]="A010"
# minimaxafter24("min",0,0,3,board)
# print(xycardtype)



frame.mainloop()

