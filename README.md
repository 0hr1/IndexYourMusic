# IndexYrMusic

## What is this
RYM doesn't have an api, and it doesn't seem like they're planning on implementing one anytime soon... :(
I wanted to sort releases that ive rated on rym by descriptor and noticed that there was no feature to do this so i wrote this script to scrape, and then index music ive rated by things like genre, descriptor etc.

## How to use
clone, install requirements `pip install -r requirements.txt`, i wrote and used this with py3.11 but i feel like itll work for any python thats not ancient

__requirements__:
* flask
* bs4
* selenium
* numpy
* tqdm
* dateutil


`python main.py --scrape` with your username and startrating-endrating range to scrape and save everything to an output file (_links.json_ has the links to all the releases scraped, and _release_data.json_ has the data itself). 
this step may take up to a few hours depending on how many releases you've rated. I put in sleeps, you can feel free to switch them up depending on how polite (and how brave) you're feeling

`python main.py --display` to throw the website up at localhost:5000
enjoy the breathtaking uiux


## TODO
i wrote this over the course of a few days, its not the prettiest and its one of the first times ive done something like this so there are definitely some things that could be done better.
heres a list of things that i wanna add to the project if i ever have time to

__technical__:
- better file structure (split up files into two folders display and scrape) 
- make this project a module

__scraping features__:
- get rym ranking
- add rym url to release_data json
- add recover feature in case of crash while scraping

__display features__:
- sort by secondary genres (for now genres searches both)
- sort by multiple descriptors/genres and make it so not all have to appear
- sort with subdescriptors / subgenres eg Rock will show releases with all Rock subgenres.
- let user decide how to make the releases appear? (as in release - artist - rating) etc
- let users write booleans for their searches with complicated ors and ands


## also
shoutout to https://github.com/dbeley/rymscraper , tons of inspiration taken from them

## um
this technically goes against ryms TOS, use at ur own risk
i put a bunch of sleeps throughout the program so as to not be ip banned (im a scaredy cat) feel free to shorten or lengthen them idc
also pls donate to rym if you can, its one of the coolest and most useful websites on the internet they deserve the money

