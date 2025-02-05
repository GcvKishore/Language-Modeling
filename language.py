"""
Language Modeling Project
Name:
Roll No:
"""

import language_tests as test

project = "Language" # don't edit this

### WEEK 1 ###

'''
loadBook(filename)
#1 [Check6-1]
Parameters: str
Returns: 2D list of strs
'''
def loadBook(filename):
    book = []
    f = open(filename)
    x = f.read().splitlines()
    for i in x:
        if len(i) > 0:
            book.append(i.split(" "))
    return book

'''
getCorpusLength(corpus)
#2 [Check6-1]
Parameters: 2D list of strs
Returns: int
'''
def getCorpusLength(corpus):
    count = 0
    for i in corpus:
        for j in i:
            count = count+1
    return count


'''
buildVocabulary(corpus)
#3 [Check6-1]
Parameters: 2D list of strs
Returns: list of strs
'''
def buildVocabulary(corpus):
    list1= []
    for i in corpus:
        for j in i:
            if j not in list1:
                list1.append(j)
    return  list1


'''
countUnigrams(corpus)
#4 [Check6-1]
Parameters: 2D list of strs
Returns: dict mapping strs to ints
'''
def countUnigrams(corpus):
    dict1={ }
    for i in corpus:
        for j in i:
            if j in dict1:
                dict1[j] = dict1[j]+1
            else:
                dict1[j] = 1 
    return  dict1

'''
getStartWords(corpus)
#5 [Check6-1]
Parameters: 2D list of strs
Returns: list of strs
'''
def getStartWords(corpus):
    list1 = []
    for i in corpus:
        if i[0] not in list1:
            list1.append(i[0])
    return  list1


'''
countStartWords(corpus)
#5 [Check6-1]
Parameters: 2D list of strs
Returns: dict mapping strs to ints
'''
def countStartWords(corpus):
    dict1={}
    for i in corpus:
        if i[0] in dict1:
            dict1[i[0]] = dict1[i[0]] + 1
        else:
            dict1[i[0]]=1
    return dict1

'''
countBigrams(corpus)
#6 [Check6-1]
Parameters: 2D list of strs
Returns: dict mapping strs to (dicts mapping strs to ints)
'''
def countBigrams(corpus):
    dict1={}
    for w in corpus:
        for j in range(len(w)-1):
            if w[j] not in dict1:
                dict1[w[j]] = {}
            if w[j+1] in dict1[w[j]]:
                dict1[w[j]][w[j+1]] += 1
            else:
                dict1[w[j]][w[j+1]] = 1
    return dict1

### WEEK 2 ###

'''
buildUniformProbs(unigrams)
#1 [Check6-2]
Parameters: list of strs
Returns: list of floats
'''
def buildUniformProbs(unigrams):
    uni=[]
    length=len(unigrams)
    for i in unigrams:
        prob=1/length
        uni.append(prob)
    return uni

'''
buildUnigramProbs(unigrams, unigramCounts, totalCount)
#2 [Check6-2]
Parameters: list of strs ; dict mapping strs to ints ; int
Returns: list of floats
'''
def buildUnigramProbs(unigrams, unigramCounts, totalCount):
    uni=[]
    for uniq in unigrams:
        count_word=unigramCounts[uniq]
        unigram_prob=(count_word/totalCount)
        uni.append(unigram_prob)
    return uni



'''
buildBigramProbs(unigramCounts, bigramCounts)
#3 [Check6-2]
Parameters: dict mapping strs to ints ; dict mapping strs to (dicts mapping strs to ints)
Returns: dict mapping strs to (dicts mapping strs to (lists of values))
'''
def buildBigramProbs(unigramCounts, bigramCounts):
    dict1={}
    for prevWord in bigramCounts:
        word=[]
        prob=[]
        for k,v in bigramCounts[prevWord].items():
            word.append(k)
            prob.append(v/unigramCounts[prevWord])
            dict2={}
            dict2["words"]=word
            dict2["probs"]=prob
        dict1[prevWord]=dict2
    return dict1

'''
getTopWords(count, words, probs, ignoreList)
#4 [Check6-2]
Parameters: int ; list of strs ; list of floats ; list of strs
Returns: dict mapping strs to floats
'''
def getTopWords(count, words, probs, ignoreList):
    dict1 = {}
    dict2 = {}
    for i in range(len(words)):
        if words[i] not in ignoreList:
            dict1[words[i]]=probs[i]
    sorted_list = sorted(dict1, key=dict1.get, reverse=True)
    for a in sorted_list:
        if len(dict2)<count:
            dict2[a]= dict1[a]
    return dict2

