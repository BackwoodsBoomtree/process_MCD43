#-------------------------------------------------------------------------------
# Name:        LSWI from MCD43C4
# Purpose:     Calculate LSWI
#
#               
#
# Author:      Russell Doughty
#
# Created:     September 2nd 2019
#-------------------------------------------------------------------------------


import os
from tqdm import tqdm

# Define input variables
band_2_dir = r'G:\MCD43C4\daily\band2'
band_6_dir = r'G:\MCD43C4\daily\band6'

lswi_dir = r'G:\MCD43C4\daily_lswi'

nodata = -9999
gdal_calc_path = 'C:/Users/doug0002/anaconda3/Scripts/gdal_calc.py'

def viMCD43C4():
    
    print('Starting the run.')
    print('')
    
    # Create Raster Lists
    band_2_list = sorted([os.path.join(band_2_dir, l) for l in os.listdir(band_2_dir) if l.endswith('.tif')])
    band_6_list = sorted([os.path.join(band_6_dir, l) for l in os.listdir(band_6_dir) if l.endswith('.tif')])
    
    # gdal_calc needs the slash forward, so change the entire list
    rasterlist_new1 = []
    rasterlist_new2 = []

    for i in range(len(band_2_list)):
        raster = band_2_list[i].replace(os.sep, '/')
        rasterlist_new1.append(raster)
        raster = band_6_list[i].replace(os.sep, '/')
        rasterlist_new2.append(raster)

    band_2_list = rasterlist_new1
    band_6_list = rasterlist_new2

    lswi_expr = '"10000*((A-B)/(A+B))"' # LSWI
    
    for h in tqdm(range(len(band_2_list))):
        
        # Get only filename for a prefix
        raster_name = os.path.splitext(os.path.basename(band_2_list[h]))[0]
        lswi_name = raster_name[0:20] + '.LSWI.tif'
        
        output_lswi = os.path.join(lswi_dir, lswi_name)
        output_lswi = output_lswi.replace(os.sep, '/')

        gdal_calc_str = 'python {0} -A {1} -B {2} --outfile={3} --calc={4} --NoDataValue={5} --type=Int16 --overwrite --q'
        gdal_calc_nirv = gdal_calc_str.format(gdal_calc_path, band_2_list[h], band_6_list[h], output_lswi, lswi_expr, nodata) 
        os.system(gdal_calc_nirv)
        print('Done with %s.' % os.path.basename(output_lswi))
    
viMCD43C4()