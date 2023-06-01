import pytest

from names import Names


@pytest.fixture
def default_name():
    """Return a new names instance."""
    return Names()


@pytest.fixture
def name_string_list():
    """Return a list of example names."""
    return ["A1", "B12", "C7"]


@pytest.fixture
def used_names(name_string_list):
    """Return a names instance, after a list of name is added"""
    name = Names()
    name.lookup(name_string_list)
    return name


@pytest.fixture
def error_names():
    """Return a name instance after 3 errors are added"""
    name = Names()
    name.unique_error_codes(3)
    return name


def test_initialisation(default_name, error_names, used_names):
    """Test if the attributes of the class returns the expected output."""
    # Name_list is empty.
    assert default_name.names == []
    # Name_list has 3 existing names.
    assert used_names.names == ["A1", "B12", "C7"]
    # Error codes = 0.
    assert default_name.error_code_count == 0
    # Error codes = 3.
    assert error_names.error_code_count == 3


def test_unique_error_codes_exceptions(default_name):
    """Test if unique_error_codes raises expected exceptions."""
    with pytest.raises(TypeError):
        default_name.unique_error_codes(1.4)
    with pytest.raises(TypeError):
        default_name.unique_error_codes("Pooh")
    with pytest.raises(TypeError):
        default_name.unique_error_codes(["Pooh", "Piglet"])
    with pytest.raises(ValueError):
        default_name.unique_error_codes(-1)


def test_unique_error_codes(default_name, error_names):
    """Test if unique_error_codes return the expected output"""
    assert default_name.unique_error_codes(0) == range(0)
    assert default_name.unique_error_codes(3) == range(3)
    assert error_names.unique_error_codes(5) == range(3, 8)


def test_query_exceptions(default_name):
    """Test if query raises expected exceptions."""
    # with pytest.raises(SyntaxError):
    #     default_name.query('Pooh')
    with pytest.raises(TypeError):
        default_name.query(["Pooh", 3.4])
    with pytest.raises(TypeError):
        default_name.query(1.4)
    with pytest.raises(TypeError):
        default_name.query(1)


@pytest.mark.parametrize("name_string, name_id", [
    ("A1", 0),
    ("B12", 1),
    ("C7", 2),
])
def test_query(default_name, used_names, name_string, name_id):
    """Test if query method returns the expected output."""
    assert used_names.query(name_string) == name_id
    assert isinstance(used_names.query("A1"), int)


@pytest.mark.parametrize(
    "name_id, names_list",
    [([0, 1, 2], ["A1", "B12", "C7"])])
def test_lookup(used_names, name_id, names_list):
    """Test if lookup returns a list of name_id"""
    # look up present names
    assert used_names.lookup(names_list) == name_id


def test_get_name_string_exceptions(used_names):
    """Test if get_name_string raises expected exceptions."""
    with pytest.raises(TypeError):
        used_names.get_name_string(1.4)
    with pytest.raises(TypeError):
        used_names.get_name_string("Pooh")
    with pytest.raises(ValueError):
        used_names.get_name_string(-1)


@pytest.mark.parametrize("name_id, expected_string", [
    (0, "A1"),
    (1,  "B12"),
    (2,  "C7"),
])
def test_get_name_string(used_names, default_name, name_id, expected_string):
    """Test if get_name_string returns the expected string."""
    # Name is present
    assert used_names.get_name_string(name_id) == expected_string
    # Name is absent
    assert default_name.get_name_string(name_id) is None
