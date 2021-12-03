"""Get contours properties.
Gets properties of the contours found on the input image.
Creates ROI by clustering contours."""
import cv2, numpy as np, codecs
from cv_modules import cv_func

reading_directory = "C:/create_roi_by_clustering_contours/"
writing_directory = "C:/create_roi_by_clustering_contours/"
assert writing_directory[0:3] != "D:/", "OpenCV can't write images to D Drive. Please, try a different writing path."

def read_file(path):
    with codecs.open(path, "r", encoding='utf8') as f:
        data = f.read()
        f.close()
    return data

def write_file(path, content):
    f = codecs.open(path, "w", encoding='utf8')
    f.write(str(content))
    f.close()


if __name__ == "__main__":
    data = read_file(f"{reading_directory}/data.txt")
    data = eval(data)

    image_path, filters, parameters = data
    image_path = image_path.replace("\\", "/")
    assert image_path[0:3] != "D:/", "OpenCV can't read images from D Drive. Please, copy your image to your C Drive."

    # parameters
    lower, upper, color_scale, invert_binary, closing_shape, kernel_size = parameters
    if closing_shape == "rectangle":
        closing_shape = cv2.MORPH_RECT
    elif closing_shape == "ellipse":
        closing_shape = cv2.MORPH_ELLIPSE

    image = cv2.imread(image_path)
    assert image is not None, f"Image does not exist. Path: {image_path}"
    filtered = cv_func.apply_filters(image, filters)

    # get contours centers
    contours, binary = cv_func.find_contours(
        filtered, np.array(lower), np.array(upper), color_scale, invert_binary,
    )

    contours_properties = cv_func.get_contours_properties(contours)

    # group close contours and create contours clusters
    binary_with_close_operation = cv2.morphologyEx(
        binary, cv2.MORPH_CLOSE,
        cv2.getStructuringElement(closing_shape, kernel_size),
    )

    # find contours of each cluster
    _, contours, _ = cv2.findContours(
        binary_with_close_operation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE,
    )

    regions_properties = cv_func.get_contours_properties(contours)

    # draw images
    image_centers = image.copy()
    for center in contours_properties["centers"]:
        # centers of contours
        image_centers[center[1]][center[0]] = [0, 0, 255]

    image_rectangles = image.copy()
    for rectangle in contours_properties["bounding_rectangles"]:
        # bounding rectangles of contours
        cv2.rectangle(
            image_rectangles, (rectangle[0], rectangle[1]), (rectangle[2], rectangle[3]), 
            (0,0,255), thickness=1,
        )

    image_regions = image.copy()
    for rectangle in regions_properties["bounding_rectangles"]:
        # bounding rectangles of clusters
        cv2.rectangle(
            image_regions, (rectangle[0], rectangle[1]), (rectangle[2], rectangle[3]), 
            (0,0,255), thickness=1,
        )

    cv2.imwrite(f"{writing_directory}/original.bmp", image)
    cv2.imwrite(f"{writing_directory}/filtered.bmp", filtered)
    cv2.imwrite(f"{writing_directory}/binary.bmp", binary)
    cv2.imwrite(f"{writing_directory}/contours_closed.bmp", binary_with_close_operation)
    cv2.imwrite(f"{writing_directory}/centers.bmp", image_centers)
    cv2.imwrite(f"{writing_directory}/rectangles.bmp", image_rectangles)
    cv2.imwrite(f"{writing_directory}/regions.bmp", image_regions)

    results_to_write = [
        contours_properties["centers"], 
        contours_properties["bounding_rectangles"],
        regions_properties["bounding_rectangles"],
    ]
    write_file(f"{writing_directory}/results.txt", results_to_write)