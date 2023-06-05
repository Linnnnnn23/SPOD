import os

import time
from datetime import datetime
import h5py
import numpy as np
import requests
import shutil
import os

current_path = os.getcwd()
parent_path = os.path.dirname(current_path)
tmp_dir_path = os.path.join(parent_path,'001tmp')
index_dir_path = os.path.join(parent_path,'002index')
xyzVol_dir_path = os.path.join(parent_path,'003XYZVol')
dataForSPOD_dir_path = os.path.join(parent_path,'004dataForSPOD')
dataSPODResults_dir_path = os.path.join(parent_path,'005dataSPODResults')
dataForRestru_dir_path = os.path.join(parent_path,'006dataForRestru')
restructionData_dir_path = os.path.join(parent_path,'007restructionData')
backup_dir_path = os.path.join(parent_path,'008backup')


def timeprint():
    now = datetime.now()
    return '%s:%s:%s' % (now.hour, now.minute, now.second)

def send_notice(content):

    token = 'd3873b42429e42e385654a089fcd2c93'
    title = 'DES消息通知'
    url = f"http://www.pushplus.plus/send?token={token}&title={title}&content={content}&template=html"
    response = requests.request("GET", url)

def gatherData(fileNameGather,fileNameList,fileRangeList,matrixSpod):
    '''

    :param fileNameGather: 集合文件的名字：eg "dataGatehr.h5"
    :param fileNameList: 各个文件名称组成的列表：eg:['DES_test1.h5','DES_test1.h5','DES_test1.h5','DES_test1.h5']
    :param fileRangeList: 各个文件对应的数据时刻：eg：[(0,100),(500,600),(1000,1100),(1500,1600)]
    :return:
    '''
    fileNameGather = os.path.join(dataForSPOD_dir_path,fileNameGather)
    fileNameList = [os.path.join(tmp_dir_path,i)for i in fileNameList]
    print('-' * 10,'开始集合数据','-'*10)
    print(fileRangeList)


    if not os.path.exists(fileNameGather):
        fGather = h5py.File(fileNameGather, 'w')
        fGather.create_dataset('data', (matrixSpod[0], matrixSpod[1]), compression="gzip")
    else:
        fGather = h5py.File(fileNameGather, 'a')
    for i in range(len(fileNameList)):
        print('时刻%s-%s'%(fileRangeList[i][0],fileRangeList[i][1]))
        fin = h5py.File(fileNameList[i], 'r')
        for j in range(fileRangeList[i][0],fileRangeList[i][1]):
            fGather['data'][j,:]=fin['data'][j,:]
        fin.close()
    fGather.close()

def addXYZV(fileNameGather,dt,matrixSpod,indexFileName):

    indexList = []
    '''
            根据index文件（来自于X，Y，Z取值范围）
            :param path: index文件位置
            :return: indexList:索引列表，截取参数时，与列表中1对应位置的参数选择
                     paraNum选择参数个数
            '''
    print('-----------开始读取Index文件------------')
    print('          Index为%s         ' % indexFileName)
    indexFilePath = os.path.join(index_dir_path, indexFileName)

    paraNum = 0
    with open(indexFilePath)as fileIn:
        while True:
            line = fileIn.readline()
            if not line:
                break
            else:
                indexList.append(int(line.split()[0]))
                if int(line.split()[0]) == 1:
                    paraNum += 1
    print('------------Index读取结束--------------')

    print('----------开始写grid及dt数据-----------')
    listX = []
    listY = []
    listZ = []
    listV = []
    fileNameGather = os.path.join(dataForSPOD_dir_path, fileNameGather)
    fGather = h5py.File(os.path.join(dataForSPOD_dir_path,fileNameGather), 'a')
    try:
        fGather.__delitem__('dt')
        fGather.__delitem__('grid')
    except:
        pass
    try:
        fGather.create_dataset('dt',shape = (1))
        fGather['dt'][:] = dt
        fGather.create_dataset('grid', shape=(matrixSpod[1], 4))
    except:
        pass
    with open(os.path.join(xyzVol_dir_path,'XYZVol.dat'))as fileIn:
        while True:
            tmp = fileIn.readline()
            if not tmp:
                break
            else:
                if tmp.startswith(' Nodes='):
                    NodesNum = int(tmp[tmp.index("=")+1:tmp.index(',')])
                if tmp.startswith(' DT=('):
                    break
        for i in range(NodesNum):
            line = fileIn.readline()
            tmp = line.split()
            x = float(tmp[0])
            y = float(tmp[1])
            z = float(tmp[2])
            v = float(tmp[3])
            if indexList[i]==1:
                listX.append(x)
                listY.append(y)
                listZ.append(z)
                listV.append(v)
        XnP = np.array(listX)
        YnP = np.array(listY)
        ZnP = np.array(listZ)
        VnP = np.array(listV)

    fGather['grid'][:,0]=XnP
    fGather['grid'][:,1]=YnP
    fGather['grid'][:,2]=ZnP
    fGather['grid'][:,3]=VnP
    fGather.close()
    print('----------grid及dt数据写入完成-----------')

