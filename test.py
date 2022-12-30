from  wallpaper_den import downloadImgAndSet,getCats,indexImgsForCat
import os
import random
import datetime
import json
from bs4 import BeautifulSoup
from utils import setWallpaper
import requests
CONST = {
    "url" : "https://wallpapersden.com/search?q=naruto&page=12"
}

linksObj = {}
# indexImgsForCat(CONST["url"],linksObj)
response = requests.get(CONST["url"])
bsObj = BeautifulSoup(response.content, "html.parser")
if(len(bsObj.select(".surface")) > 1):
    allImages = ["https://wallpapersden.com/"[:-1] + a["href"] for a in bsObj.select(".surface")[1].select("figure > a")]
    for l in allImages:
        linksObj[l] = str(datetime.datetime.now())
print(linksObj)