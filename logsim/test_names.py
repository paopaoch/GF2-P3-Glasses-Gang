import pytest

from names import Names

@pytest.fixture
def new_names():
    """Return a new names instance."""
    return Names()


@pytest.fixture
def name_string_list():
    """Return a list of example names."""
    return ["Woody", "Buzz", "Andy"]


@pytest.fixture
def added_names(name_string_list):
    """Return a names instance, after a list of name is added"""
    name = Names()
    name.lookup(name_string_list)
    return name


def test_unique_error_codes(used_names, error_names):
    """Test if unique_error_codes return the expected output"""
    assert used_names.unique_error_codes(0) == range(0)
    assert used_names.unique_error_codes(3) == range(3)
    assert error_names.unique_error_codes(8) == range(5, 8)


def test_unique_error_codes_exceptions(used_names):
    """Test if unique_error_codes raises expected exceptions."""
    with pytest.raises(TypeError):
        used_names.get_string(1.4)
    with pytest.raises(TypeError):
        used_names.get_string("Pooh")
    with pytest.raises(TypeError):
        used_names.get_string(["Pooh", "Piglet"])
    with pytest.raises(ValueError):
        used_names.get_string(-1)


@pytest.mark.parametrize("name_string, name_id", [
    ("Woody", 0),
    ("Buzz", 1),
    ("Andy", 2),
    (None, 3)
])
def test_query(new_names, used_names, name_string, name_id):
    """Test if query method returns the expected output."""
    assert used_names.query(name_string) == name_id
    assert isinstance(used_names.query("Woody"), int)
    assert new_names.query("Pooh") is None


def test_query_exceptions(used_names):
    """Test if query raises expected exceptions."""
    with pytest.raises(TypeError):
        used_names.get_string(_)
    with pytest.raises(TypeError):
        used_names.get_string(["Pooh", 3.4])
    with pytest.raises(TypeError):
        used_names.get_string(1.4)
    with pytest.raises(TypeError):
        used_names.get_string(1)


@pytest.mark.parametrize("name_id, expected_string", [
    (0, "Woody"),
    (1, "Buzz"),
    (2, "Andy"),
    (3, None)
])
def test_lookup(used_names, new_names, name_id, expected_string):
    """Test if lookup returns a list of name_id"""
    # look up present names
    assert used_names.lookup(expected_string) == name_id
    # look up absent names
    assert new_names.lookup(expected_string) == len(new_names.names)-1


def test_lookup_exceptions(used_names):
    """Test if lookup raises expected exceptions."""
    with pytest.raises(TypeError):
        used_names.get_string(1.4)
    with pytest.raises(TypeError):
        used_names.get_string(1)
    with pytest.raises(TypeError):
        used_names.get_string("Pooh")
    with pytest.raises(TypeError):
        used_names.get_string([])
    with pytest.raises(TypeError):
        used_names.get_string(["Pooh", "Piglet", 5])
    with pytest.raises(TypeError):
        used_names.get_string(["Pooh", ["Piglet", 5]])


@pytest.mark.parametrize("name_id, expected_string", [
    (0, "Woody"),
    (1, "Buzz"),
    (2, "Andy"),
    (3, None)
])
def test_get_name_string(used_names, new_names, name_id, expected_string):
    """Test if get_name_string returns the expected string."""
    # Name is present
    assert used_names.get_name_string(name_id) == expected_string
    # Name is absent
    assert new_names.get_string(name_id) is None


def test_get_name_string_exceptions(used_names):
    """Test if get_name_string raises expected exceptions."""
    with pytest.raises(TypeError):
        used_names.get_string(1.4)
    with pytest.raises(TypeError):
        used_names.get_string("Pooh")
    with pytest.raises(ValueError):
        used_names.get_string(-1)
    
