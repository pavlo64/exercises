
class Train:
    def __init__(self, name: str):
        self.name = name
        self.wagons = []

    def __repr__(self):
        return f"Train name = {self.name} \n wagons: {self.wagons} "

    def add_wagon(self, wagon_type, *args, **kwargs):
        wagon = wagon_type(*args, train=self, **kwargs)
        if not isinstance(wagon, LuggageWagon):
            self.enough_baggage_check()
        return wagon

    def all_wagons_type_check(self) -> bool:
        required_wagon_types = {Locomotive, SeatedWagon, SleepingWagon, RestaurantWagon, LuggageWagon}
        wagon_types_in_train = {type(wagon) for wagon in self.wagons}
        return required_wagon_types.issubset(wagon_types_in_train)

    def locomotive_check(self) -> bool:
        return self.wagons[0].isinstance(Locomotive)

    def train_power_check(self, train_weight: int = 0) -> bool:
        locomotive = next((wagon for wagon in self.wagons if isinstance(wagon, Locomotive)), None)
        power = locomotive.power
        for wagon in self.wagons:
            train_weight += wagon.weight
        return power < train_weight

    def enough_baggage_check(self, all_passengers: int = 0, all_baggage: int = 0) -> None:
        for wagon in self.wagons:
            if type(wagon) in {SeatedWagon, SleepingWagon, RestaurantWagon}:
                all_passengers += wagon.passengers
            if type(wagon) == LuggageWagon:
                all_baggage += wagon.baggage
        if all_passengers > all_baggage:
            self.add_wagon(LuggageWagon)

    def main(self) -> None:
        if not self.all_wagons_type_check():
            print('Not all wagons type are present')
        if self.train_power_check():
            print('Not enough power to run train')
        if not self.locomotive_check():
            print('Locomotive should be at first position in the train')
        else:
            print('Train is ready to go')


class Wagon:
    def __init__(self, train: Train):
        self.weight = 20
        train.wagons.append(self)


class Locomotive(Wagon):
    def __init__(self, power, train: Train):
        if train is None:
            train = Train(name="Express")
        super().__init__(train)
        self.power = power
        self.weight = 10

    def __repr__(self):
        return f"Locomotive (power={self.power}, weight={self.weight}) \n"


class SeatedWagon(Wagon):
    def __init__(self, passengers, train: Train):
        super().__init__(train)
        self.seats = self.seat_number()
        self.passengers = passengers
        if self.passengers > self.seats:
            raise ValueError(f"Too many passengers: {self.passengers}. Max seats available: {self.seats}")

    def seat_number(self):
        return 50

    def __repr__(self):
        return f"Seated wagon (seats={self.seats}, passangers={self.passengers}, weight={self.weight})\n"


class SleepingWagon(SeatedWagon):
    def seat_number(self):
        return 25

    def __repr__(self):
        return f"Sleeping wagon (seats={self.seats}, passangers={self.passengers}, weight={self.weight})\n"


class RestaurantWagon(SeatedWagon):
    def __init__(self, train: Train):
        super().__init__(passengers=0, train=train)  # passengers не нужен, передаем 0
        self.seats = self.seat_number()

    def seat_number(self):
        return 30

    def __repr__(self):
        return f"Restaurant wagon (seats={self.seats}, passangers={self.passengers}, weight={self.weight})\n"


class LuggageWagon(Wagon):
    def __init__(self, train: Train):
        super().__init__(train)
        self.baggage = 100

    def __repr__(self):
        return f"Luggage wagon (baggage={self.baggage}, weight={self.weight}) \n"


if __name__ == '__main__':  # pragma: no cover
    train = Train("Express")
    train.add_wagon(Locomotive, power=1000)
    train.add_wagon(SeatedWagon, passengers=40)
    train.add_wagon(SeatedWagon, passengers=50)
    train.add_wagon(SeatedWagon, passengers=50)
    train.add_wagon(SeatedWagon, passengers=50)
    train.add_wagon(SleepingWagon, passengers=20)
    train.add_wagon(RestaurantWagon)
    print(train)
    train.main()
