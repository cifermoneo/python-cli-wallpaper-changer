from email.policy import default
from operator import index
import click
import json
import random
import ctypes
from bs4 import BeautifulSoup
import requests
import datetime
import os, ctypes,re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import base64
import re
FOLDER_NAME = "wiki"
DB_DIR = "db"
IMG_DIR = "images"
def setWallpaper(file_path,is_full_path=None):
    if(not is_full_path):
        file_path = os.path.join(os.path.dirname(__file__),file_path)
    print(file_path)
    ctypes.windll.user32.SystemParametersInfoW(20, 0, file_path , 0)
    # print("Wallpaper set to : " + file_path)

def valid_file_name(file_name):
    return re.sub('[^\w_.)( -]', '', file_name)

def ScreenshotForUrl(URL = "https://en.wikipedia.org/wiki/Special:Random"):
    opt = Options()
    opt.headless = True
    opt.add_argument("window-size=1920,1080");
    opt.add_argument("--hide-scrollbars")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=opt)
    # driver.maximize_window()
    driver.get(URL)
    if not os.path.exists(FOLDER_NAME):
        os.makedirs(FOLDER_NAME)
    fileName = os.path.join(FOLDER_NAME , valid_file_name(driver.title)) + ".png"
    driver.save_screenshot(fileName)
    holdUrl = driver.current_url
    driver.close()
    return (holdUrl,fileName)

CONST = {
    "url" : "https://wallpapersden.com/"
}
# imgs_links = { }


def byExtensions(exts):
    files = os.listdir()
    back_limit = len(max(exts))
    temp = []
    for f in files:
        if f[-back_limit:] in (exts):
            temp.append(f)
    return temp

def getCats():
    response = requests.get(CONST["url"])
    bsObj = BeautifulSoup(response.content, "html.parser")
    a = bsObj.find_all("div", {"class": "bg-accent"} )
    return [CONST["url"][:-1] + l["href"] for l in a[1].find_all("a")][1:]

def indexImgsForCat(cat_link,imgs_links):
    response = requests.get(cat_link)
    bsObj = BeautifulSoup(response.content, "html.parser")
    allImages = [CONST["url"][:-1] + a["href"] for a in bsObj.select(".surface")[1].select("figure > a")]
    for l in allImages:
        imgs_links[l] = str(datetime.datetime.now())

def downloadImgAndSet(img_link):
    response = requests.get(img_link)
    bsObj = BeautifulSoup(response.content, "html.parser")
    img_url = bsObj.select('[itemprop="contentUrl"]')[0]["href"]
    img_res = requests.get(img_url)
    with open("temp.jpg","wb+") as f:
        f.write(img_res.content)
    print("Image written, setting wallpaper")
    setWallpaper("temp.jpg")

def createFolders():
    os.chdir(os.path.dirname(__file__))
    if not (os.path.exists(DB_DIR)):
        os.mkdir(DB_DIR)
    if not (os.path.exists(IMG_DIR)):
        os.mkdir(IMG_DIR)

@click.group()
def cli():
    pass

# @cli.command()
# def bg():
#     linksObj = {}
#     if "fixture.db" in os.listdir():
#         imgs = ""
#         with open("fixture.db") as f:
#             imgs = json.loads(f.read())
#             downloadImgAndSet(random.choice(list(imgs.items()))[0])
#     else:
#         cats = getCats()
#         for c in cats:
#             indexImgsForCat(c,linksObj)
#         with open("fixture.db", "w+") as f:
#             json.dump(linksObj,f)
#         print("created_db")

def setWallpaperFromFile(query,filename):
    pathToFile = os.path.join(os.path.dirname(__file__),IMG_DIR)

    imgs = ""
    with open(os.path.join(os.path.dirname(__file__),DB_DIR,filename)) as f:
        imgs = json.loads(f.read())
        if not os.path.exists(os.path.join(pathToFile, query)):
            os.makedirs(os.path.join(pathToFile, query))
        url = random.choice(list(imgs.items()))[0]
        imageFileName = os.path.join(pathToFile , query, url.replace("/","").replace("https:wallpapersden.com","") + ".png" )
        if(os.path.exists(imageFileName)):
            click.echo(click.style('>> Image already Downloaded !!!', fg='red'))
        else:
            response = requests.get(url)
            bsObj = BeautifulSoup(response.content, "html.parser")
            img_url = bsObj.select('[itemprop="contentUrl"]')[0]["href"]
            img_res = requests.get(img_url)
            with open(imageFileName,"wb+") as f:
                f.write(img_res.content)
            click.echo(click.style('>> Image Succesfully Downloaded', fg='green'))
        setWallpaper(imageFileName)

def createDatabaseForQuery(query, limit, filename, linksObj):
    pathToFile = os.path.join(os.path.dirname(__file__),DB_DIR,filename)
    repeat = True
    i = 0
    while repeat:
        if(limit - 1 >= 0 and limit == i):
            break
        print(f'Queried >> https://wallpapersden.com/search?q={query}&page={i}')
        response = requests.get(f'https://wallpapersden.com/search?q={query}&page={i}')
        bsObj = BeautifulSoup(response.content, "html.parser")
        if(len(bsObj.select(".surface")) <= 1):
            repeat = False
            continue
        else:
            allImages = ["https://wallpapersden.com/"[:-1] + a["href"] for a in bsObj.select(".surface")[1].select("figure > a")]
            for l in allImages:
                linksObj[l] = str(datetime.datetime.now())
        i += 1
    with open(pathToFile, "w+") as f:
        json.dump(linksObj,f)
    print("created_db > " + filename)

@cli.command()
@click.option('--query', prompt='Search Term',help='Specify Search term for scraping')
@click.option('--limit', default=-1, help='Limit for scraping')
def scrap(query,limit):
    createFolders()
    filename = valid_file_name(query) + ".db"
    linksObj = {}
    try:
        limit = int(limit)
    except Exception as e:
        print("You piece of shite!!!, asked for a number as :) LIMIT")
        return
    if limit == -1:
        if os.path.exists(os.path.join(DB_DIR, filename)):
            setWallpaperFromFile(query,filename)
            return
        else:
            createDatabaseForQuery(query,limit,filename,linksObj)
            setWallpaperFromFile(query,filename)
            return
    elif limit >= 1:
        createDatabaseForQuery(query,limit,filename,linksObj)
        setWallpaperFromFile(query,filename)
        return
    else:
        print("Limit is shite mate")



@cli.command()
@click.option('--setwall', default=False, is_flag=True)
def wiki(setwall):
    (link, file) = ScreenshotForUrl()
    pathToFile = os.path.join(os.path.dirname(__file__),file)
    if (setwall):
        setWallpaper(pathToFile,True)
    print("Screenshot : \"%s\"" % pathToFile)
    print("Article Link : %s" % link)


if __name__ == "__main__":
    cli()