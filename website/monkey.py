from webscraper import GetAlbum

searches = [
    "Monkey buisness black eyed peas",
    "The E.N.D.",
    "Elephunk",
    "The Beginning deluxe"
    ]

for search in searches:
    print(GetAlbum(search)['songs'])