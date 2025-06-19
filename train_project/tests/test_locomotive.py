import pytest
import logging
from train_project.main.Locomotive import Locomotive

def test_creation_locomotive():
    w1 = Locomotive(200)
    assert w1.seats == 0
    assert w1.weight == 10
    assert w1.baggage == 0
    assert w1.passengers == 0
    assert w1.power == 200

def test_not_enough_power(caplog):
    with caplog.at_level(logging.ERROR):
        w1 = Locomotive(5)


    assert 'Not enough power for locomotive:' in caplog.text
    assert w1 == None
