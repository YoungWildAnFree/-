#coding:utf-8
import random
import jieba
def compute_prefix_function(p):
    m = len(p)
    pi = [0] * m
    k = 0
    for q in range(1, m):
        while k > 0 and p[k] != p[q]:
            k = pi[k - 1]
        if p[k] == p[q]:
            k = k + 1
        pi[q] = k
    return pi

def kmp_matcher(t, p):
    n = len(t)
    m = len(p)
    pi = compute_prefix_function(p)
    q = 0
    for i in range(n):
        while q > 0 and p[q] != t[i]:
            q = pi[q - 1]
        if p[q] == t[i]:
            q = q + 1
        if q == m:
            return i - m + 1
    return -1



question = "我国国酒茅台酒出于哪个省份"
def tiku_search(question):
    remove_words= ['哪个','以下','哪','我国','属于','作为','出自于','没有','不是','哪一种','哪一个']
    s_generator= jieba.cut(question, cut_all=False)
    s_list_2 = []
    s_list_3 = []
    search_word = ''
    for i in s_generator:
        if len(i)==2:
            s_list_2.append(i)
        elif len(i)>=3:
            s_list_3.append(i)

    for i in s_list_2:
        if i in remove_words:
            s_list_2.remove(i)

    for i in s_list_3:
        if i in remove_words:
            s_list_3.remove(i)
    if s_list_3 != []:
        search_word = s_list_3[random.randint(0, len(s_list_3) - 1)]
    else:
        search_word = s_list_2[random.randint(0, len(s_list_2) - 1)]


    # search_word = s_list[random.randint(0,len(s_list)-1)]
    print("题库中搜索的词为"+search_word)
    with open('./tiku.txt','r',encoding='utf-8') as f :
        while True:
            line = f.readline()
            # print(line)
            if search_word in line:
                print(line)
            elif line == "":
                break
            else:
                continue



