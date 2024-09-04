from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Album import Album
from urllib import parse
import random
from defaultAlbums import defaultsearches as defaults
from SeleniumDriver import CreateDriver


def GetAlbum(searchTerm: str):
    term = parse.quote(searchTerm)
    driver = CreateDriver()

    if len(searchTerm) < 3:
        searchTerm = random.choice(defaults)
    term = parse.quote(searchTerm)

    link = f"https://soundcloud.com/search/albums?q={term}"
    albumLink = findAlbumLink(driver, link)
    ChosenAlbum = Album()

    driver.get(url=albumLink)

    ChosenAlbum.Songs = GetSongs(driver)
    info = GetInfo(driver)
    ChosenAlbum.Name = info[0]
    ChosenAlbum.Artist = info[1]
    ChosenAlbum.Year = info[2]

    ChosenAlbum.CoverLink = GetCoverLink(driver)

    driver.quit()
    return ChosenAlbum.ToDictionary()


def findAlbumLink(driver, link: str) -> str:
    driver.get(url=link)
    e = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "(//a[@class='sound__coverArt'])[1]"))
    )
    return str(e.get_property("href"))


def GetSongs(driver):
    e = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located(
            ((By.XPATH, "//div[contains(@class , 'trackItem__content')]/a"))
        )
    )
    return [ele.text for ele in e]


def GetInfo(driver):
    y = driver.find_element(
        By.XPATH, "//dd[@class='listenInfo__releaseData sc-text-secondary']"
    )
    year = y.text.split(" ")[-1]

    a = driver.find_element(
        By.XPATH, "//div[@class='soundTitle__usernameHeroContainer']/h2/a"
    )
    artist = a.text.replace("Verified", "")

    n = driver.find_element(
        By.XPATH, "//div[@class='soundTitle__titleHeroContainer']//span"
    )
    name = n.text
    return [name, artist, year]


def GetCoverLink(driver):
    s = driver.find_element(By.XPATH, "//div[@class= 'fullHero__artwork']//span")
    style = str(s.get_attribute("style"))

    return style.split('url("')[1].split('");')[0]