'''
generateTextFromUnigrams(count, words, probs)
#5 [Check6-2]
Parameters: int ; list of strs ; list of floats
Returns: str
'''
from random import choices
import random
def generateTextFromUnigrams(count, words, probs):
    text = " "
    for i in range (0,count):
        randWord = random.choices(words,weights=probs)
        text = text + randWord[0] + " "
    return text


'''
generateTextFromBigrams(count, startWords, startWordProbs, bigramProbs)
#6 [Check6-2]
Parameters: int ; list of strs ; list of floats ; dict mapping strs to (dicts mapping strs to (lists of values))
Returns: str
'''
def generateTextFromBigrams(count, startWords, startWordProbs, bigramProbs):
    text = " "
    choice = random.choices(startWords,weights=startWordProbs)[0]
    text = text + choice
    for i in range(count-1):
        if (choice!="."):
                x =bigramProbs[choice]['words']
                y =bigramProbs[choice]['probs']
                choice = random.choices(x,weights=y)[0]  
                text = text + " " + choice
                #print("z",z)
                #print("sss", sentence)
        else:
            choice= random.choices(startWords,weights=startWordProbs)[0]
            text = text + " " + choice
    return text

### WEEK 3 ###

ignore = [ ",", ".", "?", "'", '"', "-", "!", ":", ";", "by", "around", "over",
           "a", "on", "be", "in", "the", "is", "on", "and", "to", "of", "it",
           "as", "an", "but", "at", "if", "so", "was", "were", "for", "this",
           "that", "onto", "from", "not", "into" ]

'''
graphTop50Words(corpus)
#3 [Hw6]
Parameters: 2D list of strs
Returns: None
'''
def graphTop50Words(corpus):
    words = buildVocabulary(corpus)
    count = getCorpusLength(corpus)
    uni_count = countUnigrams(corpus)
    uni_probs = buildUnigramProbs(words, uni_count, totalCount=count)
    top_words = getTopWords(50,words,uni_probs,ignore)
    plot = barPlot(top_words, "Top 50 Words")
    return plot

'''
graphTopStartWords(corpus)
#4 [Hw6]
Parameters: 2D list of strs
Returns: None
'''
def graphTopStartWords(corpus):
    start=getStartWords(corpus)
    start_Count=countStartWords(corpus)
    startWordProbs=buildUnigramProbs(start,start_Count,len(corpus))
    count=getTopWords(50,start,startWordProbs,ignore)
    plot=barPlot(count,"Top State Words")
    return plot

'''
graphTopNextWords(corpus, word)
#5 [Hw6]
Parameters: 2D list of strs ; str
Returns: None
'''
def graphTopNextWords(corpus, word):
    uni_count=countUnigrams(corpus)
    bi_count=countBigrams(corpus)
    bigramProb=buildBigramProbs(uni_count,bi_count)
    count=getTopWords(10,bigramProb[word]["words"],bigramProb[word]["probs"],ignore)
    plot=barPlot(count,"Top Next Words")
    return plot

'''
setupChartData(corpus1, corpus2, topWordCount)
#6 [Hw6]
Parameters: 2D list of strs ; 2D list of strs ; int
Returns: dict mapping strs to (lists of values)
'''
def setupChartData(corpus1, corpus2, topWordCount):
    final={}
    cprob1=[]
    cprob2=[]
    unigram1=buildVocabulary(corpus1)
    unicount1=countUnigrams(corpus1)
    length1=getCorpusLength(corpus1)
    prob1=buildUnigramProbs(unigram1,unicount1,length1)
    top1=getTopWords(topWordCount,unigram1,prob1,ignore)
    unigram2=buildVocabulary(corpus2)
    unicount2=countUnigrams(corpus2)
    length2=getCorpusLength(corpus2)
    prob2=buildUnigramProbs(unigram2,unicount2,length2)
    top2=getTopWords(topWordCount,unigram2,prob2,ignore)
    lst=list(top1.keys())+list(top2.keys())
    twords=list(dict.fromkeys(lst))
    for i in range(len(twords)):
        if twords[i] in unigram1:
            y=unigram1.index(twords[i])
            cprob1.append(prob1[y])
        else:
            cprob1.append(0)
        if twords[i] in unigram2:
            y=unigram2.index(twords[i])
            cprob2.append(prob2[y])
    final["topWords"]=twords
    final["corpus1Probs"]=cprob1
    final["corpus2Probs"]=cprob2
    return final


