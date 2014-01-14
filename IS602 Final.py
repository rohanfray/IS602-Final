__author__ = 'Rohan'

from Tkinter import *
from tkFileDialog import *

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

import vgprice


def getelements(vglist, type):
    tmplist = []
    for i in vglist:
        tmplist.append(getattr(i, type))
    return tmplist


def createstructarray(looseprices, cibprices, newprices, reviews, genres, years, consolenames, newloosespread):
    x = np.zeros((looseprices.size,),
                 dtype = [('looseprices', 'f4'), ('cibprices', 'f4'), ('newprices', 'f4'), ('reviews',
                                                                                            'f4'),
                          ('genres', 'a30'), ('years', 'a5'), ('consolenames', 'a30'),
                          ('newloosespread', 'f4')])

    x['looseprices'] = looseprices
    x['cibprices'] = cibprices
    x['newprices'] = newprices
    x['reviews'] = reviews
    x['genres'] = genres
    x['years'] = years
    x['consolenames'] = consolenames
    x['newloosespread'] = newloosespread
    return x


def firstplot(vgarray):
    """
    plots each genre spread v reviewscore
    :param vgarray:
    """
    listGenres = np.unique(vgarray['genres'])
    plt.figure(1)

    sp = 1
    for i in listGenres:
        plt.subplot(7, 4, sp)
        spread = vgarray[np.where(vgarray['genres'] == i)]['newloosespread']
        review = vgarray[np.where(vgarray['genres'] == i)]['reviews']
        plt.plot(spread[~np.isnan(spread)&~np.isnan(review)], review[~np.isnan(review)&~np.isnan(spread)], 'ro')


        try:
            m, b, rvalue, pvalue, stderror = stats.linregress(spread[~np.isnan(spread)&~np.isnan(review)], review[~np.isnan(review)&~np.isnan(spread)])
            x1, x2, n = np.amin(spread[~np.isnan(spread)&~np.isnan(review)]), np.amax(spread[~np.isnan(spread)&~np.isnan(review)]), 11
            x = np.r_[x1:x2:n * 1j]
            plt.plot(x, m * x + b)

        except:
            pass
        cor = stats.pearsonr(spread[~np.isnan(spread)&~np.isnan(review)], review[~np.isnan(review)&~np.isnan(spread)])
        cor = "{0:.2f}".format(cor[0])
        plt.title(i + " --- " + cor, size = 9)
        sp = sp + 1
    plt.tight_layout()
    plt.show()


def secondplot(vgarray):
    """
    asks for genre and then plots that genre and everything sans that genre
    :param vgarray:
    """
    listGenres = np.unique(vgarray['genres'])
    print "Please input one of the following genres:"
    for i in listGenres:
        print i
    var = raw_input("Enter a genre:")
    if var not in listGenres:
        print "wrong entry"
        return

    spreadgenre = vgarray[np.where(vgarray['genres'] == var)]['newloosespread']
    reviewgenre = vgarray[np.where(vgarray['genres'] == var)]['reviews']

    spreadelse = vgarray[np.where(vgarray['genres'] != var)]['newloosespread']
    reviewelse = vgarray[np.where(vgarray['genres'] != var)]['reviews']

    plt.figure(1)
    plt.subplot(2, 1, 1)
    plt.plot(spreadgenre[~np.isnan(spreadgenre)&~np.isnan(reviewgenre)], reviewgenre[~np.isnan(reviewgenre)&~np.isnan(spreadgenre)], 'ro')
    try:
        m, b, rvalue, pvalue, stderror = stats.linregress(spreadgenre[~np.isnan(spreadgenre)&~np.isnan(reviewgenre)],
                                                          reviewgenre[~np.isnan(reviewgenre)&~np.isnan(spreadgenre)])
        x1, x2, n = np.amin(spreadgenre[~np.isnan(spreadgenre)&~np.isnan(reviewgenre)]), np.amax(spreadgenre[~np.isnan(spreadgenre)&~np.isnan(reviewgenre)]), 11
        x = np.r_[x1:x2:n * 1j]
        plt.plot(x, m * x + b)
    except:
        pass
    cor = stats.pearsonr(spreadgenre[~np.isnan(spreadgenre)&~np.isnan(reviewgenre)], reviewgenre[~np.isnan(reviewgenre)&~np.isnan(spreadgenre)])
    cor = "{0:.2f}".format(cor[0])
    plt.title(var + " --- " + str(cor), size = 9)



    plt.subplot(2, 1, 2)
    plt.plot(spreadelse[~np.isnan(spreadelse)&~np.isnan(reviewelse)], reviewelse[~np.isnan(reviewelse)&~np.isnan(spreadelse)], 'ro')
    try:
        m, b, rvalue, pvalue, stderror = stats.linregress(spreadelse[~np.isnan(spreadelse)&~np.isnan(reviewelse)],
                                                          reviewelse[~np.isnan(reviewelse)&~np.isnan(spreadelse)])
        x1, x2, n = np.amin(spreadelse[~np.isnan(spreadelse)&~np.isnan(reviewelse)]), np.amax(spreadelse[~np.isnan(spreadelse)&~np.isnan(reviewelse)]), 11
        x = np.r_[x1:x2:n * 1j]
        plt.plot(x, m * x + b)
    except:
        pass
    cor = stats.pearsonr(spreadelse[~np.isnan(spreadelse)&~np.isnan(reviewelse)], reviewelse[~np.isnan(reviewelse)&~np.isnan(spreadelse)])
    cor = "{0:.2f}".format(cor[0])
    plt.title("everything but " + var + " --- " + str(cor), size = 9)

    plt.tight_layout()
    plt.show()


