#!/usr/bin/env python
# -*- coding:utf-8 -*-
# import pickle
import shlex


class InjectShield:
    def __init__(self):
        """
        算法初始化
        """
        None

    @staticmethod
    def dump_words(text):
        """
        抽取在限定范围内的字符串
        :param text:输入字符串
        """
        return shlex.quote(text)

if __name__ == '__main__':
    command = "exec(\"__import__('os').system('uname -a')\")"
    print(f"Original Command:{command}")
    print("{}\n".format(exec(command)))
    print(f"exec command:{exec(command)}")
    print(f"eval command:{exec(command)}")
    # exec("__import__('os').system('uname -a')")
    # eval("__import__('os').system('uname -a')")

    print("be injected but escape result command:")
    format_cmd = InjectShield.dump_words(command)
    print(f"Format Command:{format_cmd}")
    print(f"exec format command:{exec(format_cmd)}")
    print(f"eval format command:{exec(format_cmd)}")
