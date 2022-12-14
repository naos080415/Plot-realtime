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

""" ここから """
plotting_data = None   # プロットしたいデータの配列（グローバルに置くのはあまり良くないだろうが気にしてたら時間が・・)
class PlotGraph:
    def __init__(self, GraphSettingValues):   # GraphSettingValues : dict
        # UIを設定
        self.win = pg.GraphicsWindow()
        self.win.setWindowTitle('RealTime plot')
    
        self.graphNum = len(GraphSettingValues) # グラフの個数

        self.plt, self.curve = [], []

        for data_name, y_range in GraphSettingValues.items():
            plt_tmp = self.win.addPlot()

            plt_tmp.setYRange(y_range[0], y_range[1])   # yの範囲を設定

            curve_tmp = plt_tmp.plot(pen=(0, 0, 255))

            self.plt.append(plt_tmp)
            self.curve.append(curve_tmp)

        global plotting_data
        plotting_data = [np.zeros(100) for _ in range(self.graphNum)]


        # データを更新する関数を呼び出す時間を設定
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.display)
        self.timer.start(100)

    def display(self):
        global plotting_data
        for curve, data in zip(self.curve, plotting_data):
            curve.setData(data)


def data_update(new_data):
    global plotting_data

    for i, ndata in enumerate(new_data):
        plotting_data[i] = np.delete(plotting_data[i], 0)
        plotting_data[i] = np.append(plotting_data[i], ndata)
""" ここまで(前回のと張り替える) """

def main():
    print("call main func")

    while True:
        print("exec main func")

        new_data= [np.random.random() for i in range(2)]        # プロットしたいデータをリスト構造にして格納する。
        data_update(new_data=new_data)

        time.sleep(0.2)

    
if __name__ == "__main__":
    GraphSettingValues = {'random1': (-1, 1), 'random2': (-1, 1)}   # ここを変更する。('key': value keyには、グラフのデータの名前, valueにはYの範囲)
    graphWin = PlotGraph(GraphSettingValues=GraphSettingValues)

    t = threading.Thread(target=main, name='function')   # nameの引数は何を表してるか謎
    t.start()

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
