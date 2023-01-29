# MIS sound

Instructions to run the code for the audio of the balance board. In the python code is present a square that represent the board, in order to simulate the behaviour of the actual device for testing purposes

## Installation
 
In order to make the code work, some packages need to be installed, if not already present:

### *Python*

**python-osc 1.8.1**

```bash
pip install python-osc
```

### *Pure Data*

**mrpeach**

```bash
mrpeach 0.0.extended
```

The code have been tested with the following versions:

**Python**: 3.8.10

**Pure Data**: 0.53.0 

## Usage

In order to run the software, you need to:
* Open the patch 'MIS_sound.pd' in Pure Data
* Run the python code 'connection.pd'

When the python code is running, a representation of the board will show up. Moving the cursor over it will simulate the position of the barycenter over the balance board. The sound should start and stop automatically when the window is opened and closed

## Customize

In order to customize the code for a real board, you just need to reassign the value of the variables x and y in the python code, with the input coming from the device

## Processing

I've also created a simple 'Processing' sketch, in order to visualize the centering. It could be integrated, with some midifications, in the graphical interface of the project.

In order to test it, you just need to open it and run the sketch. The code is connected with the python one and acts simoultaneously with Pure Data.