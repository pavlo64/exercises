
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
    w1 = Locomotive(5)
    print (w1)

main()
