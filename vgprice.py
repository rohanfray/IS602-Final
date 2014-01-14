__author__ = 'Rohan'

import unirest
import json
from datetime import datetime


class vgpriceObj(object):
    METACRITICPLATFORMDICTIONARY = {"Playstation": 10, "Playstation 3": 1, "GameBoy Advance": 11, "Gamecube": 13,
                                    "Nintendo 3DS": 16, "Nintendo 64": 14, "Nintendo DS": 4, "Playstation 2": 6,
                                    "PlayStation Vita": 67365, "PSP": 7, "Sega Dreamcast": 15, "Wii": 8, "Wii U": 68410,
                                    "Xbox": 12, "Xbox 360": 2}



    def getMetacriticAttr(self):
        try:
            response = unirest.post("https://byroredux-metacritic.p.mashape.com/find/game",

                                    headers = {
                                        "X-Mashape-Authorization": "W4On1vsJD1QaVnNRJrSyEyW4PMXvHfTd"
                                    },
                                    params = {
                                        "title": self.productname,
                                        "platform": self.METACRITICPLATFORMDICTIONARY[self.consolename]
                                    }
            );

            d = json.loads(json.dumps(response.body))

            d = d['result']

            self.score = int(d[r'score'])
            self.rating = d[r'rating']
            self.publisher = d[r'publisher']
            self.developer = d[r'developer']
        except:
            self.score = None
            self.rating = None
            self.publisher = None
            self.developer = None

    def __init__(self, id, consolename, productname, looseprice, cibprice, newprice, genre, releasedate):
        self.id = id
        self.consolename = consolename
        self.productname = productname

        if looseprice == "":
            self.looseprice = None
        else:
            self.looseprice = float(looseprice.strip("$"))

        if cibprice == "":
            self.cibprice = None
        else:
            self.cibprice = float(cibprice.strip("$"))

        if newprice == "":
            self.newprice = None
        else:
            self.newprice = float(newprice.strip("$"))

        self.genre = genre

        if releasedate == "":
            self.releasedate = None
            self.year = None
        else:
            self.releasedate = datetime.strptime(releasedate, '%m/%d/%Y')
            self.year = self.releasedate.year

        self.getMetacriticAttr()

    def __str__(self):
        return self.id + " " + str(self.looseprice) + " " + str(self.cibprice) + " " + str(self.newprice) + " " + \
               str(self.releasedate.year)

