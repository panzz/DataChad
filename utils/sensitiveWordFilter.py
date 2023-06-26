#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os

CONSTANTS_ROOT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "constants")
# print('CONSTANTS_ROOT_PATH:%r'%(CONSTANTS_ROOT_PATH))
DEFAULT_SENSITIVE_PATH = os.path.join(CONSTANTS_ROOT_PATH, 'sensitive_words.txt')
# print('DEFAULT_SENSITIVE_PATH:%r'%(DEFAULT_SENSITIVE_PATH))

class SensitiveWordFilter:
    def __init__(self, path=DEFAULT_SENSITIVE_PATH, replace_char='*'):
        """
        算法敏感词过滤初始化，采用DFA(Deterministic Finite Automaton)算法
        DFA 算法是通过提前构造出一个 树状查找结构(实际上应该说是一个 森林)，之后根据输入在该树状结构中就可以进行非常高效的查找。
        参考：https://github.com/spirit-yzk/sensitive_words_blocking/blob/master/dfa.py
        :param path:词库地址
        """
        # print(f'init SensitiveWordFilter path: {path}')
        self.ban_words_set = set()
        self.ban_words_list = list()
        self.ban_words_dict = dict()
        self.replace_char = replace_char
        self.path = path
        self.get_sensitive_words()

    @staticmethod
    def draw_words(_str, pos_list):
        """
        抽取在限定范围内的字符串
        静态方法，可实例化使用 C().draw_words()，当然也可以不实例化直接调用该方法 C.draw_words()
        :param _str:输入字符串
        :param pos_list:抽取的字符串数组
        """
        ss = str()
        # print(f"draw_words> _str: {_str}")
        inputstr = str(_str)
        # print(f"draw_words> inputstr: {inputstr}")
        for i in range(len(inputstr)):
            s = str(inputstr[i])
            # print(f"draw_words> s: {s}")
            if '\u4e00' <= s <= '\u9fa5' or '\u3400' <= s <= '\u4db5' or '\u0030' <= s <= '\u0039' \
                    or '\u0061' <= s <= '\u007a' or '\u0041' <= s <= '\u005a':
                ss += inputstr[i]
                pos_list.append(i)
        return ss

    def add_new_word(self, new_word):
        """
        添加单个敏感词
        :param new_word:新敏感词
        """
        new_word = str(new_word)
        now_dict = self.ban_words_dict
        i = 0
        for x in new_word:
            if x not in now_dict:
                x = str(x)
                new_dict = dict()
                new_dict['is_end'] = False
                now_dict[x] = new_dict
                now_dict = new_dict
            else:
                now_dict = now_dict[x]
            if i == len(new_word) - 1:
                now_dict['is_end'] = True
            i += 1

    def add_hash_dict(self, new_list):
        """
        将敏感词列表转换为DFA字典序
        :param new_list:新敏感词数组
        """
        for x in new_list:
            self.add_new_word(x)

    def get_sensitive_words(self):
        """
        获取敏感词列表
        """
        if not (os.path.isfile(self.path)):
            err_msg = f'get_sensitive_words path:{self.path} is not exist'
            print(f'SensitiveWordFilter ERROR: {err_msg}')
            raise Exception(err_msg)

        with open(self.path, 'r', encoding='utf-8-sig') as f:
            for s in f:
                if s.find('\\r'):
                    s = s.replace('\r', '')
                s = s.replace('\n', '')
                s = s.strip()
                if len(s) == 0:
                    continue
                if str(s) and s not in self.ban_words_set:
                    self.ban_words_set.add(s)
                    self.ban_words_list.append(str(s))
        self.add_hash_dict(self.ban_words_list)

    def change_words(self, path):
        """
        指定新的敏感词库
        :param path:新词库的地址
        """
        self.ban_words_list.clear()
        self.ban_words_dict.clear()
        self.ban_words_set.clear()
        self.path = path
        self.get_sensitive_words()

    def find_first_illegal(self, _str):
        """
        寻找第一次出现敏感词的位置
        :param _str:输入字符串
        """
        now_dict = self.ban_words_dict
        i = 0
        start_word = -1
        is_start = True  # 判断是否是一个敏感词的开始
        while i < len(_str):
            if _str[i] not in now_dict:
                if is_start is True:
                    i += 1
                    continue
                i = start_word +1
                start_word = -1
                is_start = True
                now_dict = self.ban_words_dict
            else:
                if is_start is True:
                    start_word = i
                    is_start = False
                now_dict = now_dict[_str[i]]
                if now_dict['is_end'] is True:
                    return start_word
                else:
                    i += 1
        return -1

    def is_exists(self, s):
        """
        查找是否存在敏感词
        :param s:字符串
        """
        pos = self.find_first_illegal(s)
        if pos == -1:
            return False
        else:
            return True

    def filter_sensitive_words(self, filter_str, pos):
        """
        将指定位置的敏感词替换为*
        :param filter_str:过滤字符串
        :param pos:位置
        """
        now_dict = self.ban_words_dict
        end_str = int()
        for i in range(pos, len(filter_str)):
            if now_dict[filter_str[i]]['is_end'] is True:
                end_str = i
                break
            now_dict = now_dict[filter_str[i]]
        num = end_str - pos + 1
        filter_str = filter_str[:pos] + self.replace_char*num + filter_str[end_str + 1:]
        return filter_str

    def filter_all(self, s):
        """
        过滤字符串
        :param s:字符串
        """
        pos_list = list()
        ss = SensitiveWordFilter.draw_words(s, pos_list)
        illegal_pos = self.find_first_illegal(ss)
        while illegal_pos != -1:
            ss = self.filter_sensitive_words(ss, illegal_pos)
            illegal_pos = self.find_first_illegal(ss)
        i = 0
        while i < len(ss):
            if ss[i] == self.replace_char:
                start = pos_list[i]
                while i < len(ss) and ss[i] == self.replace_char:
                    i += 1
                i -=1
                end = pos_list[i]
                num = end-start+1
                s = s[:start] + self.replace_char*num + s[end+1:]
            i += 1
        return s

if __name__ == '__main__':
    dfa = SensitiveWordFilter()
    # s0 = dfa.get_sensitive_words()
    # print(s0)
    # 过滤实例
    s1 = '日、你￥，妈,1,2#@3,ffsf批,'
    print(f'test s1: {s1}')
    # test s1:日、你￥，妈,1,2#@3,ffsf妈 *卖 *批,
    s2 = dfa.filter_all(s1)
    print(f'test s2: {s2}')
    # test s2: ******,1,2#@3,ffsf妈 *卖 *批,
    # 添加敏感词
    s = 'sf'
    dfa.add_new_word(s)
    # 检查是否存在敏感词,存在返回True,不存在返回False,不改变字符串
    isExist = dfa.is_exists(s2)
    print(f'test isExist: {isExist}')
    # test isExist: True
    s3 = dfa.filter_all(s2)
    print(f'test s3: {s3}')
    # test s3: ******,1,2#@3,ff**妈 *卖 *批,

    # dfa.change_words(path)