def volumeFromAll(indexFileName,dataForSPOD_All,dataForSPOD_volume,volumeShape,methed = 'fast'):
    IndexList = []
    indexFileName = os.path.join(index_dir_path,indexFileName)
    dataForSPOD_All = os.path.join(dataForSPOD_dir_path,dataForSPOD_All)
    dataForSPOD_volume = os.path.join(dataForSPOD_dir_path,dataForSPOD_volume)
    with open(indexFileName, 'r')as fileIn:
        while True:
            line = fileIn.readline()
            if not line:
                break
            else:
                tmp = line.split()
                IndexList.append(int(tmp[0]))

    time1_start = time.time()
    fin = h5py.File(dataForSPOD_All, 'r')
    fout = h5py.File(dataForSPOD_volume, 'w')
    dataSet = fout.create_dataset('data', shape=(volumeShape[0], volumeShape[1]))
    L = fin['data'][:]
    Lft = np.zeros((volumeShape[0], volumeShape[1]))

    time1_end = time.time()
    print('time1%s' % (time1_end - time1_start))

    if methed == 'fast':
        time2_start = time.time()
        k = 0
        for i in range(len(IndexList)):
            if IndexList[i] == 1:
                Lft[:, k] = L[:, i]
                k += 1
        dataSet[:] = Lft[:]
        time2_end = time.time()
        print('time2%s' % (time2_end - time2_start))
    else:
        pass
    fin.close()
    fout.close()

