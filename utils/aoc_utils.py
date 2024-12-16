"""Helper functions for AOC."""
import os
import pathlib
import warnings


def load_data(year, day, token_file="../aocd_token"):
    """Load puzzle input data.

    The data is stored in the `12-DD.txt` file within the local `inputs`
    folder.
    If this file is not present, the data is retrieved from the AOC
    API using the AOC session cookie (the token).
    This data is saved locally.

    Parameters
    ----------
    year : int
        Year of the event.
    day : int
        Day for the data to retrieve.
    token_file : pathlike
        File that stores the AOC API token.
        Unused for local access to puzzle data.

    Returns
    -------
    data : str
        The puzzle input data
    """
    filename = f"inputs/12-{day:02}.txt"
    if os.path.isfile(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    else:
        try:
            from aocd import get_data
        except ModuleNotFoundError as e:
            raise ModuleNotFoundError(
                "Please install the AOC API Python wrapper "
                "(https://github.com/wimglenn/advent-of-code-data): "
                "'pip install advent-of-code-data', or download data "
                "files manually",
            ) from e
        pathlib.Path(filename).parent.mkdir(exist_ok=True, parents=True)
        with open(token_file, "r", encoding="utf-8") as f:
            aocd_session = f.read().strip()
        data = get_data(session=aocd_session, day=day, year=year)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(data)
        return data


def check(function, tests, part=1, *, verbose=False, skip=False, **kwargs):
    """Check outputs for a given function and test cases.

    Test cases are usually sequences of: input, part 1 output, part 2 output
    The output to select is references by the `part` parameter.

    Parameters
    ----------
    function : callable(data: str, **kwargs) -> T
        Function to validate.
    tests : list[str, Optional[T], ...]
        List of tests (input_string, output_1, output_2, ...) to check.
        Outputs set to None are skipped.
    part : int (default 1)
        Output selector for test cases (starts at 1).
    verbose : bool (default False)
        Display inputs and outputs.
    skip : bool (default False)
        Skip failed tests.
    **kwargs
        Additional keyword arguments to provide to the function.
    """
    for i, (input_, *outputs) in enumerate(tests):
        output = outputs[part - 1]
        if output is not None:
            try:
                if verbose:
                    print(f"[Test {i}] Input:")
                    print(input_)
                result = function(input_, **kwargs)
                if verbose:
                    print(f"[Test {i}] Result: {result} (expected: {output})")
                if result != output:
                    if skip:
                        warnings.warn(
                            f"Test {i} failed with result {result} ({output} expected).",
                            stacklevel=2,
                        )
                    else:
                        raise AssertionError(f"{result} == {output}")
            except Exception as e:
                if skip:
                    warnings.warn(
                        f"Test {i} failed with {e.__class__.__name__}: "
                        f"{e} ({output} expected).",
                        stacklevel=2,
                    )
                else:
                    raise e from None