def thirdplot(vgarray):
    """
    asks for year and plots that year and everything sans that year
    :param vgarray:
    :return:
    """
    listYears = np.sort(np.unique(vgarray['years']))
    print "Please input one of the following year:"
    for i in listYears:
        print i
    var = raw_input("Enter a year:")
    if var not in listYears:
        print "wrong entry"
        return

    spreadyear = vgarray[np.where(vgarray['years'] == var)]['newloosespread']
    reviewyear = vgarray[np.where(vgarray['years'] == var)]['reviews']


    spreadelse = vgarray[np.where(vgarray['years'] != var)]['newloosespread']
    reviewelse = vgarray[np.where(vgarray['years'] != var)]['reviews']


    plt.figure(1)
    plt.subplot(2, 1, 1)
    plt.plot(spreadyear[~np.isnan(spreadyear)&~np.isnan(reviewyear)], reviewyear[~np.isnan(reviewyear)&~np.isnan(spreadyear)], 'ro')
    try:
        m, b, rvalue, pvalue, stderror = stats.linregress(spreadyear[~np.isnan(spreadyear)&~np.isnan(reviewyear)], reviewyear[~np.isnan(reviewyear)&~np.isnan(spreadyear)])
        x1, x2, n = np.amin(spreadyear[~np.isnan(spreadyear)&~np.isnan(reviewyear)]), np.amax(spreadyear[~np.isnan(spreadyear)&~np.isnan(reviewyear)]), 11
        x = np.r_[x1:x2:n * 1j]
        plt.plot(x, m * x + b)
    except:
        pass
    cor = stats.pearsonr(spreadyear[~np.isnan(spreadyear)&~np.isnan(reviewyear)], reviewyear[~np.isnan(reviewyear)&~np.isnan(spreadyear)])
    cor = "{0:.2f}".format(cor[0])
    plt.title(var + " --- " + cor, size = 9)

    plt.subplot(2, 1, 2)
    plt.plot(spreadelse[~np.isnan(spreadelse)&~np.isnan(reviewelse)], reviewelse[~np.isnan(reviewelse)&~np.isnan(spreadelse)], 'ro')
    try:
        m, b, rvalue, pvalue, stderror = stats.linregress(spreadelse[~np.isnan(spreadelse)&~np.isnan(reviewelse)], reviewelse[~np.isnan(reviewelse)&~np.isnan(spreadelse)])
        x1, x2, n = np.amin(spreadelse[~np.isnan(spreadelse)&~np.isnan(reviewelse)]), np.amax(spreadelse[~np.isnan(spreadelse)&~np.isnan(reviewelse)]), 11
        x = np.r_[x1:x2:n * 1j]
        plt.plot(x, m * x + b)
    except:
        pass
    cor = stats.pearsonr(spreadelse[~np.isnan(spreadelse)&~np.isnan(reviewelse)], reviewelse[~np.isnan(reviewelse)&~np.isnan(spreadelse)])
    cor = "{0:.2f}".format(cor[0])
    plt.title("everything but " + var + " --- " + cor, size = 9)

    plt.tight_layout()
    plt.show()


