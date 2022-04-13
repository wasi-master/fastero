python -m fastero \
    --setup "l=[1]" \
    "a, = l" \
    "a = l[0]" \
    "a = l[-1]" \
    -n Unpacking \
    -n Indexing \
    -n "Negative Indexing" \
    --total-time 1s \
    --export-image a.png \
    --code-theme dracula
