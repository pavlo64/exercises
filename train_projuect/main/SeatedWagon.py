from .wagon import Wagon

class SeatedWagon(Wagon):
    def __init__(self, passengers: int):
        super().__init__(passengers=passengers, seats=50, weight=20, baggage=0)

    def __repr__(self):
        return f"Seated wagon (seats={self.seats}, passengers={self.passengers}, weight={self.weight})"
