# Poster Thing

## This is a website that scrapes data to generate posters for music albums

- orginally I made the scraper in c#
- now it is made in python using headless selenium, the goal is the have the python on a server and return relevant info to the user
- it gets all the songs from the <li> and <ul> things
- all hte images are just refrencing the static links used by the websites

## Although it is better for it to be in python or js to be more compatible with my web stack

- I am a gamedev and take no responsibilty for the awful web creations you see above
- my plan was to just get the src for the covers so all the image loading would be client side, and I just pass a few hundred bytes of strings

### The C# version is using interfaces becuase I wanted it to be flexible to changes

- maybe apple changes some things, and I can jsut hotswap to a spotify or soundcloud scraper.

### This is basically my first actual web based project, everything else is console or Unity

- as I was making this I learned how to properly usee XPATH. its basically regex for html DOM.

#### Notes:

- some artists dont post to apple music, thats why i want to have different interfaces
- Working on making it work with YouTube Music now
