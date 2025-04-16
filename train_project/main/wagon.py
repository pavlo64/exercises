from abc import ABC, abstractmethod
import logging


logger = logging.getLogger(__name__)


class Wagon(ABC):
    def __init__(self, passengers:int, seats:int, weight: int, baggage:int):
        self.weight = weight
        self.passengers = passengers
        self.baggage = baggage
        self.seats = seats
        if self.passengers > self.seats:
            raise ValueError(
                f"Too many passengers: {self.passengers}. Max seats available: {self.seats}"
            )

        logging.info(
            f"Created {self.__class__.__name__} with parameters: "
            f"passengers={self.passengers}, seats={self.seats}, weight={self.weight}, baggage={self.baggage}"
        )



    @abstractmethod
    def __repr__(self):
        pass
