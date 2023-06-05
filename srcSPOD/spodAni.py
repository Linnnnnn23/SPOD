import tecplot as tp
from tecplot.exception import *
from tecplot.constant import *
import time

# Uncomment the following line to connect to a running instance of Tecplot 360:
tp.session.connect(port=7602)

def restrutionForFig(MsRange,FsRange):
    if MsRange == (0, 0) and FsRange == (0, 0):
        MSFSdir = 'MSAll_FSAll'
        getOneTimeList = [1500, 1600, 1700, 1800]
    else:
        MSFSdir = 'MS%s-%s_FS%s-%s' % (MsRange[0], MsRange[1], FsRange[0], FsRange[1])
        T = 1 / FsRange[0] / 195
        dataNumInOneT = int(T * 200000)
        # getOneTimeList = [1500 + int(dataNumInOneT / 4) * i for i in range(10)]
        # getOneTimeList = [1500]
        #
        getOneTimeList = [1500 +  i*2 for i in range(150)]
    for i in getOneTimeList:
        print(i)
        start_time = time.time()
        tp.macro.execute_command('$!FrameControl DeleteTop')
        tp.macro.execute_command('''$!Pick SetMouseMode
          MouseMode = Select''')
        tp.macro.execute_command("""$!ReadDataSet  '\"E:\\Data\\LES_2048\\LES_spodDataGet\\007restructionData\\TipCube\\%s\\restru_t%s.dat\" '
          ReadDataOption = New
          ResetStyle = No
          VarLoadMode = ByName
          AssignStrandIDs = Yes
          VarNameList = '\"X\" \"Y\" \"Z\" \"Pressure\"'"""%(MSFSdir,i))
        tp.active_frame().plot().contour(0).variable_index=3
        tp.active_frame().plot().contour(0).color_cutoff.include_max=True
        tp.active_frame().plot().contour(0).levels.reset_levels([-3000, -2647.06, -2294.12, -1941.18, -1588.24, -1235.29, -882.353, -529.412, -176.471, 176.471, 529.412, 882.353, 1235.29, 1588.24, 1941.18, 2294.12, 2647.06, 3000])
        tp.active_frame().plot().rgb_coloring.red_variable_index=3
        tp.active_frame().plot().rgb_coloring.green_variable_index=3
        tp.active_frame().plot().rgb_coloring.blue_variable_index=3
        tp.active_frame().plot().contour(1).variable_index=3
        tp.active_frame().plot().contour(2).variable_index=3
        tp.active_frame().plot().contour(3).variable_index=3
        tp.active_frame().plot().contour(4).variable_index=3
        tp.active_frame().plot().contour(5).variable_index=3
        tp.active_frame().plot().contour(6).variable_index=3
        tp.active_frame().plot().contour(7).variable_index=3
        tp.active_frame().plot(PlotType.Cartesian3D).show_isosurfaces=True
        tp.active_frame().plot().isosurface(0).isosurface_values[0]=-100
        tp.macro.execute_command('$!Redraw')
        tp.active_frame().plot().view.psi=83.1136
        tp.active_frame().plot().view.theta=-29.2191
        tp.active_frame().plot().view.alpha=-2.51415
        tp.active_frame().plot().view.position=(0.539971,
            tp.active_frame().plot().view.position[1],
            tp.active_frame().plot().view.position[2])
        tp.active_frame().plot().view.position=(tp.active_frame().plot().view.position[0],
            -0.806377,
            tp.active_frame().plot().view.position[2])
        tp.active_frame().plot().view.position=(tp.active_frame().plot().view.position[0],
            tp.active_frame().plot().view.position[1],
            0.1338)
        tp.active_frame().plot().view.width=0.128726
        tp.active_frame().plot().view.psi=59.0662
        tp.active_frame().plot().view.theta=-44.1883
        tp.active_frame().plot().view.alpha=11.9795
        tp.active_frame().plot().view.position=(0.647456,
            tp.active_frame().plot().view.position[1],
            tp.active_frame().plot().view.position[2])
        tp.active_frame().plot().view.position=(tp.active_frame().plot().view.position[0],
            -0.567766,
            tp.active_frame().plot().view.position[2])
        tp.active_frame().plot().view.position=(tp.active_frame().plot().view.position[0],
            tp.active_frame().plot().view.position[1],
            0.507892)
        tp.active_frame().plot().view.width=0.128726
        tp.active_frame().plot().view.psi=78.1395
        tp.active_frame().plot().view.theta=-109.297
        tp.active_frame().plot().view.alpha=7.05291
        tp.active_frame().plot().view.position=(0.95667,
            tp.active_frame().plot().view.position[1],
            tp.active_frame().plot().view.position[2])
        tp.active_frame().plot().view.position=(tp.active_frame().plot().view.position[0],
            0.322959,
            tp.active_frame().plot().view.position[2])
        tp.active_frame().plot().view.position=(tp.active_frame().plot().view.position[0],
            tp.active_frame().plot().view.position[1],
            0.215073)
        tp.active_frame().plot().view.width=0.128726
        tp.active_frame().plot().view.psi=74.7109
        tp.active_frame().plot().view.theta=-162.16
        tp.active_frame().plot().view.alpha=3.02417
        tp.active_frame().plot().view.position=(0.360481,
            tp.active_frame().plot().view.position[1],
            tp.active_frame().plot().view.position[2])
        tp.active_frame().plot().view.position=(tp.active_frame().plot().view.position[0],
            0.887505,
            tp.active_frame().plot().view.position[2])
        tp.active_frame().plot().view.position=(tp.active_frame().plot().view.position[0],
            tp.active_frame().plot().view.position[1],
            0.270273)
        tp.active_frame().plot().view.width=0.128726
        tp.active_frame().plot().view.psi=67.3034
        tp.active_frame().plot().view.theta=-154.746
        tp.active_frame().plot().view.alpha=-0.429985
        tp.active_frame().plot().view.position=(0.453564,
            tp.active_frame().plot().view.position[1],
            tp.active_frame().plot().view.position[2])
        tp.active_frame().plot().view.position=(tp.active_frame().plot().view.position[0],
            0.807935,
            tp.active_frame().plot().view.position[2])
        tp.active_frame().plot().view.position=(tp.active_frame().plot().view.position[0],
            tp.active_frame().plot().view.position[1],
            0.386219)
        tp.active_frame().plot().view.width=0.128726
        tp.macro.execute_command('''$!Pick SetMouseMode
          MouseMode = Select''')
        tp.macro.execute_command('''$!Pick AddAtPosition
          X = 8.80508474576
          Y = 2.68220338983
          ConsiderStyle = Yes''')
        tp.macro.execute_command('''$!Pick AddAtPosition
          X = 8.80508474576
          Y = 2.68220338983
          CollectingObjectsMode = HomogeneousAdd
          ConsiderStyle = Yes''')
        tp.macro.execute_command('$!Pick Clear')
        tp.macro.execute_command('''$!Pick AddAtPosition
          X = 8.60169491525
          Y = 1.10593220339
          CollectingObjectsMode = HomogeneousAdd
          ConsiderStyle = Yes''')
        tp.macro.execute_command('$!Pick Clear')
        tp.macro.execute_command('''$!Pick AddAtPosition
          X = 9.99152542373
          Y = 2.42796610169
          ConsiderStyle = Yes''')
        tp.macro.execute_command('''$!Pick AddAtPosition
          X = 10
          Y = 4.6313559322
          ConsiderStyle = Yes''')
        tp.macro.execute_command('''$!FrameControl ActivateByNumber
          Frame = 1''')
        tp.macro.execute_command('''$!Pick Shift
          X = 2.50847457627
          Y = 0
          PickSubposition = Right''')
        tp.macro.execute_command('''$!Pick Shift
          X = -2.45762711864
          Y = 0
          PickSubposition = Left''')
        tp.macro.execute_command('$!Redraw')
        tp.active_frame().plot().view.position=(0.453564,
            tp.active_frame().plot().view.position[1],
            tp.active_frame().plot().view.position[2])
        tp.active_frame().plot().view.position=(tp.active_frame().plot().view.position[0],
            0.807935,
            tp.active_frame().plot().view.position[2])
        tp.active_frame().plot().view.position=(tp.active_frame().plot().view.position[0],
            tp.active_frame().plot().view.position[1],
            0.386219)
        tp.active_frame().plot().view.width=0.187816
        tp.active_frame().plot().axes.x_axis.show=True
        tp.active_frame().plot().axes.y_axis.show=True
        tp.active_frame().plot().axes.z_axis.show=True
        tp.macro.execute_command('$!Redraw')
        tp.active_frame().plot().view.position=(0.453564,
            tp.active_frame().plot().view.position[1],
            tp.active_frame().plot().view.position[2])
        tp.active_frame().plot().view.position=(tp.active_frame().plot().view.position[0],
            0.807935,
            tp.active_frame().plot().view.position[2])
        tp.active_frame().plot().view.position=(tp.active_frame().plot().view.position[0],
            tp.active_frame().plot().view.position[1],
            0.386219)
        tp.active_frame().plot().view.width=0.209264
        tp.active_frame().plot().axes.z_axis.title.title_mode=AxisTitleMode.UseText
        tp.active_frame().plot().axes.z_axis.title.text='Spanwise'
        tp.active_frame().plot().axes.z_axis.title.font.typeface='Times'
        tp.active_frame().plot().axes.z_axis.title.font.size=18
        tp.active_frame().plot().axes.y_axis.title.title_mode=AxisTitleMode.UseText
        tp.active_frame().plot().axes.y_axis.title.text='Pitchwise'
        tp.active_frame().plot().axes.y_axis.title.font.typeface='Times'
        tp.active_frame().plot().axes.y_axis.title.font.size=18
        tp.active_frame().plot().axes.x_axis.title.font.typeface='Times'
        tp.active_frame().plot().axes.x_axis.title.title_mode=AxisTitleMode.UseText
        tp.active_frame().plot().axes.x_axis.title.text='Streamwise'
        tp.active_frame().plot().axes.x_axis.title.font.size = 18
        tp.macro.execute_command('$!Redraw')
        tp.active_frame().plot().axes.x_axis.title.offset=30
        tp.active_frame().plot().axes.y_axis.title.offset=30
        tp.active_frame().plot().axes.z_axis.title.offset=30
        tp.active_frame().plot().axes.z_axis.tick_labels.font.typeface='Times'
        tp.macro.execute_command('$!Redraw')
        tp.active_frame().plot().axes.z_axis.tick_labels.font.bold=True
        tp.active_frame().plot().axes.y_axis.tick_labels.font.typeface='Times'
        tp.active_frame().plot().axes.x_axis.tick_labels.font.typeface='Times'
        tp.macro.execute_command('$!Redraw')
        tp.active_frame().plot().view.position=(0.453564,
            tp.active_frame().plot().view.position[1],
            tp.active_frame().plot().view.position[2])
        tp.active_frame().plot().view.position=(tp.active_frame().plot().view.position[0],
            0.807935,
            tp.active_frame().plot().view.position[2])
        tp.active_frame().plot().view.position=(tp.active_frame().plot().view.position[0],
            tp.active_frame().plot().view.position[1],
            0.386219)
        tp.active_frame().plot().view.width=0.224419
        tp.active_frame().plot().axes.x_axis.tick_labels.font.size=12
        tp.active_frame().plot().axes.x_axis.tick_labels.font.bold=True
        tp.active_frame().plot().axes.y_axis.tick_labels.font.size=12
        tp.active_frame().plot().axes.y_axis.tick_labels.font.bold=True
        tp.active_frame().plot().axes.z_axis.tick_labels.font.size = 12
        tp.active_frame().plot().axes.z_axis.tick_labels.font.bold = True

        tp.macro.execute_command('$!Redraw')
        tp.export.save_tiff('E:\\Data\\LES_2048\\LES_spodDataGet\\007restructionData\\TipCube\\%s\\-100_%s.tiff'%(MSFSdir,i),
            width=4000,
            region=ExportRegion.AllFrames,
            supersample=1,
            convert_to_256_colors=False,
            gray_scale_depth=None,
            byte_order=TIFFByteOrder.Intel)
        tp.save_layout('E:\\Data\\LES_2048\\LES_spodDataGet\\007restructionData\\TipCube\\%s\\%s_-100.lay'%(MSFSdir,i),
            use_relative_paths=True)
        endtime = time.time()
        eachtime = endtime -start_time
        print('一次用时%s,剩余时间%s'%(eachtime,eachtime*(getOneTimeList[-1]-i)))
        # End Macro.

def main():
    restrutionForFig((0,1), (4,5))


if __name__ == '__main__':
    main()