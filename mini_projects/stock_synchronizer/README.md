# Stock synchronizer

Goal of application is to keep products stock in sync (i.e. ebay or amazon products). It means that stock level on all products from one tree should be exactly the same all the time.

# Author

Maciej Moskała

# Installation

Project is set to run in Python 3.6.0+

To install requirements run:

```
$ python setup.py install
```

# Development

To develop use:

```
$ python setup.py develop
```

# Testing

To run tests use:

```
$ python setup.py test
```

# How to run

Project is prepared to be develop in the future.

To run project, use script:

```
$ run_stock_synchronizer
```

The script by default will load data from scenario/input.txt and save to scenario/output.txt. If you want to change those files you can ran script with one or both parameters: `INPUT_FILE`, `OUTPUT_FILE`. In example:

```
$ OUTPUT_FILE=./scenario/out.txt run_stock_synchronizer
```
