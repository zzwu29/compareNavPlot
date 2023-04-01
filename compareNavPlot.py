# Author: zzWu
# Version: 1.0
# Date: 2022.04.05

from PySide2.QtWidgets import QApplication, QFileDialog, QGraphicsScene, QMainWindow, QMessageBox
from PySide2.QtUiTools import QUiLoader
import numpy as np
import math
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import tool_func as tf
matplotlib.use("Qt5Agg")  # 声明使用QT5

# colors=['#FD6D5A', '#FEB40B', '#6DC354', '#994487', '#518CD8','#2A9D8F' ,'#45CAFF', '#B913FF', '#443295', '#F4A261', '#E76F51', '#253777',
#         '#C1C976', '#C8A9A1', '#FEC2E4', '#77CCE0', '#FFD372', '#F88078','#104FFF', '#2FD151', '#64C7B8', '#FF1038','#264653', '#E9C46A']

colors=["#023EFF", "#1AC938", "#E8000B","#8B2BE2", "#FFC400", "#00D7FF"] # bright6 in seaborn

def readFromFileInCol(filename='', header=0, cols=[],type=None):
    data=np.loadtxt(filename,skiprows=header,dtype=type)
    return data[:,cols]

class MyFigureCanvas(FigureCanvas):
    # 通过继承FigureCanvas类，使得该类既是一个PyQt5的Qwidget，又是一个matplotlib的FigureCanvas，这是连接pyqt5与matplotlib的关键

    def __init__(self, parent=None, width=10, height=5, dpi=100,top=False,right=False):
        # 创建一个Figure
        self.fig = plt.Figure(figsize=(width, height), dpi=dpi, tight_layout=True)  # tight_layout: 用于去除画图时两边的空白

        FigureCanvas.__init__(self, self.fig)  # 初始化父类
        self.setParent(parent)

        self.axes = self.fig.add_subplot(111)  # 添加子图
        self.axes.spines['top'].set_visible(top)  # 去掉绘图时上面的横线
        self.axes.spines['right'].set_visible(right)  # 去掉绘图时右面的横线

