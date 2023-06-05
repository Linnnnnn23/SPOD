import time
from multiprocessing import Process
from multiprocessing import Pool
import os
import sys


# DataGet library
current_path = os.getcwd()
parent_dir_path = os.path.dirname(current_path)
# DataGet library
sys.path.insert(0, parent_dir_path)
from srcDataGet import DataGet

# variables

matrixSpod = (2048,45597)
Variable = ('压力',7)

# xRange = (-0.04,0.16)
# yRange = (0.0001,0.022)
# zRange = (0.021,0.041)

xRange = (-0.04,0.2)
yRange = (-0.005,0.04)
zRange = (-0.021,0.041)

ntBackup = 25
ntSendMessage = 25
dt = 5e-6

# ntRange = [(0,10),(512,513),(1024,1536),(1536,2048),(1726,1800),(1826,1900),(1926,2000),(2000,2048)]
# port = [7600,7601,7602,7603,7604,7605,7606,7607]
ntRange = [(0,1),(512,513),(1024,1025),(1536,1537)]
port = [7600,7601,7602,7603]
h5Name = ['DES_test0.h5','DES_test1.h5','DES_test2.h5','DES_test3.h5']
fileNameTmp= ['tmp0.dat','tmp1.dat','tmp2.dat','tmp3.dat']
fileNameGather = 'dataForSPOD_TipCubeSlice0.04599.h5'
fileNameXYZVol = 'XYZVol.dat'
fileIndexPath ='indexSlice0.04599.dat'
fileForRestru = 'Ori_point_1时刻.dat'


sliceRange=['x',(0.04599,0.04601),(0.05649,0.05651),(0.06546,0.06551),(0.07539,0.07541),(0.08499,0.08501),(0.09519,0.09501)
    ,(0.1060,0.01061),(0.1151,0.01152)]

processList = []


def dataGetChild(No,ntRange,port,h5Name,fileNameTmp):
    ntRange = ntRange[No-4]
    port = port[No-4]
    h5Name = h5Name[No-4]
    fileNameTmp = fileNameTmp[No-4]

    # ----------------------------------------------------------
    # 1.建立GetDataPoint对象
    # ----------------------------------------------------------
    gDP0 = DataGet.DataGet(matrixSpod, Variable, xRange, yRange, zRange, ntRange, port, h5Name, fileNameTmp, ntBackup)

    # ----------------------------------------------------------
    # 2.从XYZVol.dat中获得indexAll或者index_xslice
    # ----------------------------------------------------------
    # gDP0.indexFromFile('index_TipCube.dat')
    # gDP0.sliceIndexFromFile(No,sliceRange)

    # ----------------------------------------------------------
    # 3.indexAll.dat中获得self.indexList
    # ----------------------------------------------------------
    gDP0.indexGet(fileIndexPath)

    # ----------------------------------------------------------
    # 4.建立临时h5文件
    # ----------------------------------------------------------
    # gDP0.h5fileDataCreat()

    # ----------------------------------------------------------
    # 5.调用tecplot提取数据并存入h5临时文件中
    # ----------------------------------------------------------


    # for i in range(gDP0.ntRange[0], gDP0.ntRange[1]):
    #     eachtime_start = time.time()
    #     print('--------DES%s  开始读第%s个时刻---------' % (No,i))
    #
    #     # -------------------------------------------
    #     # 5.1调用tecplot, 将对应的数据保存至tmp.dat中
    #     # -------------------------------------------
    #     gDP0.dataGet(i)
    #
    #     # -------------------------------------------
    #     # 5.2将tmp.dat中的数据读入np的数组中
    #     # -------------------------------------------
    #     gDP0.tmp2NpP()
    #
    #     # -------------------------------------------
    #     # 5.3将Np数组中的数据写入gather的h5文件中
    #     # -------------------------------------------
    #
    #     gDP0.NpP2h5(i)
    #     eachtime_end = time.time()
    #     eachtime = eachtime_end - eachtime_start
    #     print('用时：%s,还剩%s小时' % (round(eachtime, 2), round(eachtime * (gDP0.ntRange[1] - i - 1) / 3600, 2)))
    #     if i % ntBackup == 0 and i != 0:
    #         gDP0.backup(i)
    #     if i % ntSendMessage == 0 and i != ntRange[0]:
    #         DataGet.send_notice('DES%s   %s时刻数据  已完成' % (No, i))
    #
    # time.sleep(1)
    #
    # gDP0.f.close()
    # DataGet.send_notice('DES%s   所有时刻数据  已完成' % No)

    # ----------------------------------------------------------

def main():

    # # ----------------------------------------------------
    # # 1、DataGet
    # # ----------------------------------------------------
    # p0 =  Process(target=dataGetChild,args=(4,ntRange,port,h5Name,fileNameTmp))
    # p1 =  Process(target=dataGetChild,args=(5,ntRange,port,h5Name,fileNameTmp))
    # p2 =  Process(target=dataGetChild,args=(6,ntRange,port,h5Name,fileNameTmp))
    # p3 =  Process(target=dataGetChild,args=(7,ntRange,port,h5Name,fileNameTmp))
    #
    # p0.start()
    # p1.start()
    # p2.start()
    # p3.start()
    # #
    # p0.join()
    # p1.join()
    # p2.join()
    # p3.join()

    # DataGet.gatherData(fileNameGather,h5Name,ntRange,matrixSpod)
    DataGet.addXYZV(fileNameGather,dt,matrixSpod,fileIndexPath)


if __name__ == '__main__':
    main()
