import pytest
from train_projuect.main.train import Train, Locomotive, SleepingWagon, SeatedWagon, RestaurantWagon, LuggageWagon

@pytest.fixture
def full_train():
    train = Train("Test Express")
    w1 = Locomotive(200)
    w2 = SleepingWagon(20)
    w3 = SeatedWagon(20)
    w4 = RestaurantWagon()
    train.add_wagon(w1)
    train.add_wagon(w2)
    train.add_wagon(w3)
    train.add_wagon(w4)
    return train

@pytest.fixture
def empty_train():
    train = Train("Test Express")
    return train