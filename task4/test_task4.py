import pytest
import sys

from task4 import min_moves


def test_min_moves_empty_list():
    assert min_moves([]) == 0


def test_min_moves_single_element():
    assert min_moves([100]) == 0
    assert min_moves([-42]) == 0


def test_min_moves_basic_cases():
    assert min_moves([4, 5, 6]) == 2
    assert min_moves([3, 6, 8, 9]) == 8
    assert min_moves([1, 2, 3, 4]) == 4


def test_min_moves_more_20_moves():
    assert min_moves([1, 16, 3, 20]) is None
    assert min_moves([0, 50]) is None
    assert min_moves([-100, 100]) is None


def test_min_moves_negative_and_mixed():
    assert min_moves([-2, -1, 3]) == 5
    assert min_moves([-5, -5, -5]) == 0
    assert min_moves([10, -10, 0]) == 20


def test_min_moves_all_equal():
    assert min_moves([7] * 100) == 0
