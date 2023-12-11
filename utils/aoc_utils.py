"""Helper functions for AOC."""
import os


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
                "files manually"
            ) from e
        with open(token_file, "r", encoding="utf-8") as f:
            aocd_session = f.read().strip()
        data = get_data(session=aocd_session, day=day, year=year)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(data)
        return data


def check(function, tests, part=1, verbose=False, **kwargs):
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
    **kwargs
        Additional keyword arguments to provide to the function.
    """
    for input_, *outputs in tests:
        output = outputs[part - 1]
        if output is not None:
            result = function(input_, **kwargs)
            if verbose:
                print("Input:")
                print(input_)
                print(f"Result: {result} (expected: {output})")
            assert result == output, f"{result} == {output}"
