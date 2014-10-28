from random import Random


class Graph:
    alpha = 3
    beta = 2
    rho = 0.01
    Q = 2.0

    initial_pheromone = 0.01

    def __init__(self, cities_distances):
        self.random_generator = Random()

        self.cities_distances = cities_distances
        self.cities_count = len(cities_distances)
        self.pheromone_matrix = [[self.initial_pheromone for _ in range(self.cities_count)] for _ in
                                 range(self.cities_count)]

    def choose_city(self, present_city, visited_cities):
        paths_attractiveness = []

        for city in range(self.cities_count):
            if city == present_city or city in visited_cities:
                paths_attractiveness.append(0.0)
            else:
                paths_attractiveness.append(self.__calculate_path_attractiveness(present_city, city))

        paths_probability = self.__calculate_path_probability(paths_attractiveness)
        value = self.random_generator.random()

        for city in range(self.cities_count):
            if paths_probability[city] <= value < paths_probability[city + 1]:
                return city

        raise RuntimeError("City not found")

    def calculate_total_distance(self, cities):
        total_distance = 0

        for i in range(len(cities) - 1):
            city_from = cities[i]
            city_to = cities[i + 1]

            total_distance += self.__distance(city_from, city_to)

        return total_distance

    def update_pheromones(self, ants):

        for i in range(self.cities_count):
            for j in range(self.cities_count):
                for ant in ants:
                    increase = 0.0
                    decrease = (1.0 - self.rho) * self.__pheromone(i, j)
                    if ant.contains_connection(i, j):
                        increase = (self.Q / ant.distance)

                    self.__update_pheromone(i, j, increase + decrease)

    def __calculate_path_attractiveness(self, city_from, city_to):
        distance = self.__distance(city_from, city_to)
        pheromone = self.__pheromone(city_from, city_to)

        return (pheromone ** self.alpha) * ((1.0 / distance) ** self.beta)

    @staticmethod
    def __calculate_path_probability(paths_attractiveness):
        attractiveness_sum = sum(paths_attractiveness)

        paths_probability = []
        for i in range(len(paths_attractiveness)):
            paths_probability.append(paths_attractiveness[i] / attractiveness_sum)

        converted_form = [0.0]
        for probability in paths_probability:
            converted_form.append(converted_form[-1] + probability)

        return converted_form

    def __distance(self, city_from, city_to):
        return self.cities_distances[city_from][city_to]

    def __pheromone(self, city_from, city_to):
        return self.pheromone_matrix[city_from][city_to]

    def __update_pheromone(self, city_from, city_to, val):
        self.pheromone_matrix[city_from][city_to] = val