'''
graphTopWordsSideBySide(corpus1, name1, corpus2, name2, numWords, title)
#6 [Hw6]
Parameters: 2D list of strs ; str ; 2D list of strs ; str ; int ; str
Returns: None
'''
def graphTopWordsSideBySide(corpus1, name1, corpus2, name2, numWords, title):
    dict_1=setupChartData(corpus1,corpus2,numWords)
    sideBySideBarPlots(dict_1["topWords"],dict_1["corpus1Probs"],dict_1["corpus2Probs"],name1,name2,title)
    return



'''
graphTopWordsInScatterplot(corpus1, corpus2, numWords, title)
#6 [Hw6]
Parameters: 2D list of strs ; 2D list of strs ; int ; str
Returns: None
'''
def graphTopWordsInScatterplot(corpus1, corpus2, numWords, title):
    dict_1=setupChartData(corpus1,corpus2,numWords)
    scatterPlot(dict_1["corpus1Probs"],dict_1["corpus2Probs"],dict_1["topWords"],title)
    return



### WEEK 3 PROVIDED CODE ###

"""
Expects a dictionary of words as keys with probabilities as values, and a title
Plots the words on the x axis, probabilities as the y axis and puts a title on top.
"""
def barPlot(dict, title):
    import matplotlib.pyplot as plt

    names = []
    values = []
    for k in dict:
        names.append(k)
        values.append(dict[k])

    plt.bar(names, values)

    plt.xticks(rotation='vertical')
    plt.title(title)

    plt.show()

"""
Expects 3 lists - one of x values, and two of values such that the index of a name
corresponds to a value at the same index in both lists. Category1 and Category2
are the labels for the different colors in the graph. For example, you may use
it to graph two categories of probabilities side by side to look at the differences.
"""
def sideBySideBarPlots(xValues, values1, values2, category1, category2, title):
    import matplotlib.pyplot as plt

    w = 0.35  # the width of the bars

    plt.bar(xValues, values1, width=-w, align='edge', label=category1)
    plt.bar(xValues, values2, width= w, align='edge', label=category2)

    plt.xticks(rotation="vertical")
    plt.legend()
    plt.title(title)

    plt.show()

"""
Expects two lists of probabilities and a list of labels (words) all the same length
and plots the probabilities of x and y, labels each point, and puts a title on top.
Note that this limits the graph to go from 0x0 to 0.02 x 0.02.
"""
def scatterPlot(xs, ys, labels, title):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()

    plt.scatter(xs, ys)

    # make labels for the points
    for i in range(len(labels)):
        plt.annotate(labels[i], # this is the text
                    (xs[i], ys[i]), # this is the point to label
                    textcoords="offset points", # how to position the text
                    xytext=(0, 10), # distance from text to points (x,y)
                    ha='center') # horizontal alignment can be left, right or center

    plt.title(title)
    plt.xlim(0, 0.02)
    plt.ylim(0, 0.02)

    # a bit of advanced code to draw a y=x line
    ax.plot([0, 1], [0, 1], color='black', transform=ax.transAxes)

    plt.show()


### RUN CODE ###

# This code runs the test cases to check your work
if __name__ == "__main__":
    # print("\n" + "#"*15 + " WEEK 1 TESTS " +  "#" * 16 + "\n")
    # test.week1Tests()
    # print("\n" + "#"*15 + " WEEK 1 OUTPUT " + "#" * 15 + "\n")
    # test.runWeek1()
    # test.testLoadBook()
    # test.testGetCorpusLength()
    # test.testBuildVocabulary()
    # test.testCountUnigrams()
    # test.testGetStartWords()
    # test.testCountStartWords()
    # test.testCountBigrams()
    # test.testBuildUniformProbs()
    # test.testBuildUnigramProbs()
    # test.testBuildBigramProbs()
    # test.testGetTopWords()
    # test.testGenerateTextFromUnigrams()
    # test.testGenerateTextFromBigrams()
    ## Uncomment these for Week 2 ##
# """
#     print("\n" + "#"*15 + " WEEK 2 TESTS " +  "#" * 16 + "\n")
#     test.week2Tests()
#     print("\n" + "#"*15 + " WEEK 2 OUTPUT " + "#" * 15 + "\n")
#     test.runWeek2()
# """

    ## Uncomment these for Week 3 ##

    print("\n" + "#"*15 + " WEEK 3 OUTPUT " + "#" * 15 + "\n")
    test.runWeek3()
