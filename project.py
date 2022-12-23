"""Final project.py file"""
import os
import re
import sys


from os.path import exists, join

import cv2  # for identifying QR codes and decoding them
import fitz  # fitz is what PyMuPDF is called
import numpy as np
import qrcode
from fpdf import FPDF

# TODO need to rework the QR_pages class/maybe change how seperator page pdfs are produced?


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

        # render image
        self._pdf.image(def_qr_filepath, x=50, y=100)

    def save_pages(self, name):
        self._pdf.output(name)


def main():
    """This function determines whether or not the program was run from the terminal with arguments, if it was, it determines which arguments, and how they correspond to the program inputs.
    If there are no arguments, then it calls the user_input function, to get input from the user
    """
    # setting default QR code seperator string
    default_sep_string = "seperator page"  # place holder default might change later
    
    
    
    # extract sys.argv to a list
    args = sys.argv[1:]
    
    if len(args) > 0:
        results = args_validation(args)
        if results[1] == "print":
            
            # if qr data not given, set it to default value
            if results[3] == "":
                qr_data = default_sep_string
            else:
                qr_data = results[3]
            msg = produce_qr_page(results[2], qr_data)
            
        if results[1] == "split":
            
            # if qr data not given, set it to default value
            if results[4] == "":
                qr_data = default_sep_string
            else:
                qr_data = results[4]
            msg = work_flow(results[2], results[3], qr_data)
            
        
        
        
    else:
        results = user_input()
        msg = work_flow(results[0], results[1], default_sep_string)
    
    
    print(f"program completed:\n{msg}")
    
    
    # finding the presence of argv's
    
    
    
    # getting user input
    pdf_path, output_path = user_input()

    work_flow(pdf_path, output_path, default_sep_string)

def produce_qr_page(pages, qr_data):
    """Given a number of pages, and qr_data. Produce a pdf document of given number of pages. Each page containing a QR code of given qr_data
    """
    
    #placeholder
    print(f"Number of pages: {pages}\nQR_data: ")
    
    return f"A Pdf with {pages} pages has been produced "
    



def work_flow(pdf_path, output_path, default_QR):
    """for a given set of valid inputs, describing an existing pdf file, and non-existant output pdf file, this function calls a series of other functions to do the following
    1. seperate each pdf page into a seperate image
    2. detect whether or not each image has a specific qr code present
    3. generates output pdf's based on the location of the specific qr code within the document
    4. saves these output pdf's to the user provided location

    Args:
        pdf_path (str): The file path of the pdf to be split according to the presence of a given QR code
        output_path (str): The location that the output files will be saved to
    """
    # producing a list containing images of each pdf page
    doc_images = pdf_2_image_list(pdf_path)

    # Finding the seperator string, either from a qr code on the first page scanned, or the default value

    

    # finding qr_data split string
    # search first page of doc, if no qr present, then use default
    QR_present, data = QR_data(doc_images[0])
    if QR_present:
        sep_string = data
    else:
        sep_string = default_QR

    # determine if the seperator qr code is present in each image from the list
    sep_pos = QR_sep_present(doc_images, sep_string)

    # determine where each sub document starts and ends
    sub_doc_tuples = sub_doc_pos(sep_pos)

    # Split the input pdf based on the list of sub doc tuples
    pdf_split(pdf_path, output_path, sub_doc_tuples)

    return "split completed successfully"

# TODO if the user wants to produce a seperator page, handle that within user input. Maybe before using input() have some branch condition asking the user if they wish to print a sep page?

# TODO add ability to run the page sep from the command line, using argv's

def user_input():
    """This function handles the user input to the program. It checks the validity by passing the user input to the input_validation function. Once the user provides a valid set of user inputs it returns the pdf_file location and the output_file location

    Returns:
        A list containing two strings, as follows
        string: A str containing the location of the input file
        string: A str containing the location of the output file
    """
    
    # TODO remove after testing
    test_pdf = "/home/liams/CS50P_Project/TEST PDF Scans/combined test doc/two_qr_types_test_doc.pdf"
    test_output = "Output/Trial_output"

    pdf_file = input("Enter PDF Filename:\n")
    output_file = input("Desired output filename:\n")


    # TODO remove after testing
    pdf_file = test_pdf
    output_file = test_output

    while True:
        pdf_file = input("Enter PDF Filename:\n")
        output_file = input("Desired output filename:\n")

        valid, msg = input_validation(pdf_file, output_file)

        if valid:
            break
        else:
            print(
                f"User inputs are not valid, for the following reason(s):\n{msg}\nPlease Try Again"
            )
    return [pdf_file, output_file]


