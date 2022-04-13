python -m fastero \
    -s "import itertools" \
    "(i for i in itertools.repeat(None, 100_000_000))" \
    "(i for i in range(100_000_000))"