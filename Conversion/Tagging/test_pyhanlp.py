from pyhanlp import *

# result1 = HanLP.parseDependency("用户输入账号和有效密码，点击取钱，输入取款金额")
result1 = HanLP.parseDependency("如果执行预计算，则预期预计算路径成功，客户确认路径，点击应用。如果不执行预计算，则客户点击按钮")

# 也可以直接拿到数组，任意顺序或逆序遍历
word_array = result1.getWordArray()
for word in word_array:
    print("%s --(%s)--> %s" % (word.LEMMA, word.DEPREL, word.HEAD.LEMMA))
print(len(word_array))
print()

result = ''
user = ''
action = ''
pre = 1
mid = 1
post = 1
temp_pre = ''
temp_mid = ''
temp_post = ''
suffix = '('
i = 0
while i < len(word_array):
    if word_array[i].DEPREL == '主谓关系':
        user = word_array[i].LEMMA
        i += 1
        pre = 0
        continue
    if word_array[i].DEPREL == "核心关系":
        action = word_array[i].LEMMA
        i += 1
        mid = 0
        continue
    if word_array[i].DEPREL == "动宾关系":
        result += temp_pre + user + temp_mid + action + temp_post + word_array[i].LEMMA + suffix
        i += 1
        post = 0
        continue
    if word_array[i].DEPREL == "并列关系":
        temp = word_array[i].HEAD
        pre = 0
        while temp.DEPREL != '核心关系' and temp.DEPREL != '动宾关系' and temp.DEPREL is not None:
            temp = temp.HEAD
        if temp.DEPREL == '核心关系':
            action = word_array[i].LEMMA
            mid = 0
            i += 1
            continue
        if temp.DEPREL == "动宾关系":
            result += temp_pre + user + temp_mid + action + temp_post + word_array[i].LEMMA + suffix
            i += 1
            post = 0
            continue
        i += 1
    if word_array[i].DEPREL == "标点符号":
        pre = mid = post = 1
        temp_pre = temp_post = temp_mid = ""
        i += 1
        continue
    if word_array[i].DEPREL == "左附加关系":
        post = 1
        i += 1
        continue
    if pre == 1:
        temp_pre += word_array[i].LEMMA
        i += 1
        pre = 0
        continue
    if mid == 1:
        temp_mid += word_array[i].LEMMA
        i += 1
        continue
    if post == 1:
        temp_post += word_array[i].LEMMA
        i += 1
        continue
    i += 1
print(result)
