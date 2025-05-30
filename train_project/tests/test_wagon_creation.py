from train_project.main.SeatedWagon import SeatedWagon
from train_project.main.SleepingWagon import SleepingWagon
from train_project.main.RestaurantWagon import RestaurantWagon
from train_project.main.LuggageWagon import LuggageWagon
import pytest

@pytest.mark.parametrize('wagon_type, seats',
                         [(SeatedWagon, 50),
                          (SleepingWagon, 25)
                          ])
def test_wagons_with_passengers_creation(wagon_type,seats):
    w1 = wagon_type(20)

    assert w1.seats == seats
    assert w1.weight == 20
    assert w1.baggage == 0
    assert w1.passengers == 20

@pytest.mark.parametrize('wagon_type, seats, luggage',
                         [(RestaurantWagon, 30, 0),
                          (LuggageWagon , 0, 100)
                          ])
def test_wagons_without_passengers_creation(wagon_type, seats, luggage):
    w1 = wagon_type()

    assert w1.seats == seats
    assert w1.weight == 20
    assert w1.baggage == luggage
    assert w1.passengers == 0

@pytest.mark.parametrize('wagon_type, passengers',
                         [(SeatedWagon, 60),
                          (SleepingWagon, 30)
                          ])
def test_wagon_more_passengers_then_seats_creation(wagon_type,passengers):
    with pytest.raises(ValueError) as exc_info:
        wagon_type(passengers)

    assert 'Too many passengers' in str(exc_info.value)
