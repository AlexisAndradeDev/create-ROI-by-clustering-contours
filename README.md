# create-ROI-by-clustering-contours

# Description
In computer vision, it's common to create regions of interest (ROI) to inspect electronic components or for any other application. The process of creating ROIs in automatic optical inspection machines is usually slow and tedious for the user. The code of this repository helps automate the process of creating ROIs for AOI machines, especially for stencil inspection.

# Install

1. Create a folder "create_roi_by_clustering_contours" on C:/
2. Copy the content of this repository to C:/create_roi_by_clustering_contours/

# How to use
The file named "data.txt" contains the input data that the get_cs_pro.py script will read (more information in the «data.txt content» section).
Once you have your data.txt and your image, you can run get_cs_pro.py. It will create a file called "results.txt", which contains the centers and bounding rectangles of each contour, and also the bounding rectangle of each cluster (more information in the «results.txt content» section).
Also, images of the process will be written:

original.bmp : Imagen sin modificar.
filtered.bmp : Imagen con filtros secundarios.
binary.bmp : Imagen binarizada.
contours_closed : Imagen con los contornos agrupados.
centers.bmp : Imagen con el centro de cada contorno individual dibujado.
rectangles.bmp : Imagen con un rectángulo dibujado alrededor de cada contorno individual.
regions.bmp : Imagen con un rectángulo dibujado alrededor de cada grupo de contornos.

You can change the reading_directory (which determines the location of the data.txt) and the writing_directory (where the images and the results.txt file will be written) inside of get_cs_pro.py.


# data.txt content
data.txt is written using Python syntax:

[
"image_path",

[filters],

[
    min_color, max_color, color_scale, invert_binary, closing_shape, kernel_size
],
    
]

image_path: String with the path of the image.

filters: List of filters which will be applied to the image.
    [["filter_name", *params], ["filter_name", *params], ...]
    Example: [["gaussianBlur", 3], ["medianBlur", 7]]
    Documented in cv_func.apply_filters

min_color, max_color: Pixels within the range will become  white; pixels outside the range will become black.
    Example:
        Using "hsv" color scale:
            [50,20,30], [255, 100, 150]
            min_color = [50,20,30]
            max_color = [255, 100, 150]
        Using "gray" color scale:
            80, 190
            min_color = 80
            max_color = 190

color_scale: "hsv", "gray".
    Determines the color scale with which the image will be binarized.

invert_binary: True/False
    True if the binarization will be inverted, false if not. 
    If True, white pixels (255) will become black (0), and black pixels will become white.

closing_shape: "ellipse", "rectangle".
    Determines the shape of the line that will be drawn to connect contours (this can be seen in the output image called "contours_closed.bmp").

kernel_size: (x_distance, y_distance)
  Determines the distance that must exist between two contours to form a cluster. 
    Example: (12, 14)
    
# results.txt content
[
[center_of_each_contour],
[bounding_rectangle_of_each_contour],
[bounding_rectangle_of_each_cluster]
]

center_of_each_contour: List that contains the [x,y] of centers (of the contours).
    [[x,y], [x,y], [x,y], ...]

bounding_rectangle_of_each_contour: List that contains the [x1,y1,x2,y2] of bounding rectangles (of the contours).
    [[x1,y1,x2,y2], [x1,y1,x2,y2], [x1,y1,x2,y2], ...]

bounding_rectangle_of_each_cluster: List that contains the [x1,y1,x2,y2] of each bounding rectangle (of the clusters).
    [[x1,y1,x2,y2], [x1,y1,x2,y2], [x1,y1,x2,y2], ...]
