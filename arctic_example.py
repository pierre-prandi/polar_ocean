#!/usr/bin/env python
# coding: utf-8

"""
an example of how to read and plot the Arctic Ocean Sea level product

The product itself is available from AVISO (https://www.aviso.altimetry.fr/en/index.php?id=1708)

The paper describing the processing is available from  https://essd.copernicus.org/articles/13/5469/2021/

This has been tested with the following versions
    3.9.7 | packaged by conda-forge | (default, Sep  2 2021, 17:58:34) 
    [GCC 9.4.0]
    numpy version  1.20.3
    xarray version 0.19.0
    cartopy version  0.19.0.post1

"""

import sys
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# methods --------------------------------------------------------
def create_fig():
    """ create figure and axes """
    fig = plt.figure(figsize=(10,10))
    ax  = fig.add_axes([0,0,1,1], projection=ccrs.NorthPolarStereo())
    ax.add_feature(cfeature.LAND, color='#d9d9d9', zorder=100)
    ax.set_extent([-180,180,50,90], crs=ccrs.PlateCarree())
    return fig, ax

# ----------------------------------------------------------------

print(sys.version)
print('numpy version ', np.__version__)
print('xarray version', xr.__version__)
print('cartopy version ', cartopy.__version__)

# path to the netCDF file, this should be updated to match your directory structure
path_to_file = '/data/MSA_ETU/sar_seaice/livraison_v1.1/combined_arctic_sea_level_aviso.nc'

# open the dataset
dset = xr.open_dataset(path_to_file)

# average over time
avg = np.nanmean(dset.data_vars['sla'].values, axis=0)

# create the fig and axes
f, ax = create_fig()

# plotting method
ax.pcolormesh(
    dset.coords['longitude'].values,
    dset.coords['latitude'].values,
    avg,
    shading='flat',
    transform=ccrs.PlateCarree(),
    zorder=10,
    vmin=-0.3, 
    vmax=0.3,
    cmap='RdBu_r'
)

# save to file
f.savefig('avg_sla.png')