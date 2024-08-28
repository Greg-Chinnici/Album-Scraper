from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.wpewebkit.webdriver import WebDriver
from defaultAlbums import defaultsearches as defaults
import random
from Album import Album
from urllib import parse




options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('log-level=1') # so it wont print warnings from websites being mad at headless browsers



def formatForLink(searchString):
    return searchString.replace(' ', "%20")

#? sometimes it just breaks, not sure if it is the driver crashing or timing out
def GetAlbum(searchTerm:str):
    """
    input:
        searchTerm (string): name and artist is enough
    return:
        dictionary of the album data. Defined in Album.ToDictionary
    """
    #? you are at the mercy of Apple's SEO for albums, sometimes it will give the deluxe versions
    #? maybe add a selector that gives the top 3 from the search
    term = parse.quote(searchTerm)
    searchWebsite = f"https://music.apple.com/us/search?term={term}"

    driver = webdriver.Chrome(options);

    albumLink, altLinks = findAlbumLink(searchWebsite, driver)
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

    no_results_elements = driver.find_elements(By.XPATH, "//*[text()='No Results' or text()='Try a new search.']")
    if len(no_results_elements) == 2 or len(website.split("/")[-1]) == len("search?term="):
        link = "https://music.apple.com/us/search?term="+parse.quote(random.choice(defaults))
        driver.get(link)

    # product lockup is only on the albums, so pick the first one and take the link. xpaths are not zero indexed
    # doing xpath so i can move it to other scrapers or langauges if i need to
    # grabs the first <a> with product_lockup and then takes the href value of the element. this is the link to the album page
    # if it is detected as useless, search from some random defaults
    albumlinkElements = driver.find_elements(By.XPATH ,"(//a[@data-testid='product-lockup-link'])[position()<4]")
    alternateLinks = [element.get_attribute('href') for element in albumlinkElements]

    #altNames = [l.split('/')[-2].replace('-',' ') for l in alternateLinks]
    albumlink :str= alternateLinks[0]
    return albumlink, alternateLinks



def GetCoverLink(driver):
    source = driver.find_element(By.XPATH , "(//picture)[2]/source[2]")
    srcset = source.get_attribute('srcset')
    return srcset.split(',')[-1].split(' ')[0]


def GetInfo(driver):
    texts = driver.find_element(By.XPATH , "//div[@data-testid='container-detail-header']")

    text = texts.text.split("Preview")[0] # get everything before 'Preview'

    def rep(s:str , old:list , new:str):
        # replace with anything in list
        for d in old:
            s = s.replace(d,new)
        return s

    text = rep(text , ["\u2004·\u2004" , "\n"], "^")
    return text.split("^")



def GetSongs(driver):
    songElements = driver.find_elements(By.XPATH , "//div[@data-testid='track-title']")
    return [e.text for e in songElements]
