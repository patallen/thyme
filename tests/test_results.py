from thyme.results import InvalidResult, ValidResult


def test_result_boolean_values():
    assert not InvalidResult()
    assert ValidResult({})


def test_invalid_result_init():
    w_error = InvalidResult(error="There was an error.")
    assert len(w_error.errors) == 1

    w_errors = InvalidResult(errors=["Error one.", "Error Two"])
    assert len(w_errors.errors) == 2


def test_invalid_to_str():
    inv = InvalidResult(error="There was an error.")
    assert str(inv) == 'Whoops! We couldn\'t do that...\nThere was an error.'


def test_invalid_from_list():
    inv = InvalidResult.from_list(["error one"])
    assert str(inv) == 'Whoops! We couldn\'t do that...\nerror one'


def test_invalid_result_has_errors():
    no_errors = InvalidResult()
    assert not no_errors.has_errors()

    errors = InvalidResult.from_list(["dalfjdlsakfj"])
    assert errors.has_errors()


def test_invalid_add_error():
    inv = InvalidResult()
    inv.add_error("This was an error.")
    assert len(inv.errors) == 1


def test_valid_result():
    val = ValidResult(result=100000)
    assert val.result == 100000

    assert '100000' in str(val)
