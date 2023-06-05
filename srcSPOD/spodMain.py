"""
Application of SPOD to compressor blade surface blade data by DDES.
Details of the data can be found in the following:

  He, X., Zhao, F., & Vahdati, M. (2022). Detached Eddy Simulation: Recent
  Development and Application to Compressor Tip Leakage Flow. ASME Journal
  of Turbomachinery, 144(1), 011009.

Xiao He (xiao.he2014@imperial.ac.uk)
Last update: 24-Sep-2021
"""
from multiprocessing import Process

def spodMain(dataForSPODName,saveName,getOneTimeList,MsRange=(0,0),FsRange=(0,0),savefig = True,
             restructime = (1000,3),spodMain = True,Spectrum = True,para = 'v',pararange =(-10,11,21)):
    # -------------------------------------------------------------------------
    # 0. Import libraries
    # standard python libraries
    import sys
    import time
    import matplotlib.pyplot as plt
    from matplotlib import cm
    import imageio
    import psutil
    import os
    import numpy as np
    import h5py
    import pylab
    import io

    # all path
    srcSPOD_dir_path = os.getcwd()
    parent_dir_path = os.path.dirname(srcSPOD_dir_path)

    if MsRange == (0, 0) and FsRange == (0, 0):
        MSFSdir = 'MSAll_FSAll'
    else:
        MSFSdir = 'MS%s-%s_FS%s-%s' % (MsRange[0], MsRange[1], FsRange[0], FsRange[1])
        T = 1 / FsRange[1] / 195
        dataNumInOneT = int(T * 200000)
        getOneTimeList = [restructime[0] + i for i in range(dataNumInOneT * restructime[1])]

    dataForSPOD_path = os.path.join(parent_dir_path, '004dataForSPOD', dataForSPODName)

    dataSPODResults_dir_path = os.path.join(parent_dir_path, '005dataSPODResults', saveName)
    if not os.path.exists(dataSPODResults_dir_path):
        os.makedirs(dataSPODResults_dir_path)

    dataForRestru_dir_path = os.path.join(parent_dir_path, '006dataForRestru', saveName, MSFSdir)
    if not os.path.exists(dataForRestru_dir_path):
        os.makedirs(dataForRestru_dir_path)


    dataRestruction_dir_path = os.path.join(parent_dir_path, '007restructionData', saveName, MSFSdir)
    if not os.path.exists(dataRestruction_dir_path):
        os.makedirs(dataRestruction_dir_path)

    # SPOD library
    sys.path.insert(0, parent_dir_path)
    from srcSPOD import spod
    from srcDataGet import DataGet
    # -------------------------------------------------------------------------
    # 1. Load input data for SPOD
    # data shape: nrow = nt (total number of snapshots)
    #             ncol = ngrid*nvar (number of grid point * number of variable)
    # grid shape: nrow = ngrid (number of grid)
    #             ncol = 3 (e.g., x, r, control volume size)
    # In this case, nt = 1701, ngrid = 7086, and nvar = 1 (e.g., p)
    # -------------------------------------------------------------------------

    # Sec. 1 start time
    start_sec1 = time.time()


    # load data from h5 format
    h5f = h5py.File(os.path.join(dataForSPOD_path), 'r')
    if para == 'p':
        data = h5f['data'][:, 45597 * 0:45597 * 1]  # flow field
    elif para == 'v':
        data = h5f['data'][:,45597*2:45597*3]  # flow fields
    elif para == 'w':
        data = h5f['data'][:,45597*3:45597*4]  # flow fields
    grid = h5f['grid'][:]  # grid points
    dt = h5f['dt'][0]  # unit in seconds
    ng = int(grid.shape[0])  # number of grid point
    nt = data.shape[0]  # number of snap shot
    nx = data.shape[1]  # number of grid point * number of variable
    nvar = int(nx / ng)  # number of variables
    h5f.close()

    # calculate weight
    weight_grid = grid[:, 3]  # control volume weighted
    weight_grid = weight_grid / np.mean(weight_grid)  # normalized by mean values for better scaling
    weight_phy = np.ones(ng)  # sigle variable does not require weights from physics
    weight = weight_grid * weight_phy  # element-wise multiplation

    # Sec. 1 end time
    end_sec1 = time.time()

    print('--------------------------------------')
    print('SPOD input data summary:')
    print('--------------------------------------')
    print('number of snapshot   :', nt)
    print('number of grid point :', ng)
    print('number of variable   :', nvar)
    print('--------------------------------------')
    print('SPOD input data loaded!')
    print('Time lapsed: %.2f s' % (end_sec1 - start_sec1))
    print('--------------------------------------')

    # -------------------------------------------------------------------------
    # 2. Run SPOD
    # function spod.spod(data_matrix,timestep)
    # -------------------------------------------------------------------------

    # Sec. 2 start time
    start_sec2 = time.time()

    # main function
    if spodMain == True:
        spod.spod(data, dt, dataSPODResults_dir_path, weight, nDFT=1024, nOvlp=880, method='fast')

    # Sec. 2 end time
    end_sec2 = time.time()

    print('--------------------------------------')
    print('SPOD main calculation finished!')
    print('Time lapsed: %.2f s' % (end_sec2 - start_sec2))
    print('--------------------------------------')

    # -------------------------------------------------------------------------
    # 3. Read SPOD result
    # -------------------------------------------------------------------------

    # Sec. 3 start time
    start_sec3 = time.time()

    # load data from h5 format
    SPOD_LPf = h5py.File(os.path.join(dataSPODResults_dir_path, 'SPOD_LPf.h5'), 'r')
    L = SPOD_LPf['L'][:, :]  # modal energy E(f, M)
    P = SPOD_LPf['P'][:, :, :]  # mode shape
    f = SPOD_LPf['f'][:]  # frequency
    SPOD_LPf.close()

    # Sec. 3 end time
    end_sec3 = time.time()

    print('--------------------------------------')
    print('SPOD results read in!')
    print('Time lapsed: %.2f s' % (end_sec3 - start_sec3))
    print('--------------------------------------')

    # -------------------------------------------------------------------------
    # 4. Plot SPOD result
    # Figs: 1. f-mode energy;
    #       2. get reconstructed flow field data
    #       3. get oneTime data from rec_data
    # -------------------------------------------------------------------------

    # Sec. 4 start time
    start_sec4 = time.time()

    # -------------------------------------------------------------------------
    ### 4.0 pre-defined function
    params = {
        'axes.labelsize': '20',
        'xtick.labelsize': '16',
        'ytick.labelsize': '16',
        'lines.linewidth': 1.5,
        'legend.fontsize': '14',
        'figure.figsize': '8, 6'  # set figure size
    }
    pylab.rcParams.update(params)

    def figure_format(xtitle, ytitle, legend):
        plt.xlabel(xtitle)
        plt.ylabel(ytitle)
        # plt.axis(zoom)
        if legend != 'None':
            plt.legend(loc=legend)

    def comp_contour(q, qlevels, qname, x, y, colormap=cm.coolwarm):
        '''
        Purpose: template for comp 2D contour plot
        '''

        fig, axs = plt.subplots(1, figsize=(9, 12))

        cntr = axs.tricontourf(x[:41205], y[:41205],
                               q[:41205], qlevels, cmap=colormap, extend='both')

        cntr = axs.tricontourf(x[41205:], y[41205:],
                               q[41205:], qlevels, cmap=colormap, extend='both')


        fig.colorbar(cntr, ax=axs, ticks=np.linspace(qlevels[0], qlevels[-1], 3), shrink=0.8, extendfrac='auto',
                     orientation='horizontal', pad=0.15, label=qname)

        # fig.subplots_adjust(wspace=0.4)

        return fig

    def comp_contour_anim(t_start, t_end, t_delta, dt, ani_save_name, q, qlevels,
                          qname, x, y, colormap=cm.coolwarm):
        '''
        Purpose: plot and save animation of comp 2D contour plot
        '''
        with imageio.get_writer(os.path.join(dataRestruction_dir_path, ani_save_name), mode='I') as writer:
            # loop over snapshots
            for ti in range(t_start, t_end, t_delta):
                fig = comp_contour(q[ti, :], qlevels, qname, x, y)
                buf = io.BytesIO()
                fig.savefig(buf, format='png', dpi=50)
                buf.seek(0)

                # read png in and plot gif
                image = imageio.imread(buf)
                writer.append_data(image)

                # release RAM
                plt.close(fig)

        return
    # -------------------------------------------------------------------------
    ### 4.1 Energy spectrum
    fig = spod.plot_spectrum(f, L, hl_idx=3)

    # figure format
    figure_format(xtitle='f/Hz', ytitle='SPOD mode energy',
                  legend='best')


    plt.savefig(os.path.join(dataSPODResults_dir_path, 'Spectrum.png'), dpi=300, bbox_inches='tight')
    plt.close()

    print('Plot spectrum finished')

    if Spectrum == True:
        with open(os.path.join(dataSPODResults_dir_path,'Spectrum.dat'),'w')as fileOut:
            fileOut.write('Variables = "f","Energy"\n')
            for i in range(L.shape[1]):
                fileOut.write("Zone T = mode%s\n"%i)
                for i1 in range(f.shape[0]):
                    fileOut.write("%018.12E\t%018.12E\n"%(f[i1],L[i1][i]))
                fileOut.write('\n\n')

    # -------------------------------------------------------------------------

    ### 4.2 Original flow field
    data_mean = np.mean(data, axis=0)  # time-averaged data

    # plot snapshot flow field
    plot_snapshot = [1500, 1600, 1700, 1800, 1900]  # [t1,t2,...] to be plotted

    for i in range(len(plot_snapshot)):
        ti = plot_snapshot[i]

        fig = plt.figure(figsize=(6, 4))
        if para == 'p':
            fig = comp_contour(data[ti, :] - data_mean, np.arange(pararange[0], pararange[1], pararange[2]),
                               r'$p-\bar{p} $ (Pa)', grid[:, 1], grid[:, 2])
            # fig.suptitle(r't $\cdot$ BPF = %.2f'%(ti*dt*BPF),fontsize=16,y=0.93)

            if savefig:
                fig.savefig(os.path.join(dataRestruction_dir_path, 't' + str(ti) + '_p.png'), dpi=300, bbox_inches='tight')
                plt.close()
        elif para == 'v':
            fig = comp_contour(data[ti, :] - data_mean, np.arange(pararange[0], pararange[1], pararange[2]),
                               r'$v-\bar{v} $ (m/s)', grid[:, 1], grid[:, 2])
            # fig.suptitle(r't $\cdot$ BPF = %.2f'%(ti*dt*BPF),fontsize=16,y=0.93)

            if savefig:
                fig.savefig(os.path.join(dataRestruction_dir_path, 't' + str(ti) + '_v.png'), dpi=300,
                            bbox_inches='tight')
                plt.close()
        elif para == 'w':
            fig = comp_contour(data[ti, :] - data_mean, np.arange(pararange[0], pararange[1], pararange[2]),
                               r'$w-\bar{w} $ (m/s)', grid[:, 1], grid[:, 2])
            # fig.suptitle(r't $\cdot$ BPF = %.2f'%(ti*dt*BPF),fontsize=16,y=0.93)

            if savefig:
                fig.savefig(os.path.join(dataRestruction_dir_path, 't' + str(ti) + '_w.png'), dpi=300,
                            bbox_inches='tight')
                plt.close()

    # plot animation of flow field
    t_start = 1500
    t_end = 1600
    t_delta = 1

    if para == 'p':
        if savefig:
            comp_contour_anim(t_start, t_end, t_delta, dt, 'ori_p_anim.gif',
                              data - data_mean, np.arange(pararange[0], pararange[1], pararange[2]),
                              r'$p-\bar{p} $ (Pa)', grid[:, 1], grid[:, 2],
                              colormap=cm.coolwarm)
    if para == 'v':
        if savefig:
            comp_contour_anim(t_start, t_end, t_delta, dt, 'ori_v_anim.gif',
                              data - data_mean, np.arange(pararange[0], pararange[1], pararange[2]),
                              r'$v-\bar{v} $ (m/s)', grid[:, 1], grid[:, 2],
                              colormap=cm.coolwarm)

    if para == 'w':
        if savefig:
            comp_contour_anim(t_start, t_end, t_delta, dt, 'ori_w_anim.gif',
                              data - data_mean, np.arange(pararange[0], pararange[1], pararange[2]),
                              r'$w-\bar{w} $ (m/s)', grid[:, 1], grid[:, 2],
                              colormap=cm.coolwarm)

    print('Plot original flow field finished')




    # -------------------------------------------------------------------------
    ### 4.1 Reconstructed flow field

    if MsRange == (0, 0) and FsRange == (0, 0):
        restrMs = (0, L.shape[1])
        restrFs = (0, f.shape[0])
    else:
        restrMs = (MsRange[0], MsRange[1])
        restrFs = (FsRange[0], FsRange[1])

    data_mean = np.mean(data, axis=0)  # time-averaged data
    # modes and frequencies used for reconstruction
    Ms = np.arange(restrMs[0], restrMs[1])
    fs = np.arange(restrFs[0], restrFs[1])

    # plot animation of reconstructed flow field

    data_rec = spod.reconstruct_time_method(data - data_mean, dt, f, P, Ms, fs, dataForRestru_dir_path, weight=weight,
                                            method='fast')

    if savefig:
        t_start = 1500
        t_end = 1600
        t_delta = 1
    if para == 'p':
        comp_contour_anim(t_start, t_end, t_delta, dt, ani_save_name='rec_p_anim%s.gif'%MSFSdir,
                          q=data_rec, qlevels=np.arange(pararange[0], pararange[1], pararange[2]),
                          qname=r'$p-\bar{p} $ (Pa)', x=grid[:, 1], y=grid[:, 2],
                          colormap=cm.coolwarm)
    elif para == 'v':
        comp_contour_anim(t_start, t_end, t_delta, dt, ani_save_name='rec_v_anim%s.gif'%MSFSdir,
                          q=data_rec, qlevels=np.arange(pararange[0], pararange[1], pararange[2]),
                          qname=r'$v-\bar{v} $ (m/s)', x=grid[:, 1], y=grid[:, 2],
                          colormap=cm.coolwarm)

    elif para == 'w':
        comp_contour_anim(t_start, t_end, t_delta, dt, ani_save_name='rec_w_anim%s.gif' % MSFSdir,
                          q=data_rec, qlevels=np.arange(pararange[0], pararange[1], pararange[2]),
                          qname=r'$w-\bar{w} $ (m/s)', x=grid[:, 1], y=grid[:, 2],
                          colormap=cm.coolwarm)


    print('Plot reconstructed flow field finished')

    # Sec. 2 end time
    end_sec4 = time.time()

    print('--------------------------------------')
    print('SPOD results postprocessed!')
    print('Time lapsed: %.2f s' % (end_sec4 - start_sec4))
    print('--------------------------------------')

    # Sec.4.3 getOneTime data

    print('-----------getOneTimeData------------')
    spod.getOneTimeData(getOneTimeList, os.path.join(dataForRestru_dir_path, 'reconstruct.h5'),dataRestruction_dir_path)
    print('--------finishGetOneTimeData---------')
    # -------------------------------------------------------------------------
    # -1. print memory usage
    # -------------------------------------------------------------------------
    process = psutil.Process(os.getpid())
    RAM_usage = np.around(process.memory_info().rss / 1024 ** 3, decimals=2)  # unit in GBs
    print('Total memory usage is: %.2f GB' % RAM_usage)




