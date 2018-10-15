import random
import time
import numpy as np

COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0
random.seed(0)
# need a dictionary to story every pattern and their grade, 检查的时候记得需要反过来还要查一遍
five_connected = "ooooo"                #50000
live_four = "_oooo_"                    #4320
flush_four1 = "oooo_"                   #720
flush_four2 = "ooo_o"                   #720
flush_four3 = "oo_oo"                   #720
connected_three = "__ooo_"              #720
jump_three = "_oo_o_"                   #720
live_two1 = "__oo__"                    #120
live_two2 = "__o_o_"                    #120
live_one = "___o__"                     #20
string_patternList = [five_connected, live_four, flush_four1, flush_four2, flush_four3, connected_three, jump_three, live_two1, live_two2, live_one]
score_patternList = [50000, 4320, 720, 720, 720, 720, 720, 120, 120, 20]


# don't change the class name
class AI(object):
    # chessboard_size, color, time_out passed from agent
    def __init__(self, chessboard_size, color, time_out):
        self.chessboard_size = chessboard_size # (15)
        # You are white or black, my color
        self.color = color
        #the max time you should use, your algorithm's run time must not exceed the time limit.
        self.time_out = time_out
        # You need add your decision into your candidate_list. System will get the end of your
        # candidate_list as your decision. It represent only a list (X_location, Y_location).
        self.candidate_list = []


    # The input is current chessboard.
    def go(self, chessboard):
        # Clear candidate_list
        self.candidate_list.clear()
        print("color = " + str(self.color))
        # ==================================================================
        # Write your algorithm here

        # First judge if you are the first
        if not chessboard.any():
            print("it is a kind of empty chessboard")
            # the first step better in the area of "four point of chessboard"
            f_step_x = random.randint(4, 11)
            f_step_y = random.randint(4, 11)
            new_pos = (f_step_x, f_step_y)
            # print("new_pos" + str(new_pos))
        else:
            # get the location of all chess represented as (x,y)
            idx = np.where(chessboard != COLOR_NONE)
            idx = list(zip(idx[0], idx[1]))
            print("idx=" + str(idx))

            # search the blank piece and return list
            blankPiece_list = self.__get_search_blankPiece(idx)
            # print("blankPiece_list" + str(blankPiece_list))
            my_scoreList = self.__get_blankP_score(chessboard, self.color, blankPiece_list)         # 获取到我方的空位分数
            enemy_color = self.color * -1
            enemy_scoreList = self.__get_blankP_score(chessboard, enemy_color, blankPiece_list)     # 获取到对方的空位分数
            # print("my_scoreList=" + str(my_scoreList))
            # print("enemy_scoreList="+str(enemy_scoreList))
            # my_eval = self.__get_list_sum(my_scoreList)                                             # 获取我的分数总和
            # enemy_eval = self.__get_list_sum(enemy_scoreList)                                       # 获取对方的分数总和
            # print("my_eval="+ str(my_eval))
            # print("enemy_eval=" + str(enemy_eval))
            combine_scoreList = self.__combine_list(my_scoreList, enemy_scoreList)
            # print("combine_scoreList" + str(combine_scoreList))
            blankPiece_index = self.__descend_sort(combine_scoreList)[0][0]                         # 只取第一个tuple的第一个数值，第一个tuple是最大的，第一个tuple的第一个数值是index

            # try:
            #     print("I have get try try try try")
            #     attack_defensive_state = my_eval / enemy_eval
            # except ZeroDivisionError:
            #     attack_defensive_state = 2
            # print("I have go here")

            # if attack_defensive_state >= 1:
            #     # attack
            #     blankPiece_index = self.__descend_sort(my_scoreList)[0][0]
            # else:
            #     # defensive
            #     blankPiece_index = self.__descend_sort(enemy_scoreList)[0][0]

            new_pos = blankPiece_list[blankPiece_index]


        # Make sure that the position of your decision in chess board is empty.
        # If not, return error.
        assert chessboard[new_pos[0],new_pos[1]]== COLOR_NONE

        #Add your decision into candidate_list, Records the chess board
        self.candidate_list.append(new_pos)
        print("self.candidate_list:" + str(self.candidate_list))


    # 得到每一个空位在理论图样上的分值并放置到一个list里面后返回
    def __get_blankP_score(self, chessboard, color, blankPiece_list):
        blankP_score_list = []
        # 对于每一个空位，我们计算四个方向上的位子
        for blankP in blankPiece_list:                          # blankP is tuple
            x = blankP[0]                                       # 某一个空位的x坐标
            y = blankP[1]                                       # 某一个空位的y坐标
            # horizontal part
            horizontal_string = self.__get_horizontal_pattern(chessboard, color, x, y)
            vertical_string = self.__get_vertical_pattern(chessboard, color, x, y)
            leftd_string = self.__get_leftdiagonally_pattern(chessboard, color, x, y)
            rightd_string = self.__get_rightdiagonally_pattern(chessboard, color, x, y)
            # print("horizontal_string = " + str(horizontal_string))
            # print("vertical_string = " + str(vertical_string))

            # 然后再分别计算四个方向位置的分值
            horizontal_score = self.__earn_value(horizontal_string)
            vertical_score = self.__earn_value(vertical_string)
            leftd_score = self.__earn_value(leftd_string)
            rightd_score = self.__earn_value(rightd_string)
            # print("horizontal_score" + str(horizontal_score))
            # print("vertical_score" + str(vertical_score))

            # 加在一起
            blankP_score = horizontal_score + vertical_score + leftd_score + rightd_score
            blankP_score_list.append(blankP_score)
        return blankP_score_list

    # check the red line, search range || return a list contain all blank piece within the range
    def __get_search_blankPiece(self, idx):
        _blankPiece_list = []
        # find all "available blank piece" of every piece that have already been played
        for i in idx:
            root_x = i[0]
            root_y = i[1]
            for x in range(root_x-2, root_x+3):
                for y in range(root_y-2, root_y+3):
                    if x<0 or y<0 or x>14 or y>14:                              # any one little than zero will fail
                        continue
                    if (x,y) in _blankPiece_list:
                        continue
                    if (x,y) in idx:
                        continue
                    _blankPiece_list.append((x,y))
        return _blankPiece_list

    # Evaluation function only calculate the score of an empty piece, Pattern matching
    def __earn_value(self, pattern):                  # pattern is a String
        score = 0
        for p, s in zip(string_patternList, score_patternList):
            reverse_p = p[::-1]
            if p in pattern:               # some string or its reverse
                score = s
                break
            elif reverse_p in pattern:
                score = s
                break
        return score

    # 计算一个数字列表的总和
    def __get_list_sum(self, list):
        sum = 0
        for l in list:
            sum = sum + l
        return sum

    # 降序排列list并得到其index
    def __descend_sort(self, list):
        return sorted(enumerate(list), key=lambda x:x[1], reverse=True)

    # 组合两个list的对应值得到新的list
    def __combine_list(self, list1, list2):
        sum = []
        for l1, l2 in zip(list1, list2):
            sum.append(l1+l2)
        return sum

    # 获取到水平方向上的图样
    def __get_horizontal_pattern(self, chessboard, color, x, y):
        horizontal_string = 'o'
        for i in range(1, 5):                               # 先往左侧的4个空位
            yle = y - i
            if yle < 0:
                break
            else:  # 右侧还有棋位的情况
                piece_value_left = chessboard[x][yle]
                if piece_value_left == color:
                    horizontal_string = 'o' + horizontal_string
                elif piece_value_left == 0:
                    horizontal_string = '_' + horizontal_string
                else:
                    horizontal_string = 'x' + horizontal_string
                    break

        for i in range(1, 5):                               # 然后往右侧的4个空位
            yre = y + i
            if yre > 14:
                break
            else:
                piece_value_right = chessboard[x][yre]
                if piece_value_right == color:
                    horizontal_string = horizontal_string + 'o'
                elif piece_value_right == 0:
                    horizontal_string = horizontal_string + '_'
                else:
                    horizontal_string = horizontal_string + 'x'
                    break
        return horizontal_string

    # 获取到垂直方向上的图样
    def __get_vertical_pattern(self, chessboard, color, x, y):
        vertical_string = 'o'
        for i in range(1, 5):                               # 先往上面的4个空位
            xupe = x - i
            if xupe < 0:
                break
            else:
                piece_value_up = chessboard[xupe][y]
                if piece_value_up == color:
                    vertical_string = 'o' + vertical_string
                elif piece_value_up == 0:
                    vertical_string = '_' + vertical_string
                else:
                    vertical_string = 'x' + vertical_string
                    break

        for i in range(1, 5):                               # 然后往下面的4个空位
            xdowne = x + i
            if xdowne > 14:
                break
            else:
                piece_value_down = chessboard[xdowne][y]
                if piece_value_down == color:
                    vertical_string = vertical_string + 'o'
                elif piece_value_down == 0:
                    vertical_string = vertical_string + '_'
                else:
                    vertical_string = vertical_string + 'x'
                    break
        return vertical_string

    # 获取到左斜下对角方向上的图样
    def __get_leftdiagonally_pattern(self, chessboard, color, x, y):
        leftd_string = 'o'
        for i in range(1, 5):                               # 先往斜左下角的4个空位
            xlde = x + i
            ylde = y - i
            if xlde > 14 or ylde < 0:
                break
            else:
                piece_value_leftdown = chessboard[xlde][ylde]
                if piece_value_leftdown == color:
                    leftd_string = 'o' + leftd_string
                elif piece_value_leftdown == 0:
                    leftd_string = '_' + leftd_string
                else:
                    leftd_string = 'x' + leftd_string
                    break

        for i in range(1, 5):                               # 然后往斜右上角的4个空位
            xlde = x - i
            ylde = y + i
            if xlde < 0 or ylde > 14:
                break
            else:
                piece_value_rightup = chessboard[xlde][ylde]
                if piece_value_rightup == color:
                    leftd_string = leftd_string + 'o'
                elif piece_value_rightup == 0:
                    leftd_string = leftd_string + '_'
                else:
                    leftd_string = leftd_string + 'x'
                    break
        return leftd_string

    # 获取到右斜下对角方向上的图样
    def __get_rightdiagonally_pattern(self, chessboard, color, x, y):
        rightd_string = 'o'
        for i in range(1, 5):                               # 先往斜右下角的4个空位
            xrde = x + i
            yrde = y + i
            if xrde > 14 or yrde > 14:
                break
            else:
                piece_value_rightdown = chessboard[xrde][yrde]
                if piece_value_rightdown == color:
                    rightd_string = rightd_string + 'o'
                elif piece_value_rightdown == 0:
                    rightd_string = rightd_string + '_'
                else:
                    rightd_string = rightd_string + 'x'
                    break

        for i in range(1, 5):                               # 然后往斜左上角的4个空位
            xrde = x - i
            yrde = y - i
            if xrde < 0 or yrde < 0:
                break
            else:
                piece_value_leftup = chessboard[xrde][yrde]
                if piece_value_leftup == color:
                    rightd_string = 'o' + rightd_string
                elif piece_value_leftup == 0:
                    rightd_string = '_' + rightd_string
                else:
                    rightd_string = 'x' + rightd_string
                    break
        return rightd_string


# ai = AI(15, 1, 1)
# ai.go(np.zeros((15, 15), dtype=np.int))
