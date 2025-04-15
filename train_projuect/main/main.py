
from .SeatedWagon import SeatedWagon
from .SleepingWagon import SleepingWagon
from .RestaurantWagon import RestaurantWagon
from .LuggageWagon import LuggageWagon
from .Locomotive import Locomotive
from .train import Train
import logging
import sys

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


def main():
    train = Train("Express")
    w1 = Locomotive(200)
    w2 = SleepingWagon(20)
    w3 = SeatedWagon(20)
    w4 = RestaurantWagon()
    train.add_wagon(w1)
    train.add_wagon(w2)
    train.add_wagon(w3)
    train.add_wagon(w4)

main()