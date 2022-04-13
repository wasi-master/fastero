python -m fastero \\
    --setup "temp1 = list(range(100)); temp2 = [i * 2 for i in range(50)]" \\
    "list(set(temp1) - set(temp2))" \\
    "s = set(temp2);[x for x in temp1 if x not in s]" \\
    "set(temp1) ^ set(temp2)" \\
    "set(temp1).difference(set(temp2))" \\
    "[item for item in temp1 if item not in temp2]" \\
    -n "set - set" \\
    -n "set + list comp" \\
    -n "set + xor" \\
    -n "set.difference()" \\
    -n "list comp" \\
    --total-time 1s \\
    --export-plot python_diff_between_two_lists_benchmark.png \\
    --label-format "{snippet_name}" \\
    --export-markdown python_diff_between_two_lists_benchmark.md \\
    --export-json python_diff_between_two_lists_benchmark.json