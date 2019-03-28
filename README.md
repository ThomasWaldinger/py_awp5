# py-awp5

A python wraper for the [Archiware P5 CLI](http://support.archiware.com/support/download/cli_5.5.0.pdf).

Simplifies the integration of the Archiware P5 Software in modern MAM and DAM Systems.


## Table of Contents
- Getting Started
 - Prerequisites
 - Installation
 - First Steps

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

You will require python3 installed on your system.

If you do not have Python installed on your system go to [python.org's download section](https://www.python.org/downloads/) and download the current version for your OS. If you prefer using a package manager(like MacPorts, Homebrew, Chocolatey,...), look for a python-3 package. 

You will also need Archiware P5 installed on your system. py-awp5 is using the nsdchat executable to communicate with the P5 Server.

### Installation

install py-awp5 directly from GitHub using pip:
```
pip install git+https://github.com/ThomasWaldinger/py_awp5
```

### Usage

#### First Steps
In an interactive python session:
```python
from awp5 import Connection
from awp5.api import Job
con=Connection("P5Admin","p5passwd")
for job_i in Job.failed(31):
  print("{}:\n{}".format(job_i, job_i.xmlticket())
```

#### API Structure
The wrapper offers both a function-like syntax, using the "id strings" as
resource arguments(similar to the syntax the nsdchat cli uses) and a more
pythonic/object-based syntax.


```python
from awp5.api import volume
for vol_id in volume.names():
  print(vol_id, volume.barcode(vol_id), volume.isonline(vol_id),
        volume.label(vol_id), volume.mediatype(vol_id))

from awp5.api import Volume
for vol in Volume.names():
  print(vol, vol.barcode(), vol.isonline(), vol.label(), vol.mediatype())
```

Depending on your personal preference import the modules using capital or
lowercase letters.
