# Kuchinawa
This package help you to create a control program for measurement instruments. It provides you a dynamic way to control your program via a graphical user interface and realtime graph plotting.


## 0. Installation

	conda install -c threemeninaboat3247 kuchinawa

## 1. Example
Kuchinawa includes several sample programs. The following figure shows the screen shot when one of them is being executed. You can run it on your machine by typing the next commands in a python interpreter.

```python
import kuchinawa
kuhinawa.run_sample()
```

![Screen shot of Kuchinawa](https://github.com/threemeninaboat3247/kuchinawa/blob/master/screenshot.png)

As you can see, two windows are shown. One is a graphical user interface made by using QtDesigner and the other is a window for graph drawing. If you press _Run_ button in the toolbar, the program is started. You can stop and terminate the program by _Stop_ and _Exit_ button respectively. The following code is the main body of this sample.

```python
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QColor

from kuchinawa import Main,Graph
import sys,time
from datetime import datetime
import numpy as np


#import the file with the extension .py which was compiled from a file with extension .ui made by using QtDesigner. not include the extension.
from kuchinawa.Examples import SinCos_ui

COLORS=[QColor(255,0,0),QColor(255,255,0),QColor(0,255,0)] #the colors of points in graphs
#declaration of constants
T='time'
Sin='sin'
Cos='cos'



class Sample(Main):
    def __init__(self):
        super().__init__()
        self.ui=SinCos_ui.Ui_Form() #get a user interface made by using QtDesigner
        self.setUI(self.ui) #set the user interface

    def run(self):
        #get a file instance connected to the csv file which is created to the path appointed in a file dialog.
        file=self.getSaveFile()

        #Please use 'self.call' to call a function of a widget in the user interface. This method provides a thread-safe way
        #to interact with widgets. The first argument is the name of the function. The second and third argument are
        #a tuple and dict to be handed to the function as positional and keyword argument respectively.
        self.call(self.ui.lineEdit.setText,(file.path,))
        file.write_header([T,Sin,Cos]) #write headers to the file

        #Generate graphs by using 'self.addGraph' and get graph instances. The first argument is the graph class to instantiate.
        #This class must inherit kuchinawa.Graph.GraphBase. The second and third argument are
        #a tuple and dict to be handed to the function as positional and keyword argument respectively.
        g_sin=self.addGraph(Graph.ScatterAll,(T,'sec',Sin,'V'),{'color':COLORS[0]},'Sin')
        g_cos=self.addGraph(Graph.ScatterAll,(T,'sec',Cos,'V'),{'color':COLORS[1]},'Cos')
        g_orbit=self.addGraph(Graph.ScatterAll,(Cos,'V',Sin,'V'),{'color':COLORS[2]},'Orbit')

        timeOrigin=datetime.now() #get the origin of time

        while True:
            t=(datetime.now()-timeOrigin).total_seconds() #get an elapsed time from the origin of time

            #Calculate a sin and cos wave function of time. Get the amplitude, phase and noise level from widgets on the user interface.
            sin=self.call(self.ui.amp_sin.value)*np.sin(t+np.pi*self.call(self.ui.dial_sin.value)/180)+\
                self.call(self.ui.noise_sin.value)*np.random.rand() #
            cos=self.call(self.ui.amp_cos.value)*np.cos(t+np.pi*self.call(self.ui.dial_cos.value)/180)+\
                self.call(self.ui.noise_cos.value)*np.random.rand()

            #display the calculated values to the LCD displays on the user interface
            self.call(self.ui.lcdNumber_sin.display,(sin,))
            self.call(self.ui.lcdNumber_cos.display,(cos,))

            #Plot values to graphs　via graph instances. It depends on the implementation of a graph class how to send data to the graph, that is,
            #what you hand to 'kuchinawa.Graph.GraphInterface.put' method. In case of kuchinawa.Graph.ScatterAll, users send data
            #represented as a dict. The values of key 'x' and 'y' are the x and y coordinate of a data point respectively.
            g_sin.put({'x':t,'y':sin})
            g_cos.put({'x':t,'y':cos})
            g_orbit.put({'x':cos,'y':sin})
						
            #Write data to the file by handing a dict to 'write_data' method of the file instance.
            #A value is written to the column which has the same header with the key.
            data={T:t,Sin:sin,Cos:cos}
            file.write_data(data)
            time.sleep(0.01)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    s=Sample()
    sys.exit(app.exec_())      
```
You can refer to the comment in the program or the doc string for the usage of each method. In this program we repeatedly calculate a _sin_ and _cos_ function of time and output them to graphs and a file. The amplitudes, phases and noises of the functions can be controlled via the sliders and dials in the user interface.

## 2. How to write your program
You have to do two things in writing your own program by using Kuchinawa. One is to make your user interface by using QtDesigner and the other is to write the actual code that you want to execute. Let's understand how it works by making an actual code.

### 2-0. Make a user interface by QtDesigner
QtDesigner is a powerful tool for creating user interfaces of Qt in a graphical way. It outputs a file with the extension .ui. Kuchinawa converts this file  to a Python module and import it. This enables users to interact with widgets on the user interface when they are coding. Please make a suitable working directory and output a .ui file into it from QtDesigner. Let me suppose that you made a file named 'Interface.ui'. Then open a command prompt and set the current directory to the working directory that you made. If you start a Python interpreter, you can convert the .ui file by next commands.
```python
import kuchinawa
kuchinawa.compileUi('Interface.ui')
```
Now you should see a file named 'Interface_ui.py' created in the working directory. This is a Python module and will be used in the next section.
### 2-1. Coding
All you have to do in the coding part is to make a subclass of `kuchinawa.Main` and over-ride its methods. That is to get the user interface from the module you made above and set it to `self` in `__init__` method. Then to write in `run` method what you want to do by your program. Now please make a file named 'HelloWorld.py' in the same directory where you made 'Interface_ui.py' and write the following code in it. As you can see, this is a so-called hello world program which displays a string of 'Hello world!' in the console. Your widgets on the user interface can be accessed via `self.ui` attribute. This attribute holds instance variables with the same names that you gave widgets as object names in QtDesigner. So, if you made some widget named `button`, `self.ui.button` exists.

```python
import sys
from PyQt5.QtWidgets import QApplication
from kuchinawa import Main
import Interface_ui

class Sample(Main):
    def __init__(self):
        super().__init__()
        self.ui=Interface_ui.Ui_Form() #get a user interface made by using QtDesigner
        self.setUI(self.ui) #set the user interface

    def run(self):
				print('Hello world!')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    s=Sample()
    sys.exit(app.exec_())      
```

### 2-2. Execution
Just type the next in a command prompt to execute the program that you wrote above.

	python HelloWorld.py

### 2-3. Main methods
kuchinawa.Main class has three instance method to help users make a program.
#### 2-3-0. `call`
This method exists to support a thread-safe way to call a function of a widget on the user interface. The following figure shows an overview of how Kuchinawa works.

![Overview of Kuchinawa](https://github.com/threemeninaboat3247/kuchinawa/blob/master/overview.png)

Your code is executed in another thread where the user interface does not live. Since Qt's widgets are not thread-safe objects, you are not allowed to call their functions directly from another thread. `call` method exists to solve this problem. The usage (doc string) is as follows.
```python
def call(self,function,args=None,kwargs=None):
    '''
    Call a function in the thread in which the instance of this class exists.

    Paramters:
        function: function
            a function to call
        args: tuple
            positional arguments
        kwargs: dict
            keyward arguments

    Returns:
        object
            depends on the function
    '''
```

#### 2-3-1. `addGraph`
This method creates a graph in the graph window and returns an instance of `kuchinawa.Graph.GraphInterface`. You can plot data to the graph by calling `put` function of this instance.
```python
def addGraph(self,graph,args=None,kwargs=None,name='Unnamed'):
    '''
    Add a graph to GraphContainer.

    Parameters:
        graph: class
            a subclass of Graph.GraphBase
        *args: tuple
            positional arguments to pass to __init__ of 'graph'
        **kwargs: dict
            keyword arguments to pass to __init__ of 'graph'
        name: string
            the window title of the graph
    Returns: Graph.GraphInterface
        the interface to plot data to the graph
    '''
```
```python
class GraphInterface:
    '''
    A interface to plot data onto a graph in another process. An instance of this class holds Queue connected to GraphContainer.
    '''
    def put(self,data):
        '''
        Put data to the Queue connected to the graph

        Parameters:
            data: object
                Any object can be given. It depends on the implementation of the graph class how the data is treated
        '''
```
#### 2-3-2. `getSaveFile`
This method opens a file dialog and returns a file instance which can be used to write data to the csv file appointed by the user. The instance is an instance of `kuchinawa.File.File` and has three methods (`write_comment`, `write_header` and `write_data`) which are used to write comments, headers and data respectively to the file.

### 2-4. Extension of `kuchinawa.Graph.GraphBase`
This class is a base class for various graph drawing. You can make a new graph class by inheriting this class and give to `addGraph` method's first argument. An instance of this class has an attribute named `que` which can be accessed by `self.que` in an instance method. If you put data to a graph instance of this class via `kuchinawa.Graph.GraphInterface`, the data is stacked to `que`. This class also has `update` method which is called at regular time intervals. So you can implement you own graph drawing by over-riding this method. See the code of `kuchinawa.Graph.ScatterAll` as an example.

## 3. Future work
I made this package to support creating control programs for scientific measurements in my reasearch. As you can see, the total code is still quite small and there is much room for improvement. I am going to continue developing this package over a long span. I am happy to get your comment or advise about this package. Please [ contact me](<threemeninaboat3247@gmail.com>).
