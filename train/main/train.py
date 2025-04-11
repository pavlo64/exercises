import logging
import sys
from abc import ABC, abstractmethod

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

class Train:
    def __init__(self, name: str):
        self.name = name
        self.wagons = []

    def __repr__(self):
        wagon_list = ""
        i =1
        for wagon in self.wagons:
            wagon_list += f" {i}. {wagon} \n"
            i+=1
        return f"Train name = {self.name} \nWagons:\n{wagon_list}"

    def create_wagon(self, wagon_type, *args, **kwargs):
        wagon = wagon_type(*args, **kwargs)
        return wagon

    def add_wagon(self, wagon):
        self.wagons.append(wagon)
        self.enough_baggage_check()

    def all_wagons_type_check(self) -> bool:
        required_wagon_types = {Locomotive, SeatedWagon, SleepingWagon, RestaurantWagon, LuggageWagon}
        wagon_types_in_train = {type(wagon) for wagon in self.wagons}
        return required_wagon_types.issubset(wagon_types_in_train)

    def locomotive_check(self) -> bool:
        return isinstance(self.wagons[0], Locomotive)

    def train_power_check(self, train_weight: int = 0) -> bool:
        locomotive = next((wagon for wagon in self.wagons if isinstance(wagon, Locomotive)), None)
        power = locomotive.power
        for wagon in self.wagons:
            train_weight += wagon.weight
        return power < train_weight

    def enough_baggage_check(self, all_passengers: int = 0, all_baggage: int = 0) -> None:
        for wagon in self.wagons:
            if isinstance(wagon, (SeatedWagon, SleepingWagon, RestaurantWagon)):
                all_passengers += wagon.passengers
            elif isinstance(wagon, LuggageWagon):
                all_baggage += wagon.baggage
        if all_passengers > all_baggage:
            luggage = self.create_wagon(LuggageWagon)
            self.wagons.append(luggage)

    def start(self) -> None:
        if not self.all_wagons_type_check():
            logging.info('Not all wagons type are present')
        if self.train_power_check():
            logging.info('Not enough power to run train')
        if not self.locomotive_check():
            logging.info('Locomotive should be at first position in the train')
        else:
            logging.info('Train is ready to go')


class Wagon(ABC):
    def __init__(self, passengers:int, seats:int, weight: int, baggage:int):
        self.weight = weight
        self.passengers = passengers
        self.baggage = baggage
        self.seats = seats

    def validate_passengers(self):
        if self.passengers > self.seats:
            raise ValueError(
                f"Too many passengers: {self.passengers}. Max seats available: {self.seats}"
            )

    @abstractmethod
    def __repr__(self):
        pass



class Locomotive(Wagon):
    def __init__(self, power:int):
        super().__init__(passengers=0, seats=0, weight=10, baggage=0)
        self.power = power
        if self.power < self.weight:
            raise ValueError(
                f"Not enough power for train: {self.power}. Should be more then: {self.weight}"
            )

    def __repr__(self):
        return f"Locomotive (power={self.power}, weight={self.weight}, passengers={self.passengers}) "


class SeatedWagon(Wagon):
    def __init__(self, passengers):
        super().__init__(passengers=passengers, seats=50, weight=10, baggage=0)

    def __repr__(self):
        return f"Seated wagon (seats={self.seats}, passengers={self.passengers}, weight={self.weight})"


class SleepingWagon(Wagon):
    def __init__(self, passengers):
        super().__init__(passengers=passengers, seats=25, weight=20, baggage=0)

    def __repr__(self):
        return f"Sleeping wagon (seats={self.seats}, passengers={self.passengers}, weight={self.weight})"


class RestaurantWagon(Wagon):
    def __init__(self):
        super().__init__(passengers=0, seats=30, weight=20, baggage=0)

    def __repr__(self):
        return f"Restaurant wagon (seats={self.seats}, passengers={self.passengers}, weight={self.weight})"


class LuggageWagon(Wagon):
    def __init__(self):
        super().__init__(passengers=0,seats=0, weight=20, baggage=100)

    def __repr__(self):
        return f"Luggage wagon (baggage={self.baggage}, weight={self.weight})"


if __name__ == '__main__':  # pragma: no cover
    train = Train("Express")
    v1 = Locomotive(100)
    v2 = SeatedWagon(20)
    train.add_wagon(v1)
    train.add_wagon(v2)
    print(v1)
    print(train)