def main():
    getOneTimeList = [0,1,2,3]
    # p0 = Process(target=spodMain,args=('0.04_LES.h5','Slice0.04_v_LES',getOneTimeList,(0,1),(20,29),True,(1000,2),False,False,'v',(-10,11,1)))
    # p0.start()
    # p0.join()
    # p1 = Process(target=spodMain,args=('0.06_LES.h5','Slice0.06_v_LES',getOneTimeList,(0,1),(57,63),True,(1000,2),False,False,'v',(-20,22,2)))
    p2 = Process(target=spodMain,args=('0.08_DES.h5','Slice0.08_v_DES',getOneTimeList,(0,1),(42,45),True,(1000,2),False,False,'v',(-20,22,2)))
    # p3 = Process(target=spodMain,args=('0.06.h5','Slice0.06',getOneTimeList,(1,2),(19,26),True,(1000,2),False,False))
    # # p4 = Process(target=spodMain,args=('0.06.h5','Slice0.06',getOneTimeList,(1,2),(37,41),True,(1000,2),False,False))
    #
    #
    #
    #
    # p1.start()
    p2.start()
    # # p3.start()
    # # p4.start()
    #
    #
    # p1.join()
    p2.join()
    # # p3.join()
    # # p4.join()

if __name__ == '__main__':
    main()


