# type: ignore
import numpy as np
import pandas as pd
import json
import os
import glob
import tifffile as tf
from shapely.geometry import Polygon, MultiPolygon
import geopandas as gpd
import matplotlib.pyplot as plt
import cv2 as cv
from func import *
from baseImage import *




class img2df(baseImage):
    def __init__(self, image):
        super().__init__(image)
        self.final_geom = None
        self.gdf = None

    @staticmethod
    def _extractCont(im):
        """extract the contours from the 2D layer

        Args:
            im (binary image): binary image 

        Returns:
            contours
            heirachy of the contours
        """
        cont, heir = cv.findContours(im, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        return cont, heir

    @staticmethod
    def fPolygon(cont):
        cont = cont.squeeze()
        return Polygon(cont)

    def _convertToPolygons(self, contours):
        polygons = map(self.fPolygon, contours)  # converting to Polygons
        return MultiPolygon(polygons)

    def _contours2Polygons(self, im):
        c, h = self._extractCont(im)
        return self._convertToPolygons(c)

    def contours2Polygons(self, image):
        assert len(image.shape) == 3, "wrong dimensions"
        MP = [self._contours2Polygons(image[i, ...]) for i in range(image.shape[0])]
        return MP

    def generateContoursDataFrame(self):
        """convert the series of 2D contours into a dataframe of geom forms 
        """
        MP_list = self.contours2Polygons(self.image)
        self.gdf = gpd.GeoDataFrame({"z_level": self.z_levels, "geometry": MP_list})
        self.gdf.set_geometry("geometry")
        print(self.gdf.head(5))

    def getGDF(self):
        if self.gdf is None:
            self.generateContoursDataFrame()
        return self.gdf.set_geometry("geometry")

    def generateCompleteMultiPolygon(self):
        """Create a single multiple 3D polygon"""
        final_geom = []
        for g, z in zip(self.gdf["geometry"], self.gdf["z_level"]):
            for polygon in g:
                p = Polygon([t + (float(z),) for t in list(polygon.exterior.coords)])
                final_geom.append(p)
            # final_geom.append(MultiPolygon(empty_p))
        final_geom = MultiPolygon(final_geom)
        res = np.where(final_geom.has_z, "has z axis", " has no z axis")
        res = str(res)
        print(f"{final_geom.geom_type} generated {res}")
        self.final_geom = final_geom

    def getPolygon3D(self):
        # if any(self.gdf == None):
        try:
            self.generateContoursDataFrame()
        except:
            print("generateContoursDataFrame failed")

        # if self.final_geom == None:
        try:
            self.generateCompleteMultiPolygon()
        except:
            print("generateCompleteMultiPolygon failed")

        return self.final_geom





