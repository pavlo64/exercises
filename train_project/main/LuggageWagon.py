from .wagon import Wagon

class LuggageWagon(Wagon):
    def __init__(self):
        super().__init__(passengers=0,seats=0, weight=20, baggage=100)

    def __repr__(self):
        return f"Luggage wagon (baggage={self.baggage}, weight={self.weight})"
