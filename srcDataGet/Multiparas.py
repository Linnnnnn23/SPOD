import tecplot as tp
from tecplot.exception import *
from tecplot.constant import *
import time
# Uncomment the following line to connect to a running instance of Tecplot 360:
tp.session.connect(port = 7600)
for i in [1000+j*5 for j in range(200)]:

    print(i)
    start_time =time.time()
    tp.macro.execute_command('$!FrameControl DeleteTop')
    tp.macro.execute_command("""$!ReadDataSet  '\"StandardSyntax\" \"1.0\" \"FEALoaderVersion\" \"461\" \"FILENAME_File\" \"E:\\Data\\LES_2048\\output_20221019_LES_500\\20221019_LES_500_001\\%s.trn\" \"AutoAssignStrandIDs\" \"Yes\"'
      DataSetReader = 'ANSYS CFX (FEA)'"""%i)
    tp.macro.execute_command('$!Redraw')
    tp.active_frame().plot().rgb_coloring.red_variable_index=3
    tp.active_frame().plot().rgb_coloring.green_variable_index=3
    tp.active_frame().plot().rgb_coloring.blue_variable_index=3
    tp.active_frame().plot().contour(0).variable_index=3
    tp.active_frame().plot().contour(1).variable_index=4
    tp.active_frame().plot().contour(2).variable_index=5
    tp.active_frame().plot().contour(3).variable_index=6
    tp.active_frame().plot().contour(4).variable_index=7
    tp.active_frame().plot().contour(5).variable_index=8
    tp.active_frame().plot().contour(6).variable_index=9
    tp.active_frame().plot().contour(7).variable_index=10
    tp.active_frame().plot(PlotType.Cartesian3D).show_slices=True
    tp.active_frame().plot().slices(0).extract(transient_mode=TransientOperationMode.AllSolutionTimes)
    tp.data.save_tecplot_ascii('E:\\Data\\LES_2048\\LES_spodDataGet\\001tmp\\MultiFiles\\0.04\\%s.dat'%i,
        zones=[7],
        variables=[3,4,7,22,23,24],
        include_text=False,
        precision=9,
        include_geom=False,
        include_data_share_linkage=True,
        use_point_format=True)
    end_time = time.time()
    print('一次需要%s,总共需要%s'%(end_time-start_time,(end_time-start_time)*(1200-i)))

