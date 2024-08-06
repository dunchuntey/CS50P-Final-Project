from pytest import raises
from project import set_start_fret, form_skeleton, unearth_skeleton


def test_set_start_fret():
    # Checking valid and invalid types and values.
    assert set_start_fret(0) == 0
    assert set_start_fret(6) == 6
    assert set_start_fret(12) == 12
    with raises(SystemExit):
        set_start_fret(999)

    with raises(ValueError):
        set_start_fret("ni")
    with raises(ValueError):
        set_start_fret(-1)

    fret = set_start_fret("r")
    assert isinstance(fret, int)
    fret = set_start_fret("")
    assert isinstance(fret, int)


def test_form_skeleton():
    # Checking appropriate return value types when default arguments
    # and valid arguments passed to function.
    assert all(
        [
            isinstance(form_skeleton()[0], list),
            isinstance(form_skeleton()[1], int),
            isinstance(form_skeleton()[2], int),
        ]
    )
    assert all(
        [
            isinstance(
                form_skeleton(start_fret=0, length=5, string_grouping=3)[0], list
            ),
            isinstance(
                form_skeleton(start_fret=0, length=5, string_grouping=3)[1], int
            ),
            isinstance(
                form_skeleton(start_fret=0, length=5, string_grouping=3)[2], int
            ),
        ]
    )
    assert all(
        [
            isinstance(
                form_skeleton(start_fret="r", length=5, string_grouping=3)[0], list
            ),
            isinstance(
                form_skeleton(start_fret="r", length=5, string_grouping=3)[1], int
            ),
            isinstance(
                form_skeleton(start_fret="r", length=5, string_grouping=3)[2], int
            ),
        ]
    )
    assert all(
        [
            isinstance(
                form_skeleton(start_fret=12, length="r", string_grouping=2)[0], list
            ),
            isinstance(
                form_skeleton(start_fret=12, length="r", string_grouping=2)[1], int
            ),
            isinstance(
                form_skeleton(start_fret=12, length="r", string_grouping=2)[2], int
            ),
        ]
    )
    assert all(
        [
            isinstance(
                form_skeleton(start_fret=3, length=5, string_grouping="r")[0], list
            ),
            isinstance(
                form_skeleton(start_fret=3, length=5, string_grouping="r")[1], int
            ),
            isinstance(
                form_skeleton(start_fret=3, length=5, string_grouping="r")[2], int
            ),
        ]
    )

    # Checking invalid arguments for start_fret.
    with raises(ValueError):
        assert form_skeleton(start_fret=-1)
    with raises(ValueError):
        assert form_skeleton(start_fret="ni")
    with raises(SystemExit):
        assert form_skeleton(start_fret=9999)

    # Checking invalid str as argument for length.
    with raises(ValueError):
        assert form_skeleton(length="ni")

    # Checking program continues with inappropriate
    # int as argument for length (correction occurs within function).
    assert all(
        [
            isinstance(form_skeleton(length=20)[0], list),
            isinstance(form_skeleton(length=20)[1], int),
            isinstance(form_skeleton(length=20)[2], int),
        ]
    )

    # Checking program continues with (totally) inappropriate
    # int as argument for length (correction occurs within function).
    assert all(
        [
            isinstance(form_skeleton(length=-9999)[0], list),
            isinstance(form_skeleton(length=-9999)[1], int),
            isinstance(form_skeleton(length=-9999)[2], int),
        ]
    )

    # Checking invalid arguments for string_grouping.
    with raises(SystemExit):
        assert form_skeleton(string_grouping=0)
    with raises(SystemExit):
        assert form_skeleton(string_grouping=10)
    with raises(SystemExit):
        assert form_skeleton(string_grouping=-1)
    with raises(SystemExit):
        assert form_skeleton(string_grouping="ni")
    with raises(SystemExit):
        assert form_skeleton(string_grouping=9999)


def test_unearth_skeleton():
    # Checking function correctly returns list when passed valid arguments.
    assert isinstance(unearth_skeleton(length=4, ceiling=12), list)
    assert isinstance(unearth_skeleton(length=5, ceiling=8), list)
    assert isinstance(unearth_skeleton(length=2, ceiling=2), list)
    assert isinstance(unearth_skeleton(length=10, ceiling=9), list)

    # Checking invalid argument values for length.
    with raises(ValueError):
        assert unearth_skeleton(length=0, ceiling=12)
        assert unearth_skeleton(length=1, ceiling=12)
        assert unearth_skeleton(length=14, ceiling=12)

    # Checking invalid argument types for length and ceiling.
    with raises(TypeError):
        assert unearth_skeleton(length="ni", ceiling=12)
        assert unearth_skeleton(length=5, ceiling="ni")
