from task1 import circular_traversal


def test_basic_example_1():
    assert circular_traversal(6, 3) == [1, 3, 5]


def test_basic_example_2():
    assert circular_traversal(5, 4) == [1, 4, 2, 5, 3]


def test_m_equals_1():
    assert circular_traversal(5, 1) == [1]


def test_large_step():
    assert circular_traversal(6, 8) == circular_traversal(6, 2)


def test_n_is_1():
    assert circular_traversal(1, 5) == [1]


def test_invalid_n():
    assert circular_traversal(0, 3) == []
    assert circular_traversal(-1, 3) == []


def test_invalid_m():
    assert circular_traversal(5, 0) == []
    assert circular_traversal(5, -2) == []
