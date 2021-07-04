from bs4 import BeautifulSoup
import time
import requests
import json


class Player:

    def __init__(self,year, tr):

        self.rank = int(tr.select('.rank')[0].text)

        self.position = tr.select('.teamposition')[0].text
        self.team = tr.select('.team')[0].text
        self.age_class = tr.select('.class')[0].text

        self.profile_link = tr.select('a')[0]['href']

        self.first_name = tr.select('a span')[0].text
        self.last_name = tr.select('a span')[1].text
        self.image_link = tr.select('.name img')[0]['src']

        self.year = year


    def __repr__(self):
        return json.dumps(self.__dict__, indent=2)

    def __dict__(self):
        return {
            'year': self.year,
            'rank': self.rank,
            'team': self.team,
            'age_class': self.age_class,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'position': self.position,
            'image_link': self.image_link,
            'profile_link': self.profile_link,
        }

base_big_board_url = 'https://www.nbadraft.net/ranking/bigboard/?year-ranking=$[year]'

player_list = []

for year in range(2008, 2022):
    print('Parsing', year)
    big_board_url  = base_big_board_url.replace('$[year]', str(year))

    source = requests.get(big_board_url)

    soup = BeautifulSoup(source.content,'html.parser')

    for tr in soup.select('.big-board-table tbody tr'):
        player_list.append(Player(year, tr))

    time.sleep(10)



def create_json():
    json_string = json.dumps([player.__dict__() for player in player_list], indent=2)
    file = open("player_data.json", "w")
    file.write(json_string)

create_json()
