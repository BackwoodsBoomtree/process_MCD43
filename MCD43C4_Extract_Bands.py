#-------------------------------------------------------------------------------
# Name:        Extract bands from HDF
# Purpose:     Extract bands from MCD43C4
#
#               
#
# Author:      Russell Doughty
#
# Created:     September 27 2019
#-------------------------------------------------------------------------------


import os
import gdal
from tqdm import tqdm

# Define input variables
input_dir = r'G:\MCD43C4\2016\original'
band1_dir = r'G:\MCD43C4\2016\daily\band1'
band2_dir = r'G:\MCD43C4\2016\daily\band2'
band3_dir = r'G:\MCD43C4\2016\daily\band3'
band6_dir = r'G:\MCD43C4\2016\daily\band6'

sub_data = [0,1,2,5]


nodata = -9999

def viMCD43C4():
    
    print('Starting the run.')
    print('Input directory is %s.' % input_dir)
    
    # Create HDF List   
    hdfList = sorted([os.path.join(input_dir, l) for l in os.listdir(input_dir) if l.endswith('.hdf')])
    
    for h in tqdm(range(len(hdfList))):
        
        # Get only date from original hdf filename
        hdf_name = os.path.splitext(os.path.basename(hdfList[h]))[0] # gets filename without extension
        hdf_name = hdf_name[0:21] # Gets the date from the filename

        # Get subdataset info for each HDF
        dataset = gdal.Open(hdfList[h], gdal.GA_ReadOnly)
        subdatasets = dataset.GetSubDatasets()
            
        for i in range(len(sub_data)):
    
            if sub_data[i] == 0:
                sub_desc = 'BAND_1'
                output_path = band1_dir
            elif sub_data[i] == 1:
                sub_desc = 'BAND_2'
                output_path = band2_dir
            elif sub_data[i] == 2:
                sub_desc = 'BAND_3'
                output_path = band3_dir
            elif sub_data[i] == 3:
                sub_desc = 'BAND_6'
                output_path = band6_dir

            # Set output filename and directory
            output_file = hdf_name + sub_desc + '.tif'
            output_total = os.path.join(output_path, output_file)

            # Output to tiff with gdal
            command = 'gdalwarp -dstnodata %s -t_srs EPSG:4326 -of GTiff -overwrite -q %s %s' % (nodata,subdatasets[sub_data[i]][0],output_total)
            os.system(command)

    print ('Run FINISHED.')    
    
   
viMCD43C4()