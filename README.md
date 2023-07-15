# Introduction

In this repo I provide an code example which extracts the contours from a 3D microscopy image of bone marrow. In reality, this an snippet from a larger code base which I've abbreviated for the purpose of brevity. 

The reason for extracting marrow contours is for the purpose of (1.) 3D spatial modelling of the marrow and (2.) visualisation. For modelling, it is better to have the contours as a 3D contour profile. For visualation - it is more convenient to load the contours into a geopandas dataframe. For example;

```python
# 3D contours
[[0, 1, 1], [0, 2, 3] ... [70, 700, 1200]]

# geopandas dataframe
>>> gdf.head()
   z_level                                           geometry
0        0  MULTIPOLYGON (((6929.000 822.000, 6928.000 823...
1        1  MULTIPOLYGON (((10768.000 800.000, 10766.000 8...
2        2  MULTIPOLYGON (((7163.000 1121.000, 7162.000 11...
3        3  MULTIPOLYGON (((10768.000 799.000, 10767.000 8...
4        4  MULTIPOLYGON (((875.000 1509.000, 874.000 1510...

```



