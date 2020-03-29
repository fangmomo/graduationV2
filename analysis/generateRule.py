from numpy import *


def createC1(dataSet):
    C1 = []
    for transaction in dataSet:
        for item in transaction:
            if not [item] in C1:
                C1.append([item])
    C1.sort()
    return map(frozenset, C1)


# 其中D为全部数据集，
# # Ck为大小为k（包含k个元素）的候选项集，
# # minSupport为设定的最小支持度。
# # 返回值中retList为在Ck中找出的频繁项集（支持度大于minSupport的），
# # supportData记录各频繁项集的支持度
def scanD(D, Ck, minSupport):
    ssCnt = {}
    numItems = float(len(list(D)))
    for tid in D:
        for can in Ck:
            if can.issubset(tid):
                ssCnt[can] = ssCnt.get(can, 0) + 1
    retList = []
    supportData = {}
    for item in ssCnt:
        support = ssCnt[item] / numItems  # 计算频数
        if support >= minSupport:
            retList.insert(0, item)
        supportData[item] = support
    return retList, supportData


# 生成 k+1 项集的候选项集
# 注意其生成的过程中，首选对每个项集按元素排序，然后每次比较两个项集，只有在前k-1项相同时才将这两项合并。
# # 这样做是因为函数并非要两两合并各个集合，那样生成的集合并非都是k+1项的。在限制项数为k+1的前提下，只有在前k-1项相同、最后一项不相同的情况下合并才为所需要的新候选项集。
def genCandidateSet(Lk, k):
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i + 1, lenLk):
            # 前k-2项相同时，将两个集合合并
            L1 = list(Lk[i])[:k - 2];
            L2 = list(Lk[j])[:k - 2]
            L1.sort();
            L2.sort()
            if L1 == L2:
                retList.append(Lk[i] | Lk[j])
    return retList


def apriori(dataSet, minSupport=0.5):
    C1 = createC1(dataSet)
    D = map(set, dataSet)
    L1, supportData = scanD(D, C1, minSupport)
    L = [L1]
    k = 2
    while len(L[k - 2]) > 0:
        Ck = genCandidateSet(L[k - 2], k)
        Lk, supK = scanD(D, Ck, minSupport)
        supportData.update(supK)
        L.append(Lk)
        k += 1
    return L, supportData


# 频繁项集列表L
# 包含那些频繁项集支持数据的字典supportData
# 最小可信度阈值minConf
def generateRules(L, supportData, minConf=0.7):
    bigRuleList = []
    # 频繁项集是按照层次搜索得到的, 每一层都是把具有相同元素个数的频繁项集组织成列表，再将各个列表组成一个大列表，所以需要遍历Len(L)次, 即逐层搜索
    for i in range(1, len(L)):
        for freqSet in L[i]:
            H1 = [frozenset([item]) for item in freqSet]  # 对每个频繁项集构建只包含单个元素集合的列表H1
            # print ("\nfreqSet: ", freqSet)
            # print ("H1: ", H1)
            rulesFromConseq(freqSet, H1, supportData, bigRuleList, minConf)  # 根据当前候选规则集H生成下一层候选规则集
    return bigRuleList


# 根据当前候选规则集H生成下一层候选规则集
def rulesFromConseq(freqSet, H, supportData, brl, minConf=0.7):
    m = len(H[0])
    while len(freqSet) > m:  # 判断长度 > m，这时即可求H的可信度
        H = calcConf(freqSet, H, supportData, brl, minConf)  # 返回值prunedH保存规则列表的右部，这部分频繁项将进入下一轮搜索
        if len(H) > 1:  # 判断求完可信度后是否还有可信度大于阈值的项用来生成下一层H
            H = genCandidateSet(H, m + 1)
            # print ("H = aprioriGen(H, m + 1): ", H)
            m += 1
        else:  # 不能继续生成下一层候选关联规则，提前退出循环
            break


# 计算规则的可信度，并过滤出满足最小可信度要求的规则
def calcConf(freqSet, H, supportData, brl, minConf=0.7):
    """ 对候选规则集进行评估 """
    prunedH = []
    for conseq in H:
        # print ("conseq: ", conseq)
        # print ("supportData[freqSet]: ", supportData[freqSet])
        # print ("supportData[freqSet - conseq]: ", supportData[freqSet - conseq])
        conf = supportData[freqSet] / supportData[freqSet - conseq]
        if conf >= minConf:
            # print (freqSet - conseq, '-->', conseq, 'conf:', conf)
            brl.append((freqSet - conseq, conseq, conf))
            prunedH.append(conseq)
            # print ("prunedH: ", prunedH)
    return prunedH
