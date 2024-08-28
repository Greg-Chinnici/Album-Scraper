from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.wpewebkit.webdriver import WebDriver
from defaultAlbums import defaultsearches as defaults
import random

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('log-level=1') # so it wont print warnings from websites being mad at headless browsers

class Album:

    Name :str = ""

    Artist :str = ""

    Year :str = ""

    CoverLink :str = ""

    Songs :list = []

    def info(self) ->str:
        return f"{self.Name} by {self.Artist} in {self.Year}"

    def all(self) ->str:
        return f"{self.info()} \n {self.CoverLink} \n {self.Songs}"

    def removeParens(self, string) ->str:
        result = ""
        parentheses_count = 0
        for char in string:
            if char == '(':
                parentheses_count += 1
            elif char == ')':
                parentheses_count -= 1
            elif parentheses_count == 0:
                result += char
        result += " " # if parentheses_count != 0 else " "
        return result

    def songs(self , includeParenthese = True) ->list:
        return [(self.removeParens(song) if includeParenthese == False else song) for song in self.Songs]

    def __str__(self):
        return self.info() + "\n" + ''.join(self.songs(False))

    def ToDictionary(self) ->dict:
        return {
        "name": self.Name,
        "artist": self.Artist,
        "year": self.Year,
        "cover": self.CoverLink,
        "songs": self.Songs
        }

def formatForLink(searchString):
    return searchString.replace(' ', "%20")

def GetAlbum(searchTerm:str) ->dict:
    """
    input:
        searchTerm (string): name and artist is enough
    return:
        dictionary of the album data. Defined in Album.ToDictionary
    """
    #? you are at the mercy of spotifys SEO for albums
    #? maybe add a selector that gives the top 3 from the search
    term = formatForLink(searchTerm)
    searchWebsite = f"https://open.spotify.com/search/{term}/albums"

    driver = webdriver.Chrome(options);
    albumLink = findAlbumLink(searchWebsite, driver)

    # once it gets past here, it is definetly a valid album. sometimes the wrong one. so give list of alternative options

    ChosenAlbum = Album()
    driver.get(url = albumLink)

    ChosenAlbum.CoverLink = GetCoverLink(driver)
    print(ChosenAlbum.CoverLink)
    info = GetInfo(driver)
    ChosenAlbum.Artist = info[0]
    ChosenAlbum.Year = info[1]
    ChosenAlbum.Name = info[-1]

    ChosenAlbum.Songs = GetSongs(driver)

    driver.quit()

    return ChosenAlbum.ToDictionary()

def findAlbumLink(website :str, driver) ->str:
    driver.get(website)

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH ,'(((//div[@data-testid="grid-container"])[2])//a)[1]')))
    return str(element.get_attribute('href'))

def GetSongs(driver):
    songElements = driver.find_elements(By.XPATH , '(//a[@data-testid="internal-track-link"]//div)')
    return [e.text for e in songElements]

def GetCoverLink(driver):
    img = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH , "(//img)[1][@loading='lazy']")))
    srcset = str(img.get_attribute('srcset'))
    return srcset.split(',')[-1].strip().split(" ")[0]


def GetInfo(driver):
    titleElement = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "//span[@data-testid='entityTitle']/h1")))
    title = titleElement.text;

    infoElements = driver.find_elements(By.XPATH, "//span[@data-testid='entityTitle'][1]/following-sibling::div//*[text()]")
    i = [e.text for e  in infoElements]
    i.append(title)

    return i

d = GetAlbum("Lil Tecca")
print(d)
print(d["cover"])