class DataGet:

    def __init__(self,matrixSpod,Variable,xRange,yRange,zRange,ntRange,port,h5Name,fileNameTmp,ntBackup):
        print('Spod 矩阵为%sx%s'%(matrixSpod[0],matrixSpod[1]))
        print('参数为%s,在tecplot中为第%s个参数'%(Variable[0],Variable[1]))
        print('取值范围为x[%s,%s],y[%s,%s],z[%s,%s]'%(xRange[0],xRange[1],yRange[0],yRange[1],zRange[0],zRange[1]))
        print('时刻范围为[%s,%s]'%(ntRange[0],ntRange[1]))
        print('port为%s'%port)
        print('h5Name为："%s"'%h5Name)
        print('临时文件为："%s"'%fileNameTmp)
        self.matrixSpod = matrixSpod
        self.Variable = Variable[1]
        self.xRange = xRange
        self.yRange = yRange
        self.zRange = zRange
        self.ntRange = ntRange
        self.port = port

        self.h5Name = os.path.join(tmp_dir_path, h5Name)
        self.fileNameTmp = os.path.join(tmp_dir_path,fileNameTmp)
        self.ntBackup = ntBackup
        self.indexList = []

    def indexFromFile(self,fileNameIndex):
        print('----------------')
        print('Step1：从XYZVol.dat里读xyzRange对应区域索引并写入文件')
        sec1_start = time.time()
        Num = 0
        with open(os.path.join(index_dir_path,fileNameIndex), 'w')as fileOut:
            with open(os.path.join(xyzVol_dir_path,'XYZVol.dat'))as fileIn:
                while True:
                    tmp = fileIn.readline()
                    if not tmp:
                        break
                    else:
                        if tmp.startswith(' Nodes='):
                            self.NodesNum = int(tmp[tmp.index("=") + 1:tmp.index(',')])
                        if tmp.startswith(' DT=('):
                            break
                for i in range(self.NodesNum):
                    line = fileIn.readline()
                    tmp = line.split()
                    x = float(tmp[0])
                    y = float(tmp[1])
                    z = float(tmp[2])
                    p = float(tmp[3])
                    if x > self.xRange[0] and x < self.xRange[1] \
                            and y > self.yRange[0] and y < self.yRange[1] \
                            and z > self.zRange[0] and z < self.zRange[1]:
                        self.indexList.append(i)
                        Num+=1
                        fileOut.write('1\n')
                    else:
                        fileOut.write('0\n')
        print(Num)
        sec1_end = time.time()
        print('用时%s秒' % (sec1_end - sec1_start))
        print('----------------')
        print('                ')

    def sliceIndexFromFile(self, sliceNo, sliceIndex):
        sliceNo+=1
        print('----------------')
        print('从XYZVol.dat里读xyzRange对应区域索引并写入文件')
        sec1_start = time.time()
        with open(os.path.join(index_dir_path,'indexSlice%s.dat'%sliceIndex[sliceNo][0]), 'w')as fileOut:
            with open(os.path.join(xyzVol_dir_path,'XYZVol.dat'),'r')as fileIn:
                while True:
                    tmp = fileIn.readline()
                    if not tmp:
                        break
                    else:
                        if tmp.startswith(' Nodes='):
                            self.NodesNum = int(tmp[tmp.index("=") + 1:tmp.index(',')])
                        if tmp.startswith(' DT=('):
                            break
                for i in range(self.NodesNum):
                    line = fileIn.readline()
                    tmp = line.split()
                    x = float(tmp[0])
                    y = float(tmp[1])
                    z = float(tmp[2])
                    p = float(tmp[3])


                    if sliceIndex[0] == 'x':
                        if x > sliceIndex[sliceNo][0] and x < sliceIndex[sliceNo][1] \
                                and y > self.yRange[0] and y < self.yRange[1] \
                                and z > self.zRange[0] and z < self.zRange[1]:
                            self.indexList.append(i)
                            fileOut.write('1\n')
                        else:
                            fileOut.write('0\n')

                    if sliceIndex[0] == 'y':
                        if y > sliceIndex[sliceNo][0] and y < sliceIndex[sliceNo][1]\
                                and x > self.xRange[0] and x < self.xRange[1] \
                                and z > self.zRange[0] and z < self.zRange[1]:
                            self.indexList.append(i)
                            if i == 1:
                                print(x, y, z)
                            fileOut.write('1\n')
                        else:
                            fileOut.write('0\n')

                    if sliceIndex[0] == 'z':
                        if z > sliceIndex[sliceNo][0] and z < sliceIndex[sliceNo][1]\
                                and x > self.yRange[0] and x < self.yRange[1] \
                                and y > self.yRange[0] and y < self.zRange[1]:
                            self.indexList.append(i)
                            if i == 1:
                                print(x, y, z)
                            fileOut.write('1\n')
                        else:
                            fileOut.write('0\n')
        sec1_end = time.time()
        print('用时%s秒' % (sec1_end - sec1_start))
        print('----------------')
        print('                ')

    def indexGet(self,indexFileName):
        '''
        根据index文件（来自于X，Y，Z取值范围）
        :param path: index文件位置
        :return: indexList:索引列表，截取参数时，与列表中1对应位置的参数选择
                 paraNum选择参数个数
        '''
        print('-----------开始读取Index文件------------')
        print('          Index为%s         '%indexFileName)
        self.indexFilePath = os.path.join(index_dir_path,indexFileName)

        self.paraNum = 0
        with open(self.indexFilePath)as fileIn:
            while True:
                line = fileIn.readline()
                if not line:
                    break
                else:
                    self.indexList.append(int(line.split()[0]))
                    if int(line.split()[0])==1:
                        self.paraNum+=1
        print('------------Index读取结束--------------')
        return self.indexList

    def h5fileDataCreat(self):
        if not os.path.exists(self.h5Name):
            self.f = h5py.File(self.h5Name, 'w')
            self.f.create_dataset('data', (self.matrixSpod[0], self.matrixSpod[1]), compression="gzip")
        else:
            self.f = h5py.File(self.h5Name, 'a')

    def datapath(self,Number):
        '''
        通过给定数据的No，返回数据对应的文件位置
        :param Number: DataNumber
        :return: Trnpath
        '''
        self.folderNo = (int(Number/100)+1)*500 # 分段文件夹的No
        self.TrnPath  = r'E:\Data\DES_2048\output_20221019_DES_%s\20221019_DES_%s_001\%s.trn'%(self.folderNo,self.folderNo,1000+Number*5)
        return self.TrnPath



    # def datapath(self,Number):
    #     '''
    #     通过给定数据的No，返回数据对应的文件位置
    #     :param Number: DataNumber
    #     :return: Trnpath
    #     '''
    #     self.folderNo = (int(Number/100)+1)*500 # 分段文件夹的No
    #     self.TrnPath  = r'E:\Data\LES_2048\output_20221019_LES_%s\20221019_LES_%s_001\%s.trn'%(self.folderNo,self.folderNo,1000+Number*5)
    #     return self.TrnPath



    def dataGet(self,Number):
        import tecplot as tp
        # Uncomment the following line to connect to a running instance of Tecplot 360:
        tp.session.connect(port=self.port)
        tp.macro.execute_command('$!FrameControl DeleteTop')
        tp.macro.execute_command("""$!ReadDataSet  '\"StandardSyntax\" \"1.0\" \"FEALoaderVersion\" \"461\" \"FILENAME_File\" \"%s\" \"AutoAssignStrandIDs\" \"Yes\"'
          DataSetReader = 'ANSYS CFX (FEA)'"""%self.datapath(Number))

        tp.data.save_tecplot_ascii('%s'%self.fileNameTmp,
                                   zones=[0],
                                   variables=[self.Variable],
                                   include_text=False,
                                   precision=9,
                                   include_geom=False,
                                   include_data_share_linkage=True,
                                   use_point_format=True)

    def tmp2NpP(self):
        self.listP = []
        with open(self.fileNameTmp)as fileIn:
            while True:
                tmp = fileIn.readline()
                if not tmp:
                    break
                else:
                    if tmp.startswith(' Nodes='):
                        self.NodesNum = int(tmp[tmp.index("=")+1:tmp.index(',')])
                    if tmp.startswith(' DT=('):
                        break
            for i in range(self.NodesNum):
                line = fileIn.readline()
                tmp = line.split()
                p = float(tmp[0])
                if self.indexList[i]==1:
                    self.listP.append(p)
            print(len(self.listP))
            self.listNpP = np.array(self.listP)
        # return listNpP

    def NpP2h5(self,number):
        self.dataset = self.f['data']
        self.dataset[number,:] = self.listNpP

    def backup(self,number):
        self.f.close()
        try:
            print("开始备份，备份时刻为%s" %number)
            shutil.copy(self.h5Name, self.h5Name[:-3]+'_backup%s.h5' %number)
            try:
                os.remove(self.h5Name[:-3]+'_backup%s.h5' % (number - self.ntBackup))
            except:
                pass
        except:
            pass
        self.h5fileDataCreat()

    def gatherData(self,fileNameGather,fileNameList,fileRangeList):
        '''

        :param fileNameGather: 集合文件的名字：eg "dataGatehr.h5"
        :param fileNameList: 各个文件名称组成的列表：eg:['DES_test1.h5','DES_test1.h5','DES_test1.h5','DES_test1.h5']
        :param fileRangeList: 各个文件对应的数据时刻：eg：[(0,100),(500,600),(1000,1100),(1500,1600)]
        :return:
        '''
        fileNameGather = os.path.join(dataForSPOD_dir_path,fileNameGather)

        print('-'*40)

        if not os.path.exists(fileNameGather):
            self.fGather = h5py.File(fileNameGather, 'w')
            self.fGather.create_dataset('data', (self.matrixSpod[0], self.matrixSpod[1]), compression="gzip")
        else:
            self.fGather = h5py.File(fileNameGather, 'a')
        for i in range(len(fileNameList)):
            print('时刻%s-%s'%(fileRangeList[i][0],fileRangeList[i][1]))
            fin = h5py.File(fileNameList[i], 'r')
            for j in range(fileRangeList[i][0],fileRangeList[i][1]):
                self.fGather['data'][j,:]=fin['data'][j,:]
            fin.close()
        self.fGather.close()

    def addXYZV(self,fileNameGather,dt):

        self.listX = []
        self.listY = []
        self.listZ = []
        self.listV = []
        fileNameGather = os.path.join(dataForSPOD_dir_path, fileNameGather)
        self.fGather = h5py.File(fileNameGather, 'a')
        try:
            self.fGather.__delitem__('dt')
            self.fGather.__delitem__('grid')
        except:
            pass
        try:
            self.fGather.create_dataset('dt',shape = (1))
            self.fGather['dt'][:] = dt
            self.fGather.create_dataset('grid', shape=(self.matrixSpod[1], 4))
        except:
            pass
        with open(os.path.join(xyzVol_dir_path,'XYZVol.dat'))as fileIn:
            while True:
                tmp = fileIn.readline()
                if not tmp:
                    break
                else:
                    if tmp.startswith(' Nodes='):
                        self.NodesNum = int(tmp[tmp.index("=")+1:tmp.index(',')])
                    if tmp.startswith(' DT=('):
                        break
            for i in range(self.NodesNum):
                line = fileIn.readline()
                tmp = line.split()
                x = float(tmp[0])
                y = float(tmp[1])
                z = float(tmp[2])
                v = float(tmp[3])
                if self.indexList[i]==1:
                    self.listX.append(x)
                    self.listY.append(y)
                    self.listZ.append(z)
                    self.listV.append(v)
            XnP = np.array(self.listX)
            YnP = np.array(self.listY)
            ZnP = np.array(self.listZ)
            VnP = np.array(self.listV)

        self.fGather['grid'][:,0]=XnP
        self.fGather['grid'][:,1]=YnP
        self.fGather['grid'][:,2]=ZnP
        self.fGather['grid'][:,3]=VnP
        self.fGather.close()



