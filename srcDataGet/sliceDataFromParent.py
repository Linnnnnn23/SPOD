import os
import sys

current_path = os.getcwd()
parent_dir_path = os.path.dirname(current_path)
# DataGet library
sys.path.insert(0, parent_dir_path)
from srcDataGet import DataGet

import h5py
from multiprocessing import Process





def child(pNum,IndexParent,IndexSlice,dataParent,dataSlice):
    gDP = DataGet.IndexFromParent(pNum,IndexParent, IndexSlice,dataParent,dataSlice)

def main():

    p0 = Process(target=child,args=(0,'index_All.dat', 'indexSlice0.04599.dat','dataForSPOD_All.h5','dataForSPOD_TipCubeSlice0.04599.h5'))
    p1 = Process(target=child,args=(1,'index_All.dat', 'indexSlice0.05649.dat','dataForSPOD_All.h5','dataForSPOD_TipCubeSlice0.04599.h5'))
    p2 = Process(target=child,args=(2,'index_All.dat', 'indexSlice0.06546.dat','dataForSPOD_All.h5','dataForSPOD_TipCubeSlice0.06546.h5'))
    p3 = Process(target=child,args=(3,'index_All.dat', 'indexSlice0.07539.dat','dataForSPOD_All.h5','dataForSPOD_TipCubeSlice0.07539.h5'))
    p4 = Process(target=child,args=(4,'index_All.dat', 'indexSlice0.08499.dat','dataForSPOD_All.h5','dataForSPOD_TipCubeSlice0.08499.h5'))
    p5 = Process(target=child,args=(5,'index_All.dat', 'indexSlice0.09519.dat','dataForSPOD_All.h5','dataForSPOD_TipCubeSlice0.09519.h5'))
    p6 = Process(target=child,args=(6,'index_All.dat', 'indexSlice0.106.dat','dataForSPOD_All.h5','dataForSPOD_TipCubeSlice0.106.h5'))
    p7 = Process(target=child,args=(7,'index_All.dat', 'indexSlice0.1151.dat','dataForSPOD_All.h5','dataForSPOD_TipCubeSlice0.1151.h5'))


    p0.start()
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p5.start()
    p6.start()
    p7.start()

    p0.join()
    p1.join()
    p2.join()
    p3.join()
    p4.join()
    p5.join()
    p6.join()
    p7.join()

if __name__ == '__main__':
    main()