import csv
import pygame
import os
import sys
import queue
from pygame import draw

MAK_CONTAMINATION = 4
IMAGE_W = 1357
IMAGE_H = 628
VIRUS_COLORS = [(10, 10, 10), (0, 10, 245), (255, 255, 0), (255, 0, 0)]
CONTAMINATION_COLOR = (0, 100, 0)
STATION_COLOR = (225, 255, 255)
CITY_RADIUS = 10


def load_cities():
    cities = []
    with open('cities.csv', encoding="utf8") as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='"')
        for record in reader:
            num = int(record[0]) - 1
            name = record[1]
            cords = (int(record[2]), int(record[3]))
            virus = int(record[4]) - 1
            cities.append(Town(num, name, cords, virus))
    return cities


def load_cities_graph():
    graph = []
    with open('graph.csv', encoding="utf8") as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='"')
        for record in reader:
            c_1 = int(record[0]) - 1
            c_2 = int(record[1]) - 1
            graph.append((c_1, c_2))
    return graph


class Town:
    def __init__(self, num, name, cords, virus):
        self.num = num
        self.name = name
        self.cords = cords
        self.virus = virus

        self.players = set()
        self.station = True
        self.contamination = 4
        self.neighbors = set()

    def take_num(self):
        return self.num

    def take_name(self):
        return self.name

    def take_cords(self):
        return self.cords

    def take_virus(self):
        return self.virus

    def add_player(self, player):
        self.players.add(player)

    def del_player(self, player):
        self.players.discard(player)

    def is_station(self):
        return self.station

    def build_station(self):
        self.station = True

    def infection(self):
        if self.contamination == MAK_CONTAMINATION:
            return False
        self.contamination += 1
        return True

    def take_contamination(self):
        return self.contamination

    def take_players(self):
        return self.players

    def add_neighbor(self, city):
        self.neighbors.add(city)

    def take_neighbors(self):
        return self.neighbors


class Game:
    def __init__(self, players):
        self.players = players
        self.cities = dict()
        cities_list = load_cities()
        for city in cities_list:
            num, name, cords, virus = city
            self.cities[name] = Town(num, name, cords, virus)
        for c_1, c_2 in load_cities_graph():
            name_1, name_2 = cities_list[c_1][1], cities_list[c_2][1]
            self.cities[name_1].add_neighbor(self.cities[name_2])
            self.cities[name_2].add_neighbor(self.cities[name_1])

    def get_element(self, x, y):
        for city in self.cities.values():
            cords = city.take_cords()
            dist = ((cords[0] - x) ** 2 + (cords[1] - y) ** 2) ** 0.5
            if dist <= CITY_RADIUS:
                return city

    def outbreak(self, start_city):
        infected = queue.Queue()
        infected.put(start_city)
        used = [False] * len(self.cities.values())
        used[start_city.take_num()] = True
        while not infected.empty():
            city = infected.get()
            for neig in city.take_neighbors():
                if not used[neig.take_num()]:
                    used[neig.take_num()] = True
                    if not neig.infection():
                        infected.put(neig)


def new_card(screen, image, cities, graph):
    screen.blit(image, (0, 0))
    for city in cities:
        x, y = city.take_cords()
        draw.circle(screen, VIRUS_COLORS[city.take_virus()], (x, y), 15)
        if city.is_station():
            draw.polygon(screen, STATION_COLOR,
                         ((x + 5, y), (x + 5, y - 7), (x + 7 + 5, y - 14), (x + 19, y - 7), (x + 19, y)))
        for i in range(city.take_contamination()):
            draw.circle(screen, CONTAMINATION_COLOR, (x - 10 - ((i + 1) % 2) * 9, y + (i // 2) * 9 + 2), 4)


def main():
    pygame.init()
    size = IMAGE_W, IMAGE_H
    screen = pygame.display.set_mode(size)
    image = load_image('2.png')
    screen.blit(image, (0, 0))
    pygame.display.flip()
    cities = load_cities()
    graph = load_cities_graph()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        new_card(screen, image, cities, graph)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()
