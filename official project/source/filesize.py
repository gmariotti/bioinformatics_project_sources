traditional = [
    (1024 ** 5, 'P'),
    (1024 ** 4, 'T'),
    (1024 ** 3, 'G'),
    (1024 ** 2, 'M'),
    (1024 ** 1, 'K'),
    (1024 ** 0, 'B'),
]

alternative = [
    (1024 ** 5, ' PB'),
    (1024 ** 4, ' TB'),
    (1024 ** 3, ' GB'),
    (1024 ** 2, ' MB'),
    (1024 ** 1, ' KB'),
    (1024 ** 0, (' byte', ' bytes')),
]


def size(bytes, system=traditional):
    """Human-readable file size.

    Using the traditional system, where a factor of 1024 is used::
    
    >>> size(10)
    '10B'
    >>> size(100)
    '100B'
    >>> size(1000)
    '1000B'
    >>> size(2000)
    '1K'
    >>> size(10000)
    '9K'
    >>> size(20000)
    '19K'
    >>> size(100000)
    '97K'
    >>> size(200000)
    '195K'
    >>> size(1000000)
    '976K'
    >>> size(2000000)
    '1M'
    """
    for factor, suffix in system:
        if bytes >= factor:
            break
    amount = int(bytes / factor)
    if isinstance(suffix, tuple):
        singular, multiple = suffix
        if amount == 1:
            suffix = singular
        else:
            suffix = multiple
    return str(amount) + suffix
