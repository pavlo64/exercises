from .wagon import Wagon
import logging

class Locomotive(Wagon):
    def __new__(cls, power: int):
        weight = 10
        if power < weight:
            logging.error(f"Not enough power for locomotive: {power}. Should be more then: {weight}")
            return None
        return super().__new__(cls)
    def __init__(self, power: int) -> None:

        super().__init__(passengers=0, seats=0, weight=10, baggage=0)
        self.power = power
        logging.info(f"Locomotive created with power={self.power}")

    def __repr__(self):
        return f"Locomotive (power={self.power}, weight={self.weight}, passengers={self.passengers}) "
