from typing import Tuple


def get_shortest_str(*args: Tuple[str]) -> str:
    '''Returns the shortest string passed.
    ```python
    get_shortest_str("abc", "abcd", "abcde") -> "abc"
    ```
    '''
    m = args[0]
    for arg in args:
        m = arg if min(len(m), len(arg)) != len(m) else m
    return m