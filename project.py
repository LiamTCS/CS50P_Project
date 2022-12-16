"""Final project.py file"""
import qrcode
from fpdf import FPDF


# for identifying QR codes and decoding them
import cv2

# for converting pdf to images
from pdf2image import convert_from_path, convert_from_bytes

# import numpy as np
# import cv2 as cv
"""
potentially handy reference material
https://techtutorialsx.com/2019/12/08/python-opencv-detecting-and-decoding-a-qrcode/#:~:text=Python%20OpenCV%3A%20Detecting%20and%20Decoding%20a%20QRCode%201,of%20your%20choice.%20...%204%20References%20%5B1%5D%20https%3A%2F%2Fdocs.opencv.org%2F4.0.0%2Fde%2Fdc3%2Fclasscv_1_1QRCodeDetector.html%23a7290bd6a5d59b14a37979c3a14fbf394

https://www.geeksforgeeks.org/convert-pdf-to-image-using-python/


https://stackoverflow.com/questions/61832964/how-to-convert-pdf-into-image-readable-by-opencv-python
"""


class QR_pages:

    # this class contains data and functions relating to the production of both starter and seperator pages
    def __init__(self, name="default", quantity=1):

        # changeable class constants
        doc_title = "Scanned PDF Document Splitter"
        doc_author = "Liam Sproule"

        # QR code data
        def_qr_data = "Other Test Data"
        def_qr_filepath = "images/def_qr.png"

        user_qr_filepath = "images/user_qr.png"

        # making and saving the two qr codes, if user doesn't enter anything, then both are the same, but are both made anyway for ease of implementation

        # make the qr codes
        def_qr = qrcode.make(def_qr_data)
        user_qr = qrcode.make(name)

        # save the qr codes
        def_qr.save(def_qr_filepath)
        user_qr.save(user_qr_filepath)

        # initialise pdf
        self._pdf = FPDF()
        # different things will happen if user wants to use custom qr code or not

        # produce a pdf of n length with a centred default qr code
        self._pdf.add_page()
        # self._pdf.set_author(doc_author)
        # self._pdf.set_title(doc_title)
        # adding title
        self._pdf.set_font("helvetica", "B", 25)
        self._pdf.cell(
            w=0,
            h=60,
            txt="Scanned PDF Document Splitter",
            new_x="LMARGIN",
            new_y="NEXT",
            align="C",
        )

        # render shirt image
        self._pdf.image(def_qr_filepath, x=50, y=100)

    def save_pages(self, name):
        self._pdf.output(name)


def main():
    # # due to assignment requirements it will be best to write this program rather flat. ie not having function call sub functions too much.

    # user_inputs = user_interface()

    # user_pdf = load(user_inputs['pdf'])

    # # determine which page seperator QR code to use

    # QR_sep = identify_seperator(user_pdf)

    # # determine the location of the seperator pages within the pdf file
    # QR_pos = QR_location(user_pdf, QR_sep)

    # # Split the scanned document based on the QR code positions

    # test bit
    # qr_data = input("Enter QR data, blank for default: ")
    # pdf = QR_pages(qr_data, 5)
    # pdf.save_pages("Qr_output.pdf")



    # The actual program below
    
    # temp constant, will eventually check first page of pdf, then use that
    
    temp_user_file = "CS50P_Project/two_qr_types_test_doc.pdf"
    
    #TODO figuring out how to properly read pdfs
    
    user_file = input("Enter PDF filename:\n")
    print(f"User enterred: {user_file}\n This is a temporary debug action")
    open_pdf = open(temp_user_file)
    
    # convert pdf file to list of png images
    list_png = pdf_images(open_pdf)
    
    # check each image to see if it contains the QR code

    ...


# def identify_seperator():
#     # this function looks at the first page of the scan and identifies any QR codes on the page.
#     # if there are no QR codes, then return the default seperator QR code value
#     # if there are two QR codes, and one matches the default seperator QR code, then return the other QR code
#     ...


# def user_interface():
#     # This function handles the user interface, and returns the user options to main
#     ...


# def job_progress():
#     # this function displays the job progress in the terminal as a progress bar, and if possible gives information about the current task
#     ...


def QR_location(pdf, QR_sep):
    """
    This function is given the scanned document, and the QR code seperator to look for
    """
    ...



def pdf_images(file):
    """this function is given an opened pdf file, and returns a list, containing PNG images with a maximum width of 500 px

    Args:
        file (PDF Object): an Open PDF object, that has been read from disk somewhere else in the program

    Returns:
        list: Returns a list of PNG images with a maximum width of 500 px
    """

    return convert_from_bytes(file, fmt="png", size=(500, None))

    # This function is given the scanned document
    # it uses the pdf2image library, but is included as a seperate function because there may be some future additional features added to it


def QR_code_present(image, qr_data):
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


if __name__ == "__main__":
    main()
