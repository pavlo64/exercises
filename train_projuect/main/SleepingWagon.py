from .wagon import Wagon

class SleepingWagon(Wagon):
    def __init__(self, passengers):
        super().__init__(passengers=passengers, seats=25, weight=20, baggage=0)

    def __repr__(self):
        return f"Sleeping wagon (seats={self.seats}, passengers={self.passengers}, weight={self.weight})"