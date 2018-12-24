# -*- coding: utf-8 -*-
from Conversion.Tagging.code.Sentiment_svm_3 import svm_predict
from Conversion.Tagging.code.Sentiment_lstm_3 import lstm_predict, lstm_double_predict


# argvs_lenght = len(sys.argv)
# if argvs_lenght != 3:
#     print('参数长度错误！')
# argvs = sys.argv
#
# sentence = argvs[-1]
#
# if argvs[1] == 'svm':
#     svm_predict(sentence)
#
# elif argvs[1] == 'lstm':
#     lstm_predict(sentence)
#
# else:
#     print('选择svm或lstm！')


class predictor:
    def __init__(self, type='lstm'):
        self.type = type

    def predict_sentence(self, sentence=''):
        if self.type == 'lstm':
            return lstm_predict(sentence)
        elif self.type == 'svm':
            return svm_predict(sentence)

    def predict_double_sentence(self, string1, string2):
        if self.type == 'lstm':
            return lstm_double_predict(string1, string2)
        elif self.type == 'svm':
            return '', ''


if __name__ == "__main__":
    p = predictor('lstm')
    p.predict_sentence("系统登录成功")
