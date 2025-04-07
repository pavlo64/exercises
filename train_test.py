import pytest
from train import Train, Locomotive, SleepingWagon, SeatedWagon, RestaurantWagon, LuggageWagon

@pytest.fixture
def setup_train():
    train = Train("Express")
    train.add_wagon(Locomotive, power=1000)
    train.add_wagon(SeatedWagon, passengers=40)
    train.add_wagon(SleepingWagon, passengers=20)
    train.add_wagon(RestaurantWagon)

    return train

def test_train_creation(setup_train):
    assert setup_train.name == "Express"
    assert len(setup_train.wagons) > 0


def test_all_wagons_type_check(setup_train):
    assert setup_train.all_wagons_type_check() is True

def test_locomotive_position(setup_train):
    assert isinstance(setup_train.wagons[0], Locomotive)

def test_train_power_check(setup_train):
    assert setup_train.train_power_check() is False

def test_enough_baggage(setup_train):
    total_passengers = sum(wagon.passengers for wagon in setup_train.wagons if hasattr(wagon, 'passengers'))
    total_baggage = sum(wagon.baggage for wagon in setup_train.wagons if hasattr(wagon, 'baggage'))
    assert total_baggage >= total_passengers

def test_excess_passengers_raises_error():
    train = Train("Overload Test")
    train.add_wagon(Locomotive, power=1000)
    with pytest.raises(ValueError, match="Too many passengers"):
        train.add_wagon(SeatedWagon, passengers=100)

def test_train_main_output(setup_train, capsys):
    setup_train.main()
    captured = capsys.readouterr()
    assert "Train is ready to go" in captured.out

