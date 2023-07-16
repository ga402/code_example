# 'createBoundaries' script aims to extract the contours from
# a 3D binary image into two separate outputs; a geopandas
# dataframe and a 3D polygon.

import numpy as np
import tifffile as tf
import cv2 as cv
import geopandas as gpd
from utils.contourtools import *
from utils.func import *
from utils.img2df import img2df as img2df


def get_program_parameters():
    epilogue = """
    create a dataframe of pixel sizes and z levels and image names
    """

    parser = argparse.ArgumentParser(
        description="create the dataframe",
        epilog=epilogue,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("-f", "--file", help="image path, control.tif")
    parser.add_argument(
        "-o", "--output", help="output name: eg. control_boundaries.geojson"
    )
    parser.add_argument(
        "-s",
        "--block_reduce_size",
        type=int,
        default=3,
        help="amount to reduce slice amount, eg. 1",
    )
    args = parser.parse_args()
    return args.file, args.output, args.block_reduce_size


@spapply3D
def main(im, br_size):
    """Main function for creating contours  - parallel function.

    Args:
        im ([type]): binary (padded) image (3D)

    Returns:
        list[numpy.ndarray]: contours list (3D)
    """
    contours, hierarchy = findContours(im)
    hierarchy = hierarchy.squeeze()
    filtered_contours, filtered_hierarchy = filterContoursSize(contours, hierarchy)
    filtered_contours2 = [
        c for c, h in zip(filtered_contours, filtered_hierarchy) if h[3] == -1
    ]
    # adjustment for the downscaling..
    if br_size:
        filtered_contours2 = [c * br_size for c in filtered_contours2]

    try:
        contours_out = applySmoothContour(filtered_contours2, smooth_parameter=10)
    except:
        contours_out = filtered_contours2
    return contours_out


if __name__ == "__main__":
    logfile = createlog()
    logging.basicConfig(filename=logfile, level=logging.INFO)

    image_path, output_name, br_size = get_program_parameters()

    img = tf.imread(image_path)

    # pad the image
    img = padImage(img)

    contours = main(img, br_size)

    # use contours to create new image...
    # if had block reduction - this needs to be taken into account (+padding)
    if br_size:
        z, x, y = img.shape
        img = np.zeros((z, (x - 2) * br_size, (y - 2) * br_size))

    im = fillImage(img, contours)

    # load into the 'img2df' class
    idf = img2df(im)

    # create 3D polygon...
    final_geom = idf.getPolygon3D()

    # create the dataframe
    gdf = idf.getGDF()

    # save 3D polygon (using geopandas tools to save)
    gpd.GeoSeries([final_geom]).to_file(
        f"CountourBoundaries_{output_name}", driver="GeoJSON"
    )

    # save the gdf dataframe
    gdf.to_file(f"geodf_{output_name}", driver="GeoJSON")
