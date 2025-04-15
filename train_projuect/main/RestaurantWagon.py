from .wagon import Wagon

class RestaurantWagon(Wagon):
    def __init__(self):
        super().__init__(passengers=0, seats=30, weight=20, baggage=0)

    def __repr__(self):
        return f"Restaurant wagon (seats={self.seats}, passengers={self.passengers}, weight={self.weight})"