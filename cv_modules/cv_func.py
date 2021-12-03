import numpy as np
import cv2

def apply_filters(img, filters):
    """Returns the image with filters (gaussian, medianBlur, etc.).
    Args:
        img (np.array): Raw image.
        filters (list): List of filters which will be applied to the image.
            [["filter_name", *params], ["filter_name", *params]]
            Example: [["gaussianBlur", 5], ["bilateral", 15, 75], ["bitwise", "hsv", [[0,0,0], [255,255,255]], False]]
    Returns:
        img (np.array): Filtered image.
    """
    if not filters:
        return img
    for filter in filters:
        if filter[0] == "gaussianBlur":
            filter_area_size = filter[1]
            img = cv2.GaussianBlur(img, (filter_area_size, filter_area_size), 0)
        elif filter[0] == "blur":
            filter_area_size = filter[1]
            img = cv2.blur(img, (filter_area_size, filter_area_size))
        elif filter[0] == "medianBlur":
            filter_area_size = filter[1]
            img = cv2.medianBlur(img, filter_area_size)
        elif filter[0] == "bilateral":
            filter_area_size = filter[1]
            sigma = filter[2]
            img = cv2.bilateralFilter(img, filter_area_size, sigma, sigma)
        elif filter[0] == "bitwise":
            # white pixels in binary image keep their original color, and 
            # black pixels in binary image become black in the filtered image
            color_scale = filter[1]
            color_range = filter[2]
            lower, upper = color_range
            invert_binary = filter[3]

            img = binarize_image(img, lower, upper, color_scale, invert_binary)
    return img

def binarize_image(img, lower, upper, color_scale, invert_binary=False):
    if color_scale == "hsv":
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        binary_image = cv2.inRange(hsv, lower, upper)
    elif color_scale == "gray":
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        binary_image = cv2.inRange(gray, lower, upper)

    if invert_binary:
        # invertir binarizado
        binary_image = cv2.bitwise_not(binary_image)

    return binary_image

def find_contours(img, lower, upper, color_scale, invert_binary=False):
    """Returns found contours and the binary image.
    
    Args:
        img (np.array): Image where the contours are located.
        lower (np.array, int): Min color value.
            If the color scale is HSV: np.array([minH, minS, minV])
            If the color scale is gray: minPixelValue (as an int)
        upper (np.array, int): Max color value.
            If the color scale is HSV: np.array([maxH, maxS, maxV])
            If the color scale is gray: maxPixelValue (as an int)
        color_scale (str): Color scale to filter the image. 
            "hsv" for HSV, "gray" for gray scale.
        invert_binary (bool, optional): True if the binarization will be inverted,
            false if not. If True, the white pixels (255) will become black (0),
            and black pixels will become white.
            Defaults to False.
    Returns:
        contours (list): Contours found with cv2.findContours().
        binary_image (np.array): Binarized image (black 0 and white 255 pixels)
    """
    # retorna los contornos encontrados y la imagen binarizada
    binary_image = binarize_image(img, lower, upper, color_scale, invert_binary)

    # Encontrar contornos
    try:
        _, contours, _ = cv2.findContours(
            binary_image,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE
        )
    except:
         return None, None

    return contours, binary_image

def average_coordinates(coordinates1, coordinates2):
    x_average = int(round((coordinates1[0] + coordinates2[0])/2))
    y_average = int(round((coordinates1[1] + coordinates2[1])/2))
    return [x_average, y_average]

def get_contours_properties(contours):
    """Returns properties of each input contour.
    Args:
        contours (list): Contours found with cv2.findContours().
    Returns:
        contours_properties (dict): Stores the centers and bounding_rectangles
            of each contour.
    """
    contours_properties = {}

    contours_properties["centers"] = []
    contours_properties["bounding_rectangles"] = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        coordinates = [x,y,x+w,y+h]
        contours_properties["bounding_rectangles"].append(coordinates)

        center = average_coordinates(
            coordinates[:2], coordinates[2:]
        )
        contours_properties["centers"].append(center)

    return contours_properties
