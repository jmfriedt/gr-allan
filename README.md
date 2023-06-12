# GNU Radio Allan deviation plot

Assumes that https://pypi.org/project/AllanTools/ has been installed and is functional

Tested with GNU Radio 3.10.5.1 (Python 3.11.1)

## Installation

```bash
mkdir build
cd build
cmake ../
sudo make install
``` 

Run the ``allan_demo.grc`` example in ``examples``.

The two technical challenges met in this demonstration are:
* wrapping AllanTools in a GNU Radio Sink block
* real time plotting of the result, inspired from ``gr-pyqt`` but heavily edited (and
simplified) examples.

## TODO

* Add error bars
* Add colored noise generation
