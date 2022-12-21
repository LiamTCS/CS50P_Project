"""Final project.py file"""
import qrcode
from fpdf import FPDF
import os

# for regex
import re


# for identifying QR codes and decoding them
import cv2

# for converting pdf to images
#'from pdf2image import convert_from_path, convert_from_bytes

# fitz is what PyMuPDF is called, for backwards compatibility reasons
import fitz
import numpy as np

from PIL import Image
import PIL


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
    # add handling to allow argv's to provide user input

    # getting user input
    pdf_path, output_path = user_input()

    # producing a list containing images of each pdf page
    doc_images = pdf_2_image_list(pdf_path)

    # determine if the seperator qr code is present in each image from the list
    sep_pos = QR_seperator_present(doc_images)

    # determine where each sub document starts and ends
    sub_doc_tuples = sub_doc_pos(sep_pos)

    # returns a bool True or False, for debug purposes
    split_success, _ = pdf_split(pdf_path, output_path, sub_doc_tuples)


def user_input():
    test_pdf = "/home/liams/CS50P_Project/TEST PDF Scans/test scan to test.pdf"
    test_output = "Output/Trial_output"

    pdf_file = input("Enter PDF Filename:\n")

    output_filename = input("Desired output filename:\n")

    # for testing purposes
    pdf_file = test_pdf
    output_filename = test_output

    # # ensures that there will be an output filename
    # if output_filename == "":
    #     output_filename = "pdf_split"

    while True:
        pdf_file = input("Enter PDF Filename:\n")
        output_filename = input("Desired output filename:\n")
        
        # for testing
        # TODO remove
        pdf_file = test_pdf
        output_filename = test_output

        valid, msg = input_validation(pdf_file, output_filename)

        if valid:
            break
        else:
            print(f"User inputs are not valid, for the following reason(s):\n{msg}\nPlease Try Again")
    return pdf_file, output_filename


def input_validation(pdf, output):
    """This function validates the user inputs. By carrying out the following checks:
    1. Checking that the input filename ends with ".pdf"
    2. Checking for the existance of the input file
    3. Checking that the output filename ends with ".pdf"
    4. checking that the desired output file does not exist

    Args:
        pdf (string): filename or filepath
        output (string): filename or filepath

    Returns:
        Bool: Is input valid
        String: A string containing information about which validity checks failed. Might be useful to display the message to the user, so they know where the issue is.

    """

    # this function validates the input and output files that are passed to the user_input function
    # returns TRUE or FALSE, depending on validity

    # msg string is used to pass back the failure condition to the calling function.
    msg = ""
    valid = True

    # checking input file

    # Does the input File end in ".pdf"?
    if not pdf.endswith(".pdf"):
        # if input file doesn't end in .pdf, then not valid
        valid = False
        msg = msg + ' Input File Does not end with ".pdf".'

    # Checking whether the output file already exists, if so inform user
    if not os.path.isFile(pdf):
        # if input file does not exist
        msg = msg + " Input file does not exist."
        valid = False

    # Checking output file

    # checking to ensure the output file does not already exist
    if os.path.isFile(output):
        # File exists, not a valid input
        valid = False
        msg = msg + " Output file already exists"

    # checking if the output file ends with ".pdf"
    if not output.endswith(".pdf"):
        # if input file doesn't end in .pdf, then not valid
        valid = False
        msg = msg + ' Output File Does not end with ".pdf".'

    # A msg string with leading whitespace can be produced, this strips it
    msg.strip()

    return valid, msg


def pdf_2_image_list(file):
    """this function is given a filepath string of a pdf, and returns a list containing the converted images

    Args:
        file (string): The location of the pdf file to be converted to a list of images

    Returns:
        list: Returns a list of images
    """

    # return convert_from_path(file, fmt="png", size=(500, None))

    # Using pdf2image required external dependencies that I could not use
    # Using the PyMuPDF library instead

    file_path = file
    dpi = 300
    zoom = dpi / 72
    magnify = fitz.Matrix(zoom, zoom)  # resizes image, to be more consistent

    # open document
    doc = fitz.open(file_path)

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

        ## resizing the image, so later cv2 qr code recognition runs faster

        # determine scaling factor to resize image by
        # desired final image width
        desired_width = 600

        # producing dsize tuple, to find new dimensions
        current_width = openCV_format.shape[1]
        scaling_factor = current_width / desired_width
        dsize = (600, int(openCV_format.shape[0] / scaling_factor))

        # resize the image, and append it to the images list
        images.append(
            cv2.resize(openCV_format, dsize, interpolation=cv2.INTER_AREA)
        )  # adding the image to the list

        print(f"{page} converted to image, added to list")

    # Return list of generated images
    return images


