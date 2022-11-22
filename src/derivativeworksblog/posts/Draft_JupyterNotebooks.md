# Jupyter notebooks are too widely used
## Okay for EDA and reports

## Not repeatable
Difficult to version control
Easy to lose steps / ordering when running

## Hard to share
Often need access to specific data that is not adequately bundled
Along with being unrepeatable, this leads to a high [bus factor](https://en.wikipedia.org/wiki/Bus_factor)

## Lead to innefficient code
People create complex cached datastructures in order to speed up exploration
A long running step to refine dataset often would be difficult to track and maintain in production
Instead, people rely on long running notebooks which increases the bus factor