def args_validation(args):
    """This function is passed a list of arguments and from it determines a list of program inputs

    Args:
        args (list): a list of arguments, produced by calling args = str(sys.argv[1:])

    Returns:
        list: A list containing data. 
            list[0] will always contain a boolean value, indicating if the arguments were valid or not
            list[2] contains program action. Either print a QR seperator page, or split a document
            list[3] contains either the number of pdf seperator pages to produce, or the file path for the input pdf
            list[4] contains either 
    """

    # determine program action

    if args[0] in ["-p", "--print"]:
        if len(args) == 3:
            # if custom QR data supplied

            # n_copies is kept as string, makes returned data easier to handle
            # to print a double sided pdf, need two pages the same
            n_copies = str(int(args[1]) * 2)
            QR_data = args[2]
            return [True, "print", n_copies, QR_data]

        elif len(args) == 2:
            n_copies = str(int(args[1]) * 2)
            QR_data = ""
            return [True, "print", n_copies, QR_data]

        else:
            # if args are not valid
            return [False, "print", "", ""]

    if args[0] in ["-s", "--split"]:
        if len(args) == 4:
            in_path = args[1]
            out_path = args[2]
            QR_data = args[3]
            return [True, "split", in_path, out_path, QR_data]

        elif len(args) == 3:
            in_path = args[1]
            out_path = args[2]
            QR_data = ""
            return [True, "split", in_path, out_path, QR_data]

        else:
            return [False, "split", "", "", ""]



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

    # To allow handling of relative filepaths, ie output to a subfolder, the absolute filepath needs to be used.

    # finding the filepath of current directory, required for checking for files that are not in the same file as the project.py program
    cur_dir = os.getcwd()

    pdf_path = join(cur_dir, pdf)
    output_path = join(cur_dir, output)

    # Checking file extensions

    # checking if the output file ends with ".pdf"
    if not output.endswith(".pdf"):
        # if input file doesn't end in .pdf, then not valid
        valid = False
        msg = msg + ' Output File Does not end with ".pdf".'

    # Does the input File end in ".pdf"?
    if not pdf.endswith(".pdf"):
        # if input file doesn't end in .pdf, then not valid
        valid = False
        msg = msg + ' Input File Does not end with ".pdf".'

    # Checking filepath validity

    # Checking whether the input file already exists, if so inform user
    if not exists(pdf_path):
        # if input file does not exist
        msg = msg + " Input file does not exist."
        valid = False

    # Checking output file
    # checking to ensure the output file does not already exist
    if exists(output_path):
        # File exists, not a valid input
        valid = False
        msg = msg + " Output file already exists."

    # A msg string with leading whitespace can be produced, this strips it

    return valid, msg.strip()


def pdf_2_image_list(file):
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
    doc = fitz.open(file_path) # type: ignore

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

    # Return list of generated images
    return images


# TODO decide if this should be implemented or not
def progress_bar(num, den):
    # implement a terminal progress bar that is passed a numerator/denominator, and ouputs a progress bar showing the percentage of task completion
    perc = num / den

    ...


def QR_sep_present(image_list, qr_data):
    """This function is passed a list of images, and the qr code data it will search for (qr_data),  and returns a list of Boolean values indicating whether or not a QR code containing "qr_data" is present or not

    Args:
        image_list (list or numpy.ndarray image data): A list of images to check for QR codes
        qr_data (string): data of the qr code function is to determine the presence of
    Returns:
        Boolean list: a list of boolean values, indicating the presence of the seperator qr code on each page
    """

    # initialising a list to contain location of the seperator pages
    sep_page_location = []

    # iterates over each image in the list
    for i in range(len(image_list)):
        # check whether the seperator QR code is present
        if detect_QR_present(image_list[i], qr_data):
            # if true
            sep_page_location.append(True)
        else:
            # if false
            sep_page_location.append(False)
    return sep_page_location


def detect_QR_present(image, qr_data):
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


def sub_doc_pos(sep_page_pos):
    """This function is given a boolean list, describing the presence of the seperator QR code pages, and returns a list of tuples, describing the sub document start and end positions

    Args:
        sep_page_pos (Boolean list): A list containing boolean values

    Returns:
        list: list of tuples. describing the start and end postition of each sub document that will be extracted
    """

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
    """Splits the given input pdf, pdf_path, according to a list of tuples containing start and end pages. These sub documents are then saved to output file(s).

    Args:
        pdf_path (string): location of the input pdf. filename
        output (string): desired output file prefix
        doc_tuples (list): A list containing a series of tuples. Each tuple containing a start page and an end page from which each sub-document will be created
    """
    # Open the pdf to be split as a PyMuPDF document
    doc_src = fitz.open(pdf_path) # type: ignore
 
    for i in range(len(doc_tuples)):
        # extract start/end position from the list of tuples
        start_page, end_page = doc_tuples[i]

        # create a new blank document
        sub_doc = fitz.open() # type: ignore

        # insert a given range of pages from a given pdf document, doc_src
        sub_doc.insert_pdf(doc_src, from_page=start_page,
                           to_page=end_page, start_at=-1)

        # save the new sub document as a new file, using the output filename provided by user
        sub_doc.save(f"{output}_{i}.pdf")


def QR_data(image_data):
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


if __name__ == "__main__":
    main()