def progress_bar(num, den):
    # implement a terminal progress bar that is passed a numerator/denominator, and ouputs a progress bar showing the percentage of task completion
    perc = num / den

    ...

"""
TODO Combine functionality of QR_seperator_present and QR_code_present. It will require some branching logic to handle either a single image or a list, but nothing too bad.
Just add the single image to a list, then use the list in the rest of the code


"""



# TODO Change this to accept (list_png, sep_string), better practice to expose it, and do: sep_string = QR_data(list_png[0]) seperately
# should change name to better reflect that it is calling QR_Code_present over the given list, nothing more 
def QR_seperator_present(list_png):
    """This function is passed a list of images, and returns a list of Boolean values indicating whether the seperator QR code is present or no

    Args:
        list_png (_type_): A list of images to check for QR codes

    Returns:
        Boolean list: a list of boolean values, indicating the presence of the seperator qr code on each page
    """

    # TODO needs to be improved, so that a qr page is not required for the first page, only if using a custom one
    default_qr_data = "seperator page"  # placeholder default might change later
    
    sep_string = QR_data(list_png[0])
    
    
    
    # initialising a list to contain location of the seperator pages
    sep_page_location = []

    for i in range(len(list_png)):
        # check whether the seperator QR code is present
        if QR_code_present(list_png[i], sep_string):
            # if true
            sep_page_location.append(True)
        else:
            # if false
            sep_page_location.append(False)
    return sep_page_location

# TODO might want to allow either a bool list or a binary string to be passed, would make it more versatile
def sub_doc_pos(sep_page_pos):
    # this function is given a boolean list, typically produced by QR_sep_present, and returns a list containing tuples, indicating the start and end positions of any number of sub documents that the input pdf will be split into

    # converting the boolean list into a binary string
    binary_string = ""
    for i in range(len(sep_page_pos)):
        bool_value = sep_page_pos[i]
        if bool_value:
            binary_string += "1"
        else:
            binary_string += "0"

    # regex is then used to find a set of tuples, each containing the start and end position of each sub document
    doc_tuples = tuple(re.finditer(r"[0]+", binary_string))

    # initialising tuple list, to store the tuples describing the sub doc positions
    tuple_list = []

    # The information stored in doc_tuples contains more than what is needed, to make working with this information more affective, a new list containing just the start and end positions was created
    for i in range(len(doc_tuples)):
        tuple_list.append(doc_tuples[i - 1].span())

    # The above produces a reversed list, due to using .append(), reversing list
    tuple_list.reverse()

    return tuple_list


def pdf_split(pdf_path, output, doc_tuples):
    # to implement, for now, just outputs each variable
    print(f"pdf filepath\n{pdf_path}")
    print(f"output file\n{output}")
    print(f"sub doc tuples\n{doc_tuples}")

    # Open the pdf to be split as a PyMuPDF document
    doc_src = fitz.open(pdf_path)

    for i in range(len(doc_tuples)):
        # extract start/end position from the list of tuples
        start_page, end_page = doc_tuples[i]

        # create a new blank document
        sub_doc = fitz.open()

        # insert a given range of pages from a given pdf document, doc_src
        sub_doc.insert_pdf(doc_src, from_page=start_page, to_page=end_page, start_at=-1)

        # save the new sub document as a new file, using the output filename provided by user
        sub_doc.save(f"{output}_{i}.pdf")

    # temp return for debugging
    return True, "completed successfully"


# TODO change function implementation to return two values:
# True/False : has a QR code been detected
# QR_Data: A string containing the data contained within  the QR code
def QR_data(image):
    """This function is passed an image, and if found, returns the data contained within a qr code.

    Args:
        image (cv2 image):

    Returns:
        string : decoded text data, or the default seperator value
    """


    QRCodeDetector = cv2.QRCodeDetector()
    decodedText, points, _ = QRCodeDetector.detectAndDecode(image)

    if points is not None:
        # A QR code was found within the image
        return True, decodedText
    else:
        return False, ""


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


# def save_list_png(list_png, output_filepath):
#     for i in range(len(list_png)):
#         im_to_save = list_png[i]
#         # im_to_save = im_to_save.save(f"{output_filepath}/test_image_page_{i}.png")
#         filepath = f"{output_filepath}/test_image_page_{i}.png"
#         cv2.imwrite(filepath, im_to_save)


if __name__ == "__main__":
    main()
