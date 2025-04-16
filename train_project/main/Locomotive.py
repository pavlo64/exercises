from .wagon import Wagon
import logging

class Locomotive(Wagon):
    def __init__(self, power: int) -> None:

        super().__init__(passengers=0, seats=0, weight=10, baggage=0)
        self.power = power
        if self.power < self.weight:
            raise ValueError(
                f"Not enough power for train: {self.power}. Should be more then: {self.weight}"
            )

        logging.info(f"Locomotive created with power={self.power}")

    def __repr__(self):
        return f"Locomotive (power={self.power}, weight={self.weight}, passengers={self.passengers}) "
