# https://rabernat.github.io/research_computing_2018/maps-with-cartopy.html
# https://stackoverflow.com/questions/45622334/pyplot-contourf-how-can-i-make-the-colors-in-the-chart-continuous
# https://matplotlib.org/stable/gallery/frontpage/contour_frontpage.html#sphx-glr-gallery-frontpage-contour-frontpage-py
# https://scitools.org.uk/cartopy/docs/v0.13/matplotlib/advanced_plotting.html
# https://rabernat.github.io/research_computing_2018/maps-with-cartopy.html


import rasterio
import numpy as np
import matplotlib.pyplot as plt
from getchinamap.getchinamap import DownloadChmap
import rasterio.mask
import cartopy.crs as ccrs
import matplotlib as mpl
import logging
import datetime


def main():
    logging.basicConfig(level=logging.DEBUG,
                        # 设置输出格式，年月日分秒毫秒，行数，等级名，打印的信息
                        format="%(asctime)s - %(levelname)s: %(message)s")
    logging.info(msg="下载数据")
    dl_engine = DownloadChmap()

    path1 = "数据集/dem1km_china/1KM_DEM_albers.tif"
    path2 = "数据集/ChinaDEM1km_WGS84.tif"
    path3 = "数据集/Global_DEM/World_e-Atlas-UCSD_SRTM30-plus_v8.tif"
    dem_raw_data = rasterio.open(path3)
    china_boundary_gdf = dl_engine.download_country(target='边界')
    china_boundary_gpd_sub = dl_engine.download_country(target='省')
    # china_boundary_gdf = dl_engine.download_province(province_name='浙江省',target='边界')

    # china_boundary_gdf
    logging.info("对数据切片")
    out_image, out_transform = rasterio.mask.mask(dem_raw_data, china_boundary_gdf['geometry'], crop=True, nodata=-999999)
    out_meta = dem_raw_data.meta
    out_meta.update({"driver": "GTiff",
                     "height": out_image.shape[1],
                     "width": out_image.shape[2],
                     "transform": out_transform})

    clean_data = out_image.copy().astype('float')
    clean_data = clean_data[0, :, :]
    clean_data[clean_data == out_meta['nodata']] = np.nan
    clean_data[clean_data == -999999] = np.nan

    # clean_data

    longitude = np.array(
        [getattr(out_transform, 'c') + i * getattr(out_transform, 'a') for i in range(clean_data.shape[1])])
    latitude = np.array(
        [getattr(out_transform, 'f') + i * getattr(out_transform, 'e') for i in range(clean_data.shape[0])])  # [::-1]

    colors = ["#33A02C", "#B2DF8A", "#FDBF6F", "#1F78B4", "#999999", "#E31A1C", "#E6E6E6", "#A6CEE3"]
    center_china_point = china_boundary_gdf.centroid[0]

    logging.info('设置投影')
    # 新的兰伯特投影
    new_crs = ccrs.LambertConformal(central_longitude=center_china_point.x,
                                    central_latitude=center_china_point.y)
    # new_crs = ccrs.Orthographic(central_longitude=center_china_point.x,
    #                             central_latitude=center_china_point.y)
    myccrs = ccrs.PlateCarree()
    new_crs = myccrs
    logging.info('开始画图')
    fig, ax = plt.subplots(figsize=(15, 15), dpi=300, subplot_kw={'projection': new_crs})
    ax.gridlines(draw_labels=True,
                 linewidth=2, color='gray', alpha=0.5, linestyle='--')

    # logging.info('添加contourf')
    # ax_im_bar = ax.contourf(longitude, latitude, clean_data,  # [::-1,:]
    #                         np.arange(np.nanmin(clean_data), np.nanmax(clean_data), 100.0),
    #                         transform=myccrs,
    #                         cmap=mpl.colors.LinearSegmentedColormap.from_list("mypalette", colors, N=1000),
    #                         extend='both', origin='upper')
    logging.info('添加im')
    mat_extent = [getattr(out_transform, 'c'),
                  getattr(out_transform, 'c') + clean_data.shape[1] * getattr(out_transform, 'a'),
                  getattr(out_transform, 'f') + clean_data.shape[0] * getattr(out_transform, 'e'),
                  getattr(out_transform, 'f')]
    ax_im_bar = ax.imshow(clean_data, origin='upper', extent=mat_extent, transform=myccrs,
                          cmap=mpl.colors.LinearSegmentedColormap.from_list("mypalette", colors, N=1000))
    fig.colorbar(ax_im_bar, orientation='vertical')
    logging.info('添加boundary')
    china_boundary_gpd_sub.boundary.plot(ax=ax, edgecolor='black', linewidth=1)
    logging.info('保存')
    fig.savefig(f"test1226_china_{datetime.datetime.now().strftime('%Y-%m-%d %X')}.png")
    logging.info('展示图片')
    plt.show()


if __name__ == '__main__':
    main()
