# this program is being used to test my understanding of how qr code recognition in opencv works


import cv2
#from cv2 import *
#import numpy as np

#from matplotlib import pyplot as plt


def qr_code_match(image, qr_data):
    """This function determines whether or not a QR code, containing the given data qr_data. Is present within the image. If the desired QR code is present a boolean True is returned, other False is returned

    Args:
        image (image): An image that may contain a QR code
        qr_data (string): A string containing the expected QR data that this function checks against.

    Returns:
        Bool: Returns True is the image contains a QR code with provided data, False otherwise
    """
    # read passed image into a cv2 image type
    # img = cv2.imread(image)
    img = image
    # Creating an object of class QRCodeDetector and calling detectAndDecode on it

    QRCodeDetector = cv2.QRCodeDetector()
    decodedText, points, _ = QRCodeDetector.detectAndDecode(img)

    # check if a qr code was found within the image

    if points is not None:
        # A QR code was found within the image
        # check if the expected qr_data was found in a QR code

        if qr_data in decodedText:
            return True
        else:
            return False
    else:
        # No QR code was found within the image
        return False


def main():
    test_image = "not_scanned_small.png"
    expected_data = "Other Test Data"
    # loading image
    image = cv2.imread(test_image)

    print(
        f"The test image contains the expected QR Code:\n{qr_code_match(image, expected_data)}"
    )

    print("calling main")


if __name__ == "__main__":
    main()