class DataRestruction:
    '''
    将已从h5中得到的单一时刻的spod数据按照index序列重构
    '''
    def __init__(self,indexFileName,oriData,oneTimeData,dataRestruction):
        '''
        :param oriData: 原始流场
        :param oneTimeData: 已从h5中得到的单一时刻的spod数据文件名
        :param dataRestruction: 重构结果的文件名
        '''
        self.oriData     = os.path.join(dataForRestru_dir_path,oriData)
        self.oneTimeData = os.path.join(dataForRestru_dir_path,oneTimeData)
        self.dataRestruction = os.path.join(restructionData_dir_path,dataRestruction)
        self.indexList = []
        self.indexFileName = os.path.join(index_dir_path,indexFileName)
    def restruction(self):
        print('-'*90)
        print('开始重构%s'%self.oneTimeData)
        sec3_start = time.time()
        listP = []
        with open(self.oneTimeData)as fileIn:
            while True:
                line = fileIn.readline()
                if not line:
                    break
                else:
                    listP.append(float(line.split()[0]))

        # 重构

        with open(self.indexFileName)as fileIn:
            while True:
                line = fileIn.readline()
                if not line:
                    break
                else:
                    tmp = int(line.split()[0])
                    self.indexList.append(tmp)
        print(len(self.indexList))

        k = 0
        with open(self.dataRestruction, 'w')as fileOut:
            with open(self.oriData)as fileIn:
                while True:
                    tmp = fileIn.readline()
                    if not tmp:
                        break
                    else:
                        fileOut.write(tmp)
                        if tmp.startswith(' Nodes='):
                            self.NodesNum = int(tmp[tmp.index("=") + 1:tmp.index(',')])
                        if tmp.startswith(' DT=('):
                            break
                for i in range(self.NodesNum):
                    tmp = fileIn.readline()
                    if self.indexList[i] == 0:
                        fileOut.write(tmp)
                    else:
                        x = tmp.split()[0]
                        y = tmp.split()[1]
                        z = tmp.split()[2]
                        fileOut.write('%s\t%s\t%s\t%s\n' % (x, y, z, listP[k]))
                        k += 1
                while True:
                    line = fileIn.readline()
                    if not line:
                        break
                    else:
                        fileOut.write(line)
        sec3_end = time.time()
        print('开始重构%s'%self.oneTimeData,'用时%s秒' % round((sec3_end - sec3_start),4))
        print('-'*90)

