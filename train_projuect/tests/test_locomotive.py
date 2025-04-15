import pytest
from train_projuect.main.Locomotive import Locomotive

def test_creation_locomotive():
 w1 = Locomotive(200)

 assert w1.seats == 0
 assert w1.weight == 10
 assert w1.baggage == 0
 assert w1.passengers == 0
 assert w1.power == 200

def test_not_enough_power():
    with pytest.raises(ValueError) as exc_info:
        Locomotive(5)

    assert str(exc_info.value) == "Not enough power for train: 5. Should be more then: 10"