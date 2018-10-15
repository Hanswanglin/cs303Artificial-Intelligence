#!/usr/bin/env python3
"""
check the security and functionability of uploaded code 
- forbid from importing os
- random chessboard check
- some special case check
"""
import imp
import traceback

import numpy as np
from timeout_decorator import timeout

FORBIDDEN_LIST = ['import os', 'exec']

class CodeCheck():
    def __init__ (self, script_file_path, chessboard_size):
        self.time_out = 1
        self.script_file_path = script_file_path
        self.chessboard_size = chessboard_size
        self.agent = None # actually it is an object
        self.errormsg = 'Error'
        # print(self.chessboard)
        
    # Call this function and get True or False, self.errormsg has the message
    def check_code(self):
        # check if contains forbidden library
        if self.__check_forbidden_import() == False:
            return False

        # check initialization
        try:
            # init as white agent object
            self.agent = imp.load_source('AI', self.script_file_path).AI(self.chessboard_size, 1, self.time_out)
            # init as black agent obj
            self.agent = imp.load_source('AI', self.script_file_path).AI(self.chessboard_size, -1, self.time_out)
        except Exception:
            self.errormsg = "Fail to init"
            return False

        # check simple condition
        if not self.__check_simple_chessboard():
            self.errormsg = "Can not pass usability test."
            return False

        # check advance condition, online test contain more test case than this demo
        if not self.__check_advance_chessboard():
            self.errormsg = "Your code is too weak, fail to pass base test."
            return False
        return True


    def __check_forbidden_import(self):
        with open(self.script_file_path, 'r') as myfile:
            data = myfile.read()
            for keyword in FORBIDDEN_LIST:
                idx = data.find(keyword)
                if idx != -1:
                    self.errormsg = "import forbidden"
                    return False
        return True

    # check exec a go() within one sec
    def __check_go (self, chessboard):
        try:
            timeout(4)(self.agent.go)(np.copy(chessboard))
        except Exception:
            self.errormsg = "Error:" + traceback.format_exc()
            return False
        return True

    # check if the agent generate its candidate_list and if the list[-1] is contained in the result
    def __check_result(self, chessboard, result):
        if not self.__check_go(chessboard):
            print("2.2")
            return False
        if not self.agent.candidate_list or list(self.agent.candidate_list[-1]) not in result:
            return False
        return True

    # if the agent can find the only available location it can decided, then it will pass the check
    def __check_simple_chessboard(self):
        # empty chessboard
        # check whether it can give an choice within one sec
        if not self.__check_go(np.zeros((self.chessboard_size, self.chessboard_size), dtype=np.int)):
            print("1")
            return False
        print("=========first simple check have pass")
        # only one empty position remain
        chessboard = np.ones((self.chessboard_size, self.chessboard_size))
        chessboard[:, ::2] = -1 # all location have been filled up
        # make sure that the chessboard made do not exist "into five" pattern
        for i in range(0, self.chessboard_size, 4):
            chessboard[i] = -chessboard[i]
        # set a single random location in the chessboard is empty
        x, y = np.random.choice(self.chessboard_size, 2)
        chessboard[x, y] = 0
        print(chessboard)
    
        if not self.__check_result(chessboard, [[x, y]]):
            print("2")
            return False
        return True
    
    def __check_advance_chessboard (self):
        print("====================here is advance_test==============")
        # win, only one chess need to make it win
        chessboard = np.zeros((self.chessboard_size, self.chessboard_size), dtype=np.int)
        chessboard[0, 0:4] = -1
        chessboard[1, 0:4] = 1
        if not self.__check_result(chessboard, [[0, 4]]):
            return False
        
        # defense 5 inline
        chessboard = np.zeros((self.chessboard_size, self.chessboard_size), dtype=np.int)
        chessboard[0, 0:3] = -1
        chessboard[0, 7] = -1
        chessboard[1, 0:4] = 1
        if not self.__check_result(chessboard, [[1, 4]]):
            return False
        
        # two three
        chessboard = np.zeros((self.chessboard_size, self.chessboard_size), dtype=np.int)
        chessboard[1, 1:3] = -1
        chessboard[2:4, 3] = -1
        chessboard[1, 6:8] = 1
        chessboard[2:4, 8] = 1
        if not self.__check_result(chessboard, [[1, 3]]):
            return False
        
        # defense
        chessboard = np.zeros((self.chessboard_size, self.chessboard_size), dtype=np.int)
        chessboard[1, 0:2] = -1
        chessboard[2:4, 2] = -1
        chessboard[1, 6:8] = 1
        chessboard[2:4, 8] = 1
        if not self.__check_result(chessboard, [[1, 8]]):
            return False

        return True


check = CodeCheck("GoBang-v1.py", 15)
check.check_code()
print(check.errormsg)