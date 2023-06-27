#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re

class PrivacyFilter:
    def __init__(self):
        self.url_re = None
        self.initialised = False
        self.numbers_to_zero = False

    def initialize(self, numbers_to_zero=False):
        """
        初始化正则表达式
        :param numbers_to_zero: 是否将数字替换为0
        """
        # Make the URL regular expression
        # https://stackoverflow.com/questions/827557/how-do-you-validate-a-url-with-a-regular-expression-in-python
        ul = '\u00a1-\uffff'  # Unicode letters range (must not be a raw string).

        # IP patterns
        ipv4_re = r'(?:0|25[0-5]|2[0-4]\d|1\d?\d?|[1-9]\d?)(?:\.(?:0|25[0-5]|2[0-4]\d|1\d?\d?|[1-9]\d?)){3}'
        ipv6_re = r'\[?((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,'\
                  r'4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{'\
                  r'1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2['\
                  r'0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,'\
                  r'3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|['\
                  r'1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,'\
                  r'2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|((['\
                  r'0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2['\
                  r'0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:['\
                  r'0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2['\
                  r'0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,'\
                  r'5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?\]?'

        # Host patterns
        hostname_re = r'[a-z' + ul + r'0-9](?:[a-z' + ul + r'0-9-]{0,61}[a-z' + ul + r'0-9])?'
        # Max length for domain name labels is 63 characters per RFC 1034 sec. 3.1
        domain_re = r'(?:\.(?!-)[a-z' + ul + r'0-9-]{1,63}(?<!-))*'
        tld_re = (
                r'\.'                                # dot
                r'(?!-)'                             # can't start with a dash
                r'(?:[a-z' + ul + '-]{2,63}'         # domain label
                r'|xn--[a-z0-9]{1,59})'              # or punycode label
                r'(?<!-)'                            # can't end with a dash
                r'\.?'                               # may have a trailing dot
        )
        host_re = '(' + hostname_re + domain_re + tld_re + '|localhost)'

        self.url_re = re.compile(
            r'([a-z0-9.+-]*:?//)?'                                       # scheme is validated separately
            r'(?:[^\s:@/]+(?::[^\s:@/]*)?@)?'                           # user:pass authentication
            r'(?:' + ipv4_re + '|' + ipv6_re + '|' + host_re + ')'
            r'(?::\d{2,5})?'                                            # port
            r'(?:[/?#][^\s]*)?',                                        # resource path
            re.IGNORECASE
        )

        self.numbers_to_zero = numbers_to_zero
        self.initialised = True

    @staticmethod
    def remove_numbers(text, numbers_to_zero):
        """
        移除数字
        :param numbers_to_zero: 是否将数字替换为0
        """
        if numbers_to_zero:
            return re.sub('\d', '0', text).strip()
        else:
            return re.sub('\d+(,\d{3})*(\.\d{1,2})?', '<NUMBER>', text).strip()

    @staticmethod
    def remove_times(text):
        """
        移除时间
        :param text: 输入文本
        """
        return re.sub('([ ]?(早|中|晚))?([ ]?(上|午))?(\d{1,2})[:](\d{1,2})?([ ]?(am|pm|AM|PM))?', '<TIME>', text)

    @staticmethod
    def remove_dates(text):
        """
        移除日期
        :param text: 输入文本
        """
        text = re.sub("\d{2,4}[- /.]\d{2}[- /.]\d{,4}", "<DATE>", text)

        text = re.sub("(\d{1,2}[^\w]{,2}(月)" "([- /.]{,2}(\d{4}|\d{2}))?)", "<DATE>", text)

        text = re.sub( "(\d{1,2}[^\w]{,2}(jan|feb|mrt|apr|mei|jun|jul|aug|sep|okt|nov|dec))[- /.](\d{4}|\d{2})?", "<DATE>", text)
        return text

    @staticmethod
    def remove_email(text):
        """
        移除邮件
        :param text: 输入文本
        """
        return re.sub("(([a-zA-Z0-9_+]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?))" "(?![^<]*>)", "<EMAIL>", text)

    def remove_url(self, text):
        """
        移除URL
        :param text: 输入文本
        """
        # print(f'remove_url url_re: {self.url_re}')
        text = re.sub(self.url_re, "<URL>", text)
        return text

    @staticmethod
    def remove_postal_codes(text):
        """
        移除邮政编码
        :param text: 输入文本
        """
        return re.sub("[1-9]\d{5}(?!\d)", "<POSTCODE>", text)

    @staticmethod
    def remove_phone_number(text):
        """
        移除电话号码
        :param text: 输入文本
        """
        text = re.sub("\d{3}-\d{8}|\d{4}-\d{7}", "<PHONE>", text)
        text = re.sub("(?:(?:\+|00)86)?1(?:(?:3[\d])|(?:4[5-79])|(?:5[0-35-9])|(?:6[5-7])|(?:7[0-8])|(?:8[\d])|(?:9[189]))\d{8}", "<PHONE>", text)
        return text

    @staticmethod
    def remove_gender(text):
        """
        移除性别
        :param text: 输入文本
        """
        text = re.sub("(男|女|male|female)", "<GENDER>", text)
        return text

    @staticmethod
    def remove_id_number(text):
        """
        移除身份证或护照号
        :param text: 输入文本
        """
        # 身份证
        text = re.sub(r"[1-9]\d{5}(?:18|19|20)\d{2}(?:0[1-9]|10|11|12)(?:0[1-9]|[1-2]\d|30|31)\d{3}[\dXx]", "<IDNUM>", text)
        # 护照
        text = re.sub(r"([EeKkGgDdSsPpHh]\d{8})|((([Ee][a-fA-F])|([DdSsPp][Ee])|([Kk][Jj])|([Mm][Aa])|(1[45]))\d{7})", "<IDNUM>", text)
        # 香港身份证
        text = re.sub(r"[a-zA-Z]\d{6}\([\dA]\)", "<IDNUM>", text)
        # 澳门身份证
        text = re.sub(r"[1|5|7]\d{6}\(\d\)", "<IDNUM>", text)
        # 台湾身份证
        text = re.sub(r"[a-zA-Z][0-9]{9}", "<IDNUM>", text)
        return text

    @staticmethod
    def cleanup_text(result):
        """
        格式化文本
        :param result: 输入文本
        """
        # result = re.sub("<[A-Z _]+>", "<FILTERED>", result)
        result = re.sub(" ([ ,.:;?!])", "\\1", result)
        result = re.sub(" +", " ", result)                          # remove multiple spaces
        result = re.sub("\n +", "\n", result)                       # remove space after newline
        result = re.sub("( <FILTERED>)+", " <FILTERED>", result)    # remove multiple consecutive <FILTERED> tags
        return result.strip()


    def filter_regular_expressions(self, text):
        """
        正则过滤文本
        :param text: 输入文本
        """
        print(f'filter_regular_expressions text: {text}')
        text = self.remove_dates(text)
        # print(f'filter_regular_expressions remove_dates text: {text}')
        text = self.remove_times(text)
        # print(f'filter_regular_expressions remove_times text: {text}')
        text = self.remove_phone_number(text)
        # print(f'filter_regular_expressions remove_phone_number text: {text}')
        text = self.remove_id_number(text)
        # print(f'filter_regular_expressions remove_id_number text: {text}')
        text = self.remove_postal_codes(text)
        # print(f'filter_regular_expressions remove_postal_codes text: {text}')
        text = self.remove_numbers(text, self.numbers_to_zero)
        # print(f'filter_regular_expressions remove_numbers text: {text}')
        text = self.remove_email(text)
        # print(f'filter_regular_expressions remove_email text: {text}')
        text = self.remove_gender(text)
        # print(f'filter_regular_expressions remove_gender text: {text}')
        text = self.remove_url(text)
        # print(f'filter_regular_expressions remove_url text: {text}')
        return text


    def filter(self, text):
        """
        过滤文本
        :param text: 输入文本
        """
        if not self.initialised:
            self.initialize()
        text = str(text)

        text = self.filter_regular_expressions(text)

        return self.cleanup_text(text)


if __name__ == '__main__':
    sentence = "小明生于2014-04-08，性别男，他的邮箱是xiaoming@email.com，手机号是13812345678,座机号是010-67837620，身份证号是110105202306170322，香港身份证C668668(A)，澳门身份证1000248(3)，台湾身份证A234567890，护照号G27940445，他今年13岁，家住北京市朝阳区北苑路28号,邮编100021，昨天晚上8:30分在网上买了1件衬衣，花了581,237.99元。他老爸叫大明，老妈叫小妹。他的个人主页是https://developerforum.lenovo.com/me"
    pft = PrivacyFilter()
    pft.initialize()
    print(pft.filter(sentence))