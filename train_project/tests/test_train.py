import pytest
from train_project.main.train import Train, Locomotive, SleepingWagon, SeatedWagon, RestaurantWagon, LuggageWagon
import logging

def test_add_locomotive_first(caplog, empty_train):
    with caplog.at_level(logging.INFO):
        w1 = Locomotive(200)
        len1 = len(empty_train.wagons)
        empty_train.add_wagon(w1)
        len2 = len(empty_train.wagons)

    assert 'added successfully' in caplog.text
    assert len2 == len1 + 1

def test_add_not_locomotive_first(caplog, empty_train):
    with caplog.at_level(logging.ERROR):
        w1 = SeatedWagon(20)
        len1 = len(empty_train.wagons)
        empty_train.add_wagon(w1)
        len2 = len(empty_train.wagons)

    assert 'Locomotive should be in the beginning' in caplog.text
    assert len2 == len1

def test_add_more_wagons_than_power(caplog, empty_train):
    with caplog.at_level(logging.ERROR):
        w1 = Locomotive(30)
        w2 = SeatedWagon(20)
        empty_train.add_wagon(w1)
        len1 = len(empty_train.wagons)
        empty_train.add_wagon(w2)
        len2 = len(empty_train.wagons)

    assert 'Not enough power for this wagon' in caplog.text
    assert len2 == len1
@pytest.mark.parametrize('wagon_type, added_len',
                         [(SeatedWagon(20), 2),
                          (RestaurantWagon(), 1),
                          (SleepingWagon(20), 2),
                          (LuggageWagon(), 1)
                          ])
def test_add_wagon(caplog, empty_train, wagon_type, added_len):
    w1 = Locomotive(200)
    empty_train.add_wagon(w1)
    len1 = len(empty_train.wagons)
    w2 = wagon_type
    with caplog.at_level(logging.INFO):
        empty_train.add_wagon(w2)
        len2 = len(empty_train.wagons)

    assert 'added successfully' in caplog.text
    assert len2 == len1 + added_len

def test_start_full_train(caplog, full_train):
    with caplog.at_level(logging.INFO):
        full_train.start()

    assert 'Train is ready to go' in caplog.text

def test_start_unfull_train(caplog, empty_train):
    w1 = Locomotive(200)
    w2 = SeatedWagon(20)
    empty_train.add_wagon(w1)
    empty_train.add_wagon(w2)
    with caplog.at_level(logging.ERROR):
        empty_train.start()

    assert 'Not all wagons type are present' in caplog.text
