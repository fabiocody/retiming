# Retiming Synchronous Circuitry

[![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/fabiocody/retiming/python-test/master?label=test)](https://img.shields.io/github/workflow/status/fabiocody/retiming/python-test/master?label=test)

The code in this repository is a Python porting of the algorithms described in the paper *Retiming Synchronous Circuitry*
by Charles E. Leiserson and James B. Saxe , published in 1986. The paper describes a circuit transformation called *retiming*,
in which registers are added at some points in a circuit and removed from others in such a way that the functional
behavior of the circuit as a whole is preserved.

## How to test the code

```
$ cd $PROJECT_DIR/src
$ pytest tests.py
```

There is also a command line interface accessible via the `main.py` file. To know more about it, type

```
$ cd $PROJECT_DIR/src
$ ./main.py --help
```

## Documentation

You can find an HTML version of the documentation at this [link](https://fabiocodiglioni.it/retiming/build/html/index.html).

## Presentation

You can find an HTML version of the presentation at this [link](https://fabiocodiglioni.it/retiming/presentation/index.html).