class IndexFromParent:
    def __init__(self,pNum,fileNameIndexParent,fileNameIndexSlice,h5ParentData,h5SliceData):


        self.IndexParent = []
        self.IndexSlice  = []

        fileNameIndexParent = os.path.join(index_dir_path,fileNameIndexParent)
        fileNameIndexSlice = os.path.join(index_dir_path,fileNameIndexSlice)

        h5ParentData = os.path.join(dataForSPOD_dir_path,h5ParentData)
        h5SliceData = os.path.join(dataForSPOD_dir_path, h5SliceData)

        self.h5SliceData = h5py.File(h5SliceData,'w')
        self.h5ParentData =  h5py.File(h5ParentData,'r')

        with open(fileNameIndexParent)as fileIn:
            while True:
                tmp = fileIn.readline()
                if not tmp:
                    break
                else:
                    self.IndexParent.append(int(tmp[0]))
        with open(fileNameIndexSlice)as fileIn:
            while True:
                tmp = fileIn.readline()
                if not tmp:
                    break
                else:
                    self.IndexSlice.append(int(tmp[0]))




        self.Num = 0
        for i in range(len(self.IndexParent)):
            if self.IndexParent[i]==1:
                if self.IndexSlice[i]==1:
                    self.Num += 1

        self.sliceDataSet = self.h5SliceData.create_dataset('data',shape=(2048,self.Num))
        self.sliceGridSet = self.h5SliceData.create_dataset('grid',shape=(self.Num,4))
        self.sliceDtSet = self.h5SliceData.create_dataset('dt',shape=(1))

        self.datasetParent = self.h5ParentData['data']
        self.gridsetParent = self.h5ParentData['grid']
        self.dtsetParent = self.h5ParentData['dt']



        self.noParent = 0
        self.noSlice = 0
        self.D = np.zeros((2048,self.Num))
        self.G = np.zeros((self.Num,4))





        for i in range(len(self.IndexParent)):
            if self.IndexParent[i]==1:
                if self.IndexSlice[i]==1:
                    self.D[:,self.noSlice] = self.datasetParent[:,self.noParent]
                    self.G[self.noSlice,:] = self.gridsetParent[self.noParent,:]
                    self.noSlice += 1
                self.noParent+=1
            if pNum == 0 or pNum == 3:
                if i % 100000 == 0:
                    print(i)
                if self.noSlice >= 1:
                    if self.noSlice == 1:
                        print('开始提取有效数据')
                    if self.noSlice < self.Num:
                        if self.noSlice % 20 == 1:
                            print(pNum,i,self.Num-self.noSlice)
                    if self.noSlice == self.Num:
                        print('数据已经提取完')
                        break


        self.sliceDataSet[:] = self.D
        self.sliceGridSet[:] = self.G
        self.sliceDtSet[:] = self.dtsetParent[:]

        self.h5SliceData.close()
        self.h5ParentData.close()











# def main():
#     gDP0 = DataGet(matrixSpod, Variable, xRange, yRange, zRange, ntRange, port, h5Name, fileNameTmp, ntBackup)
#     gDP0.gatherData(fileNameGather,h5Name,ntRange)
#     # gDP0.indexGet(fileIndexPath)
#     # gDP0.addXYZV(fileNameXYZ,5e-6)
# if __name__ == '__main__':
#     main()

