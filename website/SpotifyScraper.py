from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.wpewebkit.webdriver import WebDriver
from defaultAlbums import defaultsearches as defaults
import random

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('log-level=1') # so it wont print warnings from websites being mad at headless browsers

class Album:

    Name = ""

    Artist = ""

    Year = ""

    CoverLink = ""

    Songs = []

    def info(self):
        return f"{self.Name} by {self.Artist} in {self.Year}"

    def all(self):
        return f"{self.info()} \n {self.CoverLink} \n {self.Songs}"

    def removeParens(self, string):
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

    def songs(self , includeParenthese = True):
        return [(self.removeParens(song) if includeParenthese == False else song) for song in self.Songs]

    def __str__(self):
        return self.info() + "\n" + ''.join(self.songs(False))

    def ToDictionary(self):
        return {
        "name": self.Name,
        "artist": self.Artist,
        "year": self.Year,
        "cover": self.CoverLink,
        "songs": self.Songs
        }

def formatForLink(searchString):
    return searchString.replace(' ', "%20")

def GetAlbum(searchTerm:str):
    """
    input:
        searchTerm (string): name and artist is enough
    return:
        dictionary of the album data. Defined in Album.ToDictionary
    """
    #? you are at the mercy of spotifys SEO for albums
    #? maybe add a selector that gives the top 3 from the search
    term = formatForLink(searchTerm)
    searchWebsite = f"https://open.spotify.com/search/{searchTerm}/albums"

    driver = webdriver.Chrome(options);

    albumLink = findAlbumLink(searchWebsite, driver)

    # once it gets past here, it is definetly a valid album. sometimes the wrong one. so give list of alternative options

    ChosenAlbum = Album()

    driver.get(url = albumLink)

    ChosenAlbum.CoverLink = GetCoverLink(driver)

    info = GetInfo(driver)
    ChosenAlbum.Name = info[0]
    ChosenAlbum.Artist = info[1]
    #info[2] is the Genre
    ChosenAlbum.Year = info[3]

    ChosenAlbum.Songs = GetSongs(driver)

    driver.quit()

    return ChosenAlbum.ToDictionary()

def findAlbumLink(website :str, driver):
    driver.get(website)

    element = driver.find_element(By.XPATH ,"(((//div[@data-testid='grid-container'])[2])//a)[1]")
    link = element.get_attribute('href')
    return "https://open.spotify.com/album/" + link

def GetSongs(driver):
    songElements = driver.find_elements(By.XPATH , '(//a[@data-testid="internal-track-link"]//div)')
    return [e.text for e in songElements]

def GetCoverLink(driver):
    img = driver.find_element(By.XPATH , "$x((//img)[1]))")
    srcset = img.get_attribute('srcset')
    return srcset.split(',')[-1].split(' ')[0]

def GetInfo(driver):
    return "No Info"
