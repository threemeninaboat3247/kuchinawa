# -*- coding: utf-8 -*-
"""
Created on Sat Sep  2 13:41:09 2017

@author: Yuki
"""
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QColor

from kuchinawa import Main,Graph
import sys,time
from datetime import datetime
import numpy as np

#QtDesignerで作成した拡張子が.uiのファイルをコンパイルした拡張子が.pyのファイルをimportする　拡張子は含めない
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
        #ファイルダイアログを出して指定された場所にcsvファイルを作成し、そのファイルへアクセスできるインスタンスを取得する
        #get a file instance connected to the csv file which is created to the path appointed in a file dialog.
        file=self.getSaveFile()
        
        #ユーザインタフェース上のウィジットが持つ関数を呼び出す場合は以下のようにself.callを使う。これはスレッドセーフな方法でウィジットを使うために必要。
        #第一引数は関数名、第二、三引数はそれぞれタプル、辞書型でポジショナル、キーワード引数として関数に渡される
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
            
            #振幅、位相、ノイズをユーザインタフェース上のウィジットから取得して時間に対するsin,cosを計算する
            #Calculate a sin and cos wave function of time. Get the amplitude, phase and noise level from widgets on the user interface.
            sin=self.call(self.ui.amp_sin.value)*np.sin(t+np.pi*self.call(self.ui.dial_sin.value)/180)+\
                self.call(self.ui.noise_sin.value)*np.random.rand() # 
            cos=self.call(self.ui.amp_cos.value)*np.cos(t+np.pi*self.call(self.ui.dial_cos.value)/180)+\
                self.call(self.ui.noise_cos.value)*np.random.rand()
            #display the calculated values to the LCD displays on the user interface
            self.call(self.ui.lcdNumber_sin.display,(sin,))
            self.call(self.ui.lcdNumber_cos.display,(cos,))
            #グラフインスタンスを介してグラフにデータをプロットする。どういう形式でデータを送るか（putに何を渡すか）はグラフクラスの実装に依存するがkuchinawa.Graph.ScatterAllの
            #場合はdictで送信。　キー'x'の値がx座標、'y'の値がy座標
            #Plot values to graphs　via graph instances. It depends on the implementation of a graph class how to send data to the graph, that is, 
            #what you hand to 'kuchinawa.Graph.GraphInterface.put' method. In case of kuchinawa.Graph.ScatterAll, users send data 
            #represented as a dict. The values of key 'x' and 'y' are the x and y coordinate of a data point respectively.
            g_sin.put({'x':t,'y':sin})
            g_cos.put({'x':t,'y':cos})
            g_orbit.put({'x':cos,'y':sin})
            #辞書型をファイルインスタンスの'write_data'メソッドに渡すことでファイルにデータを書き出す。キーと同じヘッダを持つ列に値が書き込まれる。
            #Write data to the file by handing a dict to 'write_data' method of the file instance.
            #A value is written to the column which has the same header with the key.
            data={T:t,Sin:sin,Cos:cos}
            file.write_data(data)
            time.sleep(0.01)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    s=Sample()
    sys.exit(app.exec_())       