class compareNavPlot(QMainWindow):

    def __init__(self):
        super(compareNavPlot, self).__init__()
        self.ui = QUiLoader().load(r"compareNavPlot.ui")
        self.ui.actionImport_File.triggered.connect(self.prepareAll)
        self.ui.actionPlot.triggered.connect(self.plotAll)
        self.ui.actionClear_Plot.triggered.connect(self.clearPlot)
        self.ui.actionSavfig.triggered.connect(self.Savfig)
        self.ui.c1.clicked.connect(self.fileChoose)
        self.ui.c2.clicked.connect(self.fileChoose)
        self.ui.c3.clicked.connect(self.fileChoose)
        self.ui.c4.clicked.connect(self.fileChoose)

    def fileChoose(self):
        FileDirectory = QFileDialog.getOpenFileName(QMainWindow(), "Please Choose a File")
        if(self.sender().objectName()=="c1"):
            self.ui.imuFile.setText(FileDirectory[0])
        elif(self.sender().objectName()=="c2"):
            self.ui.ResultFile.setText(FileDirectory[0])
            self.ui.StateFile.setText(FileDirectory[0])
        elif(self.sender().objectName()=="c3"):
            self.ui.RefFile.setText(FileDirectory[0])
            self.ui.StateFile.setText(FileDirectory[0])
        elif(self.sender().objectName()=="c4"):
            self.ui.StateFile.setText(FileDirectory[0])
        # print(FileDirectory[0],self.sender().objectName())
    
    def Savfig(self):
        # self.graphic_content_fig_g.axes.savefig('gout.svg',bbox_inches = 'tight')
        MessageBox = QMessageBox()
        MessageBox.critical(QMainWindow(), "Critical", "Function Test in Progress !") 

    def prepareImu(self):
        # self.imuFile=self.ui.imuFile.text()
        self.imuFileHeaderline=int(self.ui.imuFileHeaderline.text())
        self.imuDataCol=[]
        value=self.ui.imuDataCol.text().split(',')
        for i in range(len(value)):
            self.imuDataCol.append(int(value[i])-1)
        self.imuData=readFromFileInCol(self.imuFile,self.imuFileHeaderline,self.imuDataCol,str)
        self.imuData=self.imuData.astype(float)
        self.imuSampleRate=int(self.ui.imuSampleRate.text())
        self.gUnit=self.ui.gUnit.currentText()
        self.aUnit=self.ui.aUnit.currentText()

        if(self.gUnit=="rad/s"):
            self.imuData[:,1:4]=self.imuData[:,1:4]/math.pi*180
        elif(self.gUnit=="deg"):
            self.imuData[:,1:4]=self.imuData[:,1:4]/float(self.imuSampleRate)
        elif(self.gUnit=="rad"):
            self.imuData[:,1:4]=self.imuData[:,1:4]/math.pi*180/float(self.imuSampleRate)

        if(self.aUnit=="m/s"):
            self.imuData[:,4:7]=self.imuData[:,4:7]/float(self.imuSampleRate)

    def prepareResult(self):
        # self.ResultFile=self.ui.ResultFile.text()
        self.ResultFileHeaderline=int(self.ui.ResultFileHeaderline.text())
        self.ResultDataCol=[]
        value=self.ui.ResultDataCol.text().split(',')
        for i in range(len(value)):
            self.ResultDataCol.append(int(value[i])-1)
        self.ResultAmb=self.ui.ResultAmb.currentText()
        self.ResultData=readFromFileInCol(self.ResultFile,self.ResultFileHeaderline,self.ResultDataCol,str)
        if self.ResultAmb=="Fixed":
            index1=np.where(self.ResultData[:,10]==str('GNSS'))
            index2=np.where(self.ResultData[:,13]==str('Fixed'))
            index=np.intersect1d(index1,index2)
            self.ResultData=self.ResultData[index,:]
        index_float=[0,1,2,3,4,5,6,7,8,9,11,12]
        index_str=[10,13]
        self.ResultDataFloat=self.ResultData[:,index_float].astype(float)
        self.ResultDataString=self.ResultData[:,index_str]
        self.ResultBlh=tf.xyz2blh_batch(self.ResultDataFloat[:,1],self.ResultDataFloat[:,2],self.ResultDataFloat[:,3])

    def prepareRef(self):
        # self.RefFile=self.ui.RefFile.text()
        self.RefFileHeaderline=int(self.ui.RefFileHeaderline.text())
        self.RefDataCol=[]
        value=self.ui.RefDataCol.text().split(',')
        for i in range(len(value)):
            self.RefDataCol.append(int(value[i])-1)
        self.RefAmb=self.ui.RefAmb.currentText()
        self.RefData=readFromFileInCol(self.RefFile,self.RefFileHeaderline,self.RefDataCol,str)
        if self.RefAmb=="Fixed":
            index1=np.where(self.RefData[:,10]==str('GNSS'))
            index2=np.where(self.RefData[:,13]==str('Fixed'))
            index=np.intersect1d(index1,index2)
            self.RefData=self.RefData[index,:]
        index_float=[0,1,2,3,4,5,6,7,8,9,11,12]
        index_str=[10,13]
        self.RefDataFloat=self.RefData[:,index_float].astype(float)
        self.RefDataString=self.RefData[:,index_str]
        self.RefBlh=tf.xyz2blh_batch(self.RefDataFloat[:,1],self.RefDataFloat[:,2],self.RefDataFloat[:,3])
        
    def prepareState(self):
        # self.StateFile=self.ui.StateFile.text()
        self.StateFileHeaderline=int(self.ui.StateFileHeaderline.text())
        self.StateDataCol=[]
        value=self.ui.StateDataCol.text().split(',')
        for i in range(len(value)):
            self.StateDataCol.append(int(value[i])-1)
        self.StateData=readFromFileInCol(self.StateFile,self.StateFileHeaderline,self.StateDataCol,str)
        index_float=[0,1,2]
        index_str=[3]
        self.StateDataFloat=self.StateData[:,index_float].astype(float)
        self.StateDataString=self.StateData[:,index_str]
        index1=np.where(self.StateDataFloat[:,1]>0)
        index2=np.where(self.StateData[:,3]==str('Fixed'))
        self.index_fixed=np.intersect1d(index1,index2)
        index1=np.where(self.StateDataFloat[:,1]>0)
        index2=np.where(self.StateData[:,3]==str('Float'))
        self.index_float=np.intersect1d(index1,index2)
        
    def prepareDiff(self):
        self.dp=tf.diff_enu(self.ResultDataFloat[:,0],self.ResultDataFloat[:,1:4],self.RefDataFloat[:,0],self.RefDataFloat[:,1:4])
        self.dv=tf.diff_vel(self.ResultDataFloat[:,0],self.ResultDataFloat[:,4:7],self.RefDataFloat[:,0],self.RefDataFloat[:,4:7],self.RefDataFloat[:,1:4])
        self.da=tf.diff_att(self.ResultDataFloat[:,0],self.ResultDataFloat[:,7:10],self.RefDataFloat[:,0],self.RefDataFloat[:,7:10])

    def prepareAll(self):
        self.imuFile=self.ui.imuFile.text()
        if len(self.imuFile)>0:
            self.prepareImu()
        self.ResultFile=self.ui.ResultFile.text()
        if len(self.ResultFile)>0:
            self.prepareResult()
        self.RefFile=self.ui.RefFile.text()
        if len(self.RefFile)>0:
            self.prepareRef()
        self.StateFile=self.ui.StateFile.text()
        if len(self.StateFile)>0:
            self.prepareState()
        if len(self.ResultFile)>0 and len(self.RefFile)>0:
            self.prepareDiff()
        # print('Prepare Data Finish !')
        MessageBox = QMessageBox()
        MessageBox.information(QMainWindow(), "Information", "Prepare Data Finish !") 

    def plotImu(self):
        self.graphic_content_fig_g = MyFigureCanvas(width=self.ui.fig_g.width() / 101,
                                                height=self.ui.fig_g.height() / 101)
        self.graphic_scene_fig_g = QGraphicsScene()
        self.graphic_scene_fig_g.addWidget(self.graphic_content_fig_g)  # 把图形放到QGraphicsScene中，注意：图形是作为一个QWidget放到放到QGraphicsScene中的
        self.ui.fig_g.setScene(self.graphic_scene_fig_g)  # 把QGraphicsScene放入QGraphicsView
        self.graphic_content_fig_g.axes.plot(self.imuData[:,0],self.imuData[:,1],color=colors[0],linewidth=1,label='x')
        self.graphic_content_fig_g.axes.plot(self.imuData[:,0],self.imuData[:,2],color=colors[1],linewidth=1,label='y')
        self.graphic_content_fig_g.axes.plot(self.imuData[:,0],self.imuData[:,3],color=colors[2],linewidth=1,label='z')
        self.graphic_content_fig_g.axes.legend(ncol=3,numpoints=5, markerscale=2, handlelength=3,frameon=False)
        self.graphic_content_fig_g.axes.set_xlabel('Times (s)')
        self.graphic_content_fig_g.axes.set_ylabel('Gyro (deg/s)')
        self.graphic_content_fig_g.axes.set_xlim(self.imuData[0,0],self.imuData[-1,0])
        self.graphic_content_fig_g.draw()

        self.graphic_content_fig_a = MyFigureCanvas(width=self.ui.fig_a.width() / 101,
                                                height=self.ui.fig_a.height() / 101)
        self.graphic_scene_fig_a = QGraphicsScene()
        self.graphic_scene_fig_a.addWidget(self.graphic_content_fig_a)  # 把图形放到QGraphicsScene中，注意：图形是作为一个QWidget放到放到QGraphicsScene中的
        self.ui.fig_a.setScene(self.graphic_scene_fig_a)  # 把QGraphicsScene放入QGraphicsView
        self.graphic_content_fig_a.axes.plot(self.imuData[:,0],self.imuData[:,4],color=colors[0],linewidth=1,label='x')
        self.graphic_content_fig_a.axes.plot(self.imuData[:,0],self.imuData[:,5],color=colors[1],linewidth=1,label='y')
        self.graphic_content_fig_a.axes.plot(self.imuData[:,0],self.imuData[:,6],color=colors[2],linewidth=1,label='z')
        self.graphic_content_fig_a.axes.legend(ncol=3,numpoints=5, markerscale=2, handlelength=3,frameon=False)
        self.graphic_content_fig_a.axes.set_xlabel('Times (s)')
        self.graphic_content_fig_a.axes.set_ylabel('Acce (m/s2)')
        self.graphic_content_fig_a.axes.set_xlim(self.imuData[0,0],self.imuData[-1,0])
        self.graphic_content_fig_a.draw()
        return

    def plotBlh(self):        
        self.graphic_content_fig_bl = MyFigureCanvas(width=self.ui.fig_bl.width() / 101,
                                                height=self.ui.fig_bl.height() / 101)
        self.graphic_scene_fig_bl = QGraphicsScene()
        self.graphic_scene_fig_bl.addWidget(self.graphic_content_fig_bl)  # 把图形放到QGraphicsScene中，注意：图形是作为一个QWidget放到放到QGraphicsScene中的
        self.ui.fig_bl.setScene(self.graphic_scene_fig_bl)  # 把QGraphicsScene放入QGraphicsView
        self.graphic_content_fig_bl.axes.plot(self.ResultBlh[:,1]/math.pi*180,self.ResultBlh[:,0]/math.pi*180,color=colors[0],linewidth=1,label='Cal')
        if len(self.RefFile)>0:
            self.graphic_content_fig_bl.axes.plot(self.RefBlh[:,1]/math.pi*180,self.RefBlh[:,0]/math.pi*180,color=colors[1],linewidth=1,label='Ref')
        self.graphic_content_fig_bl.axes.legend(ncol=2,numpoints=5, markerscale=2, handlelength=3,frameon=False)
        self.graphic_content_fig_bl.axes.set_xlabel('Lon (deg)')
        self.graphic_content_fig_bl.axes.set_ylabel('Lat (deg)')
        self.graphic_content_fig_bl.draw()

        self.graphic_content_fig_h = MyFigureCanvas(width=self.ui.fig_h.width() / 101,
                                                height=self.ui.fig_h.height() / 101)
        self.graphic_scene_fig_h = QGraphicsScene()
        self.graphic_scene_fig_h.addWidget(self.graphic_content_fig_h)  # 把图形放到QGraphicsScene中，注意：图形是作为一个QWidget放到放到QGraphicsScene中的
        self.ui.fig_h.setScene(self.graphic_scene_fig_h)  # 把QGraphicsScene放入QGraphicsView
        self.graphic_content_fig_h.axes.plot(self.ResultDataFloat[:,0],self.ResultBlh[:,2],color=colors[0],linewidth=1,label='Cal')
        if len(self.RefFile)>0:
            self.graphic_content_fig_h.axes.plot(self.RefDataFloat[:,0],self.RefBlh[:,2],color=colors[1],linewidth=1,label='Ref')
        self.graphic_content_fig_h.axes.legend(ncol=2,numpoints=5, markerscale=2, handlelength=3,frameon=False)
        self.graphic_content_fig_h.axes.set_xlabel('Times (s)')
        self.graphic_content_fig_h.axes.set_ylabel('Height (m)')
        self.graphic_content_fig_h.axes.set_xlim(self.ResultDataFloat[0,0],self.ResultDataFloat[-1,0])
        self.graphic_content_fig_h.draw()
        return

    def plotState(self):        
        self.graphic_content_fig_state = MyFigureCanvas(width=self.ui.fig_state.width() / 101,
                                                height=self.ui.fig_state.height() / 101)
        self.graphic_scene_fig_state = QGraphicsScene()
        self.graphic_scene_fig_state.addWidget(self.graphic_content_fig_state)  # 把图形放到QGraphicsScene中，注意：图形是作为一个QWidget放到放到QGraphicsScene中的
        self.ui.fig_state.setScene(self.graphic_scene_fig_state)  # 把QGraphicsScene放入QGraphicsView
        self.graphic_content_fig_state.axes.plot(self.StateDataFloat[:,0],self.StateDataFloat[:,1],color=colors[0],linewidth=1,label='Nsat')
        self.graphic_content_fig_state.axes.set_xlim(self.StateDataFloat[0,0],self.StateDataFloat[-1,0])
        
        self.graphic_content_fig_state.axes.plot(self.StateDataFloat[:,0],self.StateDataFloat[:,2],color=colors[1],linewidth=1,label='PDOP')
        self.graphic_content_fig_state.axes.set_xlim(self.StateDataFloat[0,0],self.StateDataFloat[-1,0])
        
        self.graphic_content_fig_state.axes1=self.graphic_content_fig_state.axes.twinx()
        self.graphic_content_fig_state.axes1.scatter(self.StateDataFloat[self.index_float,0],0.01*np.ones(len(self.index_float)),s=50,color='red',marker='|',label='Float')
        self.graphic_content_fig_state.axes1.scatter(self.StateDataFloat[self.index_fixed,0],0.01*np.ones(len(self.index_fixed)),s=50,color='lime',marker='|',label='Fixed')
        self.graphic_content_fig_state.axes1.set_yticks([])
        self.graphic_content_fig_state.axes1.spines['top'].set_visible(False)
        self.graphic_content_fig_state.axes1.spines['right'].set_visible(False)
        self.graphic_content_fig_state.axes1.set_ylim(0,1)
        self.graphic_content_fig_state.axes1.set_xlim(self.StateDataFloat[0,0],self.StateDataFloat[-1,0])
        self.graphic_content_fig_state.axes1.legend(bbox_to_anchor=(0.95,0.9),ncol=2,numpoints=5, markerscale=2, handlelength=3,frameon=False)
        self.graphic_content_fig_state.axes.legend(ncol=2,numpoints=5, markerscale=2, handlelength=3,frameon=False)
        self.graphic_content_fig_state.axes.set_xlabel('Times (s)')
        self.graphic_content_fig_state.axes.set_xlim(self.StateDataFloat[0,0],self.StateDataFloat[-1,0])
        self.graphic_content_fig_state.draw()
        return

    def plotDiff(self):        
        self.graphic_content_fig_dp = MyFigureCanvas(width=self.ui.fig_dp.width() / 101,
                                                height=self.ui.fig_dp.height() / 101)
        self.graphic_scene_fig_dp = QGraphicsScene()
        self.graphic_scene_fig_dp.addWidget(self.graphic_content_fig_dp)  # 把图形放到QGraphicsScene中，注意：图形是作为一个QWidget放到放到QGraphicsScene中的
        self.ui.fig_dp.setScene(self.graphic_scene_fig_dp)  # 把QGraphicsScene放入QGraphicsView
        self.graphic_content_fig_dp.axes.plot(self.dp[:,0],self.dp[:,1],color=colors[0],linewidth=1,label='e')
        self.graphic_content_fig_dp.axes.plot(self.dp[:,0],self.dp[:,2],color=colors[1],linewidth=1,label='n')
        self.graphic_content_fig_dp.axes.plot(self.dp[:,0],self.dp[:,3],color=colors[2],linewidth=1,label='u')
        self.graphic_content_fig_dp.axes.legend(ncol=4,numpoints=5, markerscale=2, handlelength=3,frameon=False)
        self.graphic_content_fig_dp.axes.set_xlabel('Times (s)')
        self.graphic_content_fig_dp.axes.set_ylabel('Pos (m)')
        self.graphic_content_fig_dp.axes.set_xlim(self.dp[0,0],self.dp[-1,0])
        self.graphic_content_fig_dp.draw()

        self.graphic_content_fig_dv = MyFigureCanvas(width=self.ui.fig_dv.width() / 101,
                                                height=self.ui.fig_dv.height() / 101)
        self.graphic_scene_fig_dv = QGraphicsScene()
        self.graphic_scene_fig_dv.addWidget(self.graphic_content_fig_dv)  # 把图形放到QGraphicsScene中，注意：图形是作为一个QWidget放到放到QGraphicsScene中的
        self.ui.fig_dv.setScene(self.graphic_scene_fig_dv)  # 把QGraphicsScene放入QGraphicsView
        self.graphic_content_fig_dv.axes.plot(self.dv[:,0],self.dv[:,1],color=colors[0],linewidth=1,label='e')
        self.graphic_content_fig_dv.axes.plot(self.dv[:,0],self.dv[:,2],color=colors[1],linewidth=1,label='n')
        self.graphic_content_fig_dv.axes.plot(self.dv[:,0],self.dv[:,3],color=colors[2],linewidth=1,label='u')
        self.graphic_content_fig_dv.axes.legend(ncol=4,numpoints=5, markerscale=2, handlelength=3,frameon=False)
        self.graphic_content_fig_dv.axes.set_xlabel('Times (s)')
        self.graphic_content_fig_dv.axes.set_ylabel('Vel (m/s)')
        self.graphic_content_fig_dv.axes.set_xlim(self.dv[0,0],self.dv[-1,0])
        self.graphic_content_fig_dv.draw()
        
        self.graphic_content_fig_da = MyFigureCanvas(width=self.ui.fig_da.width() / 101,
                                                height=self.ui.fig_da.height() / 101)
        self.graphic_scene_fig_da = QGraphicsScene()
        self.graphic_scene_fig_da.addWidget(self.graphic_content_fig_da)  # 把图形放到QGraphicsScene中，注意：图形是作为一个QWidget放到放到QGraphicsScene中的
        self.ui.fig_da.setScene(self.graphic_scene_fig_da)  # 把QGraphicsScene放入QGraphicsView
        self.graphic_content_fig_da.axes.plot(self.da[:,0],self.da[:,1],color=colors[0],linewidth=1,label='Pitch')
        self.graphic_content_fig_da.axes.plot(self.da[:,0],self.da[:,2],color=colors[1],linewidth=1,label='Roll')
        self.graphic_content_fig_da.axes.plot(self.da[:,0],self.da[:,3],color=colors[2],linewidth=1,label='Yaw')
        self.graphic_content_fig_da.axes.legend(ncol=4,numpoints=5, markerscale=2, handlelength=3,frameon=False)
        self.graphic_content_fig_da.axes.set_xlabel('Times (s)')
        self.graphic_content_fig_da.axes.set_ylabel('Att (deg)')
        self.graphic_content_fig_da.axes.set_xlim(self.da[0,0],self.da[-1,0])
        self.graphic_content_fig_da.draw()
        return

    def plotAll(self):
        if len(self.imuFile)>0:
            self.plotImu()
        if len(self.ResultFile)>0:
            self.plotBlh()
        if len(self.StateFile)>0:
            self.plotState()
        if len(self.ResultFile)>0 and len(self.RefFile)>0:
            self.plotDiff()
        # print('Plot Finish !')
        MessageBox = QMessageBox()
        MessageBox.information(QMainWindow(), "Information", "Plot Finish !") 
    
    def clearPlot(self):
        if len(self.imuFile)>0:
            for item in self.graphic_scene_fig_g.items():
                self.graphic_scene_fig_g.removeItem(item)

            for item in self.graphic_scene_fig_a.items():
                self.graphic_scene_fig_a.removeItem(item)

        if len(self.ResultFile)>0:
            for item in self.graphic_scene_fig_bl.items():
                self.graphic_scene_fig_bl.removeItem(item)
                
            for item in self.graphic_scene_fig_h.items():
                self.graphic_scene_fig_h.removeItem(item)

        if len(self.StateFile)>0:
            for item in self.graphic_scene_fig_state.items():
                self.graphic_scene_fig_state.removeItem(item)

        if len(self.ResultFile)>0 and len(self.RefFile)>0:
            # for item in self.graphic_scene_fig_bl.items():
            #     self.graphic_scene_fig_bl.removeItem(item)
                
            # for item in self.graphic_scene_fig_h.items():
            #     self.graphic_scene_fig_h.removeItem(item)
            
            for item in self.graphic_scene_fig_dp.items():
                self.graphic_scene_fig_dp.removeItem(item)

            for item in self.graphic_scene_fig_dv.items():
                self.graphic_scene_fig_dv.removeItem(item)

            for item in self.graphic_scene_fig_da.items():
                self.graphic_scene_fig_da.removeItem(item)

        # print('Clear All Plot Finish !')
        MessageBox = QMessageBox()
        MessageBox.information(QMainWindow(), "Information", "Clear All Plot Finish !") 
        return

if __name__ == '__main__':
    app = QApplication([])
    gPlot = compareNavPlot()
    gPlot.ui.show()
    app.exit(app.exec_())