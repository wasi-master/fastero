# TODO

- [ ] Maybe custom timeit implementation, especially for warmups, since they don't mean anything currently
- [ ] Add a `--plain` option
  - For this, we can use the ipython syntax

    ```text
    7.46 ns ± 0.0788 ns per loop (mean ± std. dev. of 7 runs, 100000000 loops each)
    ```

    Where loop means run and runs means batches in fastero talk

- [ ] Find/write an asciidoc lexer for pygments
- [ ] Maybe find/write a better shell lexer for shell syntax
  - [ ] Should make `--option` dimmed
  - [ ] Should make the first word some color
  - [ ] Should make strings some color
- [ ] Test compile the code using the `compile()` function before benchmarking. This should be done so that
      any syntax errors can be caught before benchmarking multiple snippets [for a long time] and then it all
      going to waste because of the last snippet having some problem.
