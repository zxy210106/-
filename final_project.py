#coding:utf-8
"""
程序:基于Python和Gelphi的《黎明破晓的街道》人物关系图谱构建
时间：2019.12.29
"""
import codecs
import jieba.posseg as pseg
import jieba#调用jieba

#excludes = {}
#txt = open("黎明破晓的街道.txt", "r", encoding='utf-8').read()
#words  = jieba.lcut(txt)
#counts = {}
#for word in words:
    #if len(word) == 1:
        #continue
    #else:
        #counts[word] = counts.get(word,0) + 1
#for word in excludes:
	#del(counts[word])
   
#items = list(counts.items())
#items.sort(key=lambda x:x[1], reverse=True) 
#for i in range(25):
    #word, count = items[i]
    #print ("{0:<10}{1:>5}".format(word, count))

names={}#姓名字典
relationships={}#关系字典
lineNames=[]

jieba.load_userdict("names.txt")#加载人物表
with codecs.open("黎明破晓的街道.txt", 'r', 'utf8') as f:
    for line in f.readlines():
        poss = pseg.cut(line)  # 分词，返回词性
        lineNames.append([])  # 为本段增加一个人物列表
        for w in poss:
            if w.flag != 'nr' or len(w.word) < 2:
                continue  # 当分词长度小于2或该词词性不为nr（人名）时认为该词不为人名
            lineNames[-1].append(w.word)  # 为当前段的环境增加一个人物
            if names.get(w.word) is None:  # 如果某人物（w.word）不在人物字典中
                names[w.word] = 0
                relationships[w.word] = {}
            names[w.word] += 1

for line in lineNames:
    for name1 in line:
        for name2 in line:
            if name1 == name2:
                continue
            if relationships[name1].get(name2) is None:
                relationships[name1][name2] = 1
            else:
                relationships[name1][name2] = relationships[name1][name2] + 1

with codecs.open("黎明破晓的街道_node.txt", "w", "utf8") as f:
    f.write("ID Label Weight\r\n")
    for name, times in names.items():
        if times > 10:
            f.write(name + " " + name + " " + str(times) + "\r\n")

with codecs.open("黎明破晓的街道_edge.txt", "w", "utf8") as f:
    f.write("Source Target Weight\r\n")
    for name, edges in relationships.items():
        for v, w in edges.items():
            if w > 10:
                f.write(name + " " + v + " " + str(w) + "\r\n")

f=open('黎明破晓的街道_edge.txt','r',encoding='utf-8')
f2=open('names.txt','r',encoding='utf-8').read()
lines=f.readlines()

X=[]
for line in lines:#判断词性，是否为人物姓名，进行适当删改
    X.append([])
    m=line.strip('\n').split(' ')
    for x in m:
        X[-1].append(x)
for items in X:
    if items[0]and items[1] not in f2:
        del(items)

f.close()
