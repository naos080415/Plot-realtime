import threading
import time
from collections import deque
from functools import partial


from defs import QtCore, QtWidgets
from my_colors import tab10_qcolor
import pyqtgraph as pg

import argparse
import sys
import pathlib
from collections import deque
import math
import time

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np

class PlotGraph:
    def __init__(self):
        # UIを設定
        self.win = pg.GraphicsWindow()
        self.win.setWindowTitle('Random plot')
        self.plt = self.win.addPlot()
        self.plt.setYRange(-0.5, 0.5) # 一旦，適当に設定
        self.curve = self.plt.plot(pen=(0, 0, 255))

        # データを更新する関数を呼び出す時間を設定
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.display)
        self.timer.start(100)

        self.data = np.zeros(100)

    def data_update(self, new_data):
        self.data = np.delete(self.data, 0)
        self.data = np.append(self.data, new_data)

    def display(self):
        self.curve.setData(self.data)


def main():
    print("call main func")

    while True:
        print("exec main func")

    
if __name__ == "__main__":
    t = threading.Thread(target=main, name='function')   # nameの引数は何を表してるか謎
    t.start()

    graphWin = PlotGraph()
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
