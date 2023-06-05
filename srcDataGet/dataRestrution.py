import os
import sys
current_path = os.getcwd()

# DataGet library
sys.path.insert(0, current_path)
from srcDataGet import DataGet
from multiprocessing import Process


oriDataFileName = 'Ori_point_1时刻.dat'
indexFileName = 'indexCube.dat'
oneTimeDataList = [os.path.join('MS1_FS45_8953',i)for i in['t1.dat','t2.dat','t10.dat','t12.dat']]
dataRestructionList = [os.path.join('MS1_FS45_8953',i)for i in['t1.dat','t2.dat','t10.dat','t12.dat']]

def dataRestruChild(No,indexFileName,oriDataFileName,oneTimeDataList,dataRestructionList):
    dRC = DataGet.DataRestruction(indexFileName,oriDataFileName,oneTimeDataList[No],dataRestructionList[No])
    dRC.restruction()

def main():
    # -----------------------------------------------------------
    # 2.DataRestrution
    # -----------------------------------------------------------
    pRestr0 = Process(target=dataRestruChild, args=(0,indexFileName,oriDataFileName,oneTimeDataList,dataRestructionList))
    pRestr1 = Process(target=dataRestruChild, args=(1,indexFileName,oriDataFileName,oneTimeDataList,dataRestructionList))

    pRestr0.start()
    pRestr1.start()
    pRestr0.join()
    pRestr1.join()

    print('-'*15,'重构完成','-'*15)

if __name__ == "__main__":
    main()