def fourthplot(vgarray):
    """
    asks for console name and plots that and everything sans that
    :param vgarray:
    :return:
    """
    listConsoleNames = np.sort(np.unique(vgarray['consolenames']))
    print "Please input one of the following consolenames:"
    for i in listConsoleNames:
        print i
    var = raw_input("Enter a consolenames:")
    if var not in listConsoleNames:
        print "wrong entry"
        return

    spreadconsolename = vgarray[np.where(vgarray['consolenames'] == var)]['newloosespread']
    reviewconsolename = vgarray[np.where(vgarray['consolenames'] == var)]['reviews']

    spreadelse = vgarray[np.where(vgarray['consolenames'] != var)]['newloosespread']
    reviewelse = vgarray[np.where(vgarray['consolenames'] != var)]['reviews']

    plt.figure(1)
    plt.subplot(2, 1, 1)
    plt.plot(spreadconsolename[~np.isnan(spreadconsolename)&~np.isnan(reviewconsolename)], reviewconsolename[~np.isnan(reviewconsolename)&~np.isnan(reviewconsolename)], 'ro')
    try:
        m, b, rvalue, pvalue, stderror = stats.linregress(spreadconsolename[~np.isnan(spreadconsolename)&~np.isnan(reviewconsolename)], reviewconsolename[~np.isnan(reviewconsolename)&~np.isnan(reviewconsolename)])
        x1, x2, n = np.amin(spreadconsolename[~np.isnan(spreadconsolename)&~np.isnan(reviewconsolename)]), np.amax(spreadconsolename[~np.isnan(spreadconsolename)&~np.isnan(reviewconsolename)]), 11
        x = np.r_[x1:x2:n * 1j]
        plt.plot(x, m * x + b)
    except:
        pass
    cor = stats.pearsonr(spreadconsolename[~np.isnan(spreadconsolename)&~np.isnan(reviewconsolename)], reviewconsolename[~np.isnan(reviewconsolename)&~np.isnan(reviewconsolename)])
    cor = "{0:.2f}".format(cor[0])
    plt.title(var + " --- " + cor, size = 9)

    plt.subplot(2, 1, 2)
    plt.plot(spreadelse[~np.isnan(spreadelse)&~np.isnan(reviewelse)], reviewelse[~np.isnan(reviewelse)&~np.isnan(spreadelse)], 'ro')
    try:
        m, b, rvalue, pvalue, stderror = stats.linregress(spreadelse[~np.isnan(spreadelse)&~np.isnan(reviewelse)], reviewelse[~np.isnan(reviewelse)&~np.isnan(spreadelse)])
        x1, x2, n = np.amin(spreadelse[~np.isnan(spreadelse)&~np.isnan(reviewelse)]), np.amax(spreadelse[~np.isnan(spreadelse)&~np.isnan(reviewelse)]), 11
        x = np.r_[x1:x2:n * 1j]
        plt.plot(x, m * x + b)
    except:
        pass
    cor = stats.pearsonr(spreadelse[~np.isnan(spreadelse)&~np.isnan(reviewelse)], reviewelse[~np.isnan(reviewelse)&~np.isnan(spreadelse)])
    cor = "{0:.2f}".format(cor[0])
    plt.title("everything but " + var + " --- " + cor, size = 9)

    plt.tight_layout()
    plt.show()

def main():
    root = Tk()
    root.withdraw()
    openfilename = askopenfilename(filetypes = [("csv", "*.csv")], parent = root, title = "Please select vgprice csv ")
    root.destroy()

    VgpriceList = []

    try:
        vgFile = open(openfilename, 'r')
        try:
            vgFile.readline()
            for line in vgFile:
                args = line.rstrip("\n").split(",")
                c = vgprice.vgpriceObj(*args)
                #print c
                VgpriceList.append(c)
        finally:
            vgFile.close()
    except IOError:
        print "file does not exist"
        return

    reviewscores = np.array(getelements(VgpriceList, 'score'))
    genres = np.array(getelements(VgpriceList, 'genre'))
    years = np.array(getelements(VgpriceList, 'year'))
    consolenames = np.array(getelements(VgpriceList, 'consolename'))
    looseprices = np.log(np.array(getelements(VgpriceList, 'looseprice'), dtype = np.float))
    cibprices = np.log(np.array(getelements(VgpriceList, 'cibprice'), dtype = np.float))
    newprices = np.log(np.array(getelements(VgpriceList, 'newprice'), dtype = np.float))
    newloosespread = newprices - looseprices

    vgarray = createstructarray(looseprices, cibprices, newprices, reviewscores, genres, years, consolenames,
                                newloosespread)



    firstplot(vgarray)
    secondplot(vgarray)
    thirdplot(vgarray)
    fourthplot(vgarray)

if __name__ == '__main__':
    main()