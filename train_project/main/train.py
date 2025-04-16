import logging
from .Locomotive import Locomotive
from .SeatedWagon import SeatedWagon
from .SleepingWagon import SleepingWagon
from .RestaurantWagon import RestaurantWagon
from .LuggageWagon import LuggageWagon

logger = logging.getLogger(__name__)

class Train:
    def __init__(self, name: str):
        self.name = name
        self.wagons = []

    def __repr__(self):
        wagon_list = ""
        i = 1
        for wagon in self.wagons:
            wagon_list += f" {i}. {wagon} \n"
            i+=1
        return f"Train name = {self.name} \nWagons:\n{wagon_list}"

    def add_wagon(self, wagon):
        if not self.wagons:
            if isinstance(wagon, Locomotive):
                self.wagons.append(wagon)
                logging.info(f"{wagon} added successfully")
            else:
                logging.error("Locomotive should be in the beginning")
            return
        power_required = self.get_power_required(wagon)
        if self.train_power_check(power_required):
            logging.error('Not enough power for this wagon')
            return
        self.wagons.append(wagon)
        logging.info(f"{wagon} added successfully")
        self.enough_baggage_check()

    def get_power_required(self, wagon):
        if isinstance(wagon, (SeatedWagon, SleepingWagon)):
            return 40
        else:
            return 20

    def all_wagons_type_check(self) -> bool:
        required_wagon_types = {Locomotive, SeatedWagon, SleepingWagon, RestaurantWagon, LuggageWagon}
        wagon_types_in_train = {type(wagon) for wagon in self.wagons}
        return required_wagon_types.issubset(wagon_types_in_train)

    def train_power_check(self, train_weight=0) -> bool:
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
            luggage = create_wagon(LuggageWagon)
            self.wagons.append(luggage)

    def start(self) -> None:
        if not self.all_wagons_type_check():
            logging.error('Not all wagons type are present')
        else:
            logging.info('Train is ready to go')


def create_wagon(wagon_type, *args, **kwargs):
    wagon = wagon_type(*args, **kwargs)
    return wagon
