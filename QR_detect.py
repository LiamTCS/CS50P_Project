# This file contains the functions that detect the presence of and positions of the seperator QR pages
import cv2
import fitz
import numpy as np








def seperator_positions(file: str, qr_data:="seperator page"):
    """this function is given a file location of a pdf file, and returns a list containing the converted image data. The image data is of type "numpy.ndarray"

    Args:
        file (string): The location of the pdf file to be converted to a list of images

    Returns:
        list: Returns a list containing image data of type "numpy.ndarray"
    """

    # Using pdf2image required external dependencies that I could not use
    # Using the PyMuPDF library instead
    file_path = file
    dpi = 300
    zoom = dpi / 72
    magnify = fitz.Matrix(zoom, zoom)  # resizes image, to be more consistent

    # open document
    doc = fitz.open(file_path)  # type: ignore

    # adding code to handle progress bars
    print("Converting pdf to images")

    # initialising a list to contain the generated images
    images = []

    # loop through each page, generating an image for each
    for page in doc:
        picture = page.get_pixmap(matrix=magnify)  # rendering page to an image

        # converting the pixmap to an image in BGR format (what openCV wants)
        np_array = np.frombuffer(picture.samples, dtype=np.uint8)
        np_array = np_array.reshape(picture.h, picture.w, picture.n)

        # converting RGB to BGR format
        openCV_format = cv2.cvtColor(np_array, cv2.COLOR_RGB2BGR)

        # resizing the image, so later cv2 qr code recognition runs faster

        # determine scaling factor to resize image by
        # desired final image width
        desired_width = 600

        # producing dsize tuple, to find new dimensions
        current_width = openCV_format.shape[1]
        scaling_factor = current_width / desired_width
        dsize = (600, int(openCV_format.shape[0] / scaling_factor))

        # resize the image, and append it to the images list
        resized = cv2.resize(openCV_format, dsize,
                             interpolation=cv2.INTER_AREA)

        # appending image data to list
        images.append(resized)

        print(f"{page} converted to image, added to list")

    # After producing the images, check each one for the presence of the  QR seperator page




    # Return list of generated images
    return images




def QR_data(image_data) -> tuple:
    """This function is passed an image, and if a QR code is found, returns the data contained within the qr code.

    Args:
        image_data (numpy.ndarray)): An numpy.ndarray containing image data

    Returns:
        bool    : True/False on whether the image contained a QR code
        string  : decoded text data, or an empty string
    """

    QRCodeDetector = cv2.QRCodeDetector()
    decodedText, points, _ = QRCodeDetector.detectAndDecode(image_data)

    if points is not None:
        # A QR code was found within the image
        return True, decodedText
    else:
        return False, ""
    
    
    
    
def QR_match(image, qr_data: str) -> bool:
    """This function determines whether or not a QR code, containing the given data qr_data. Is present within the image. If the desired QR code is present a boolean True is returned, other False is returned

    Args:
        image (image): An image that may contain a QR code
        qr_data (string): A string containing the expected QR data that this function checks against.

    Returns:
        Bool: Returns True is the image contains a QR code with provided data, False otherwise
    """

    # Creating an object of class QRCodeDetector and calling detectAndDecode on it
    QRCodeDetector = cv2.QRCodeDetector()
    decodedText, points, _ = QRCodeDetector.detectAndDecode(image)

    # check if a qr code was found within the image
    if points is not None:
        # A QR code was found within the image

        # check if the expected qr_data was found in a QR code
        # This is done to ensure that not every QR code acts as a document splitter, only the desired one
        if qr_data in decodedText:
            return True
        else:
            return False
    else:
        # No QR code was found within the image
        return False