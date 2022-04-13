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
- [ ] Compile the code before executing
