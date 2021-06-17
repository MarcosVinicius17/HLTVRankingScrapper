import requests
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup
import cloudscraper
import re
import shutil

from requests.sessions import session

number = input("Type a number from 1 to 30: ")

if int(number) < 1 or int(number) > 30:
    print("Ops, Ptilopsis says 'Error'!")
else:

    ranking = "#" + number
    print("You are looking for the team on raking ", ranking)

    scraper = cloudscraper.create_scraper()  # returns a CloudScraper instance
    mySite = scraper.get("https://www.hltv.org/ranking/teams/2021/june/14").text

    #print(scraper.get("https://www.hltv.org/ranking/teams/2021/june/7").text)
    #print(mySite)

    #Write the content to a html file. All content is there, but the CSS is lacking
    f = open("./project_hltv_ranking/page.html","w+",encoding = "utf-8")
    f.write(mySite)


    with open("./project_hltv_ranking/page.html","r",encoding = "utf-8") as s:
        soup = BeautifulSoup(s,"html.parser")
        

    #Collecting some info
    #This will result in <title>CS:GO Ranking | World Ranking | HLTV.org</title>
    #print("Title: ", soup.title)

    #This will result in CS:GO Ranking | World Ranking | HLTV.org
    #print("Title: ", soup.title.string)

    #Extract ALL the text
    #print(soup.get_text())


    #Cycles through the .html finding all the elements called position from the 
    #type span. If the element contain the ranking, use the method find_all
    #and return the LAST element. 
    #Example: for team #5, he gets the first 5 results and print the last, who
    #will be the 5th team.
    #This is not the best way, but if works, it works.
    #To see ONLY the text from an item, use the "".text"
    for i in soup.find_all("span",{"class": "position"}):
        if ranking in i:
            teamNames = soup.find_all("span",{"class":"name"},limit = int(number))
           # print(teamNames)
            teamName = teamNames[-1]
            print("The ", ranking, "team is:",teamName.text)
    #NOW, DO THE REST TO GET THE PLAYERS NAMES AND THE IMAGE LOGO!

    #Get all players names agrouped by team
    #for k in soup.find_all("div",{"class": "playersLine"},limit = int(number)):
    playerList = soup.find_all("div",{"class": "playersLine"},limit = int(number))
           # playersNames = soup.find_all("div",{"class":"rankingNicknames"}, limit=int(number))
           # print(k.text)
    players = playerList[-1]
    print(teamName.text, " has the following players:")
    print(players.text)


    #Get the team logo. First, we need the image url
    teamLogos = soup.find_all("img")

    for image in teamLogos:
        if image.has_attr('alt'):
            if image['alt'] == teamName.text:
                #print(image['src'])
                teamLogoUrl = image['src']
                #print("The team logo is available at: ", teamLogoUrl)
                #I only need one URL.
                break

    #Now, lets save the image
   #logoUrl = requests.get(teamLogoUrl)
    

    #print("Getting image from")
    #print(teamLogoUrl)
    
    #Looks like the link is from a .svg file. But when i try to access,
    #it returns me a 503, meaning Service Unavailable.
    #Guess this is it. 
    
    #image = Image.open(BytesIO(logoUrl.content))




