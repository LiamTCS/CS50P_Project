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
                qr_data = str(results[3])

            message = gen_qr_pdf(results[2], qr_data)

        elif results[1] == "split":
            # if qr data not given, set it to default value
            if results[4] == "":
                qr_data = default_sep_string
            else:
                qr_data = results[4]

            message = work_flow(results[2], results[3], qr_data)

        else:
            message = "not a match"

    else:
        results = user_input()

        # does user want to print sep pages or split a doc?

        if results[0] == "print":
            # if user wants to print seperator pages
            message = gen_qr_pdf(int(results[1]), results[2])

        elif results[0] == "split":
            # if user wants to split a doc
            message = work_flow(results[1], results[2], default_sep_string)

    print(f"program completed:\n{message}")


def gen_qr_pdf(pages: int, data: str, x=50, y=100) -> str:
    """This function produces a pdf of a given number of pages. Each page contains a QR code containing given data
    
    Args:
        pages (int): the number of seperator pages the PDF should have
        data (str): The data contained in the QR code on each page
        x (int, optional): x dimension of QR code. Defaults to 50.
        y (int, optional): y dimension of QR code. Defaults to 100.

    Returns:
        str: a message string
    """

    temp_qr_file = "pdf_data/temp_qr.png"
    output_pdf = "seperator_page.pdf"

    qr_img = qrcode.make(data)
    qr_img.save(temp_qr_file)

    pdf = FPDF()

    for i in range(pages):

        pdf.add_page()

        pdf.set_font("helvetica", "B", 25)
        pdf.cell(
            w=0,
            h=60,
            txt="Scanned PDF Document Splitter",
            new_x="LMARGIN",
            new_y="NEXT",
            align="C",
        )

        # render image
        pdf.image(temp_qr_file, x=50, y=100)

        # Adding text containing the data of the QR code
        pdf.set_font("helvetica", "", 15)
        pdf.cell(
            w=0,
            h=60,
            txt=f"{data}",
            new_x="LMARGIN",
            new_y="NEXT",
            align="C",
        )

    # saving pdf
    pdf.output(output_pdf)

    return f"pdf of length {pages} pages produced"


def work_flow(pdf_path: str, output_path: str, default_QR: str) -> str:
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


def user_input():
    """This function handles the user input to the program. It checks the validity by passing the user input to the input_validation function. Once the user provides a valid set of user inputs it returns the pdf_file location and the output_file location

    Returns:
        A list containing two strings, as follows
        string: A str containing the location of the input file
        string: A str containing the location of the output file
    """

    while True:
        # Ask whether the user wants to print a seperator page or split a document

        option = input(
            "Enter s to split a PDF, or p to produce a seperator page: ")
        if option == "s":
            pdf_file = input("Enter PDF Filename:\n")
            output_file = input("Desired output filename:\n")

            # stripping leading and trailing quotation marks and whitespace
            in_file = pdf_file.strip().replace("'", "").replace('"', "")
            out_file = output_file.strip().replace("'", "").replace('"', "")

            # set output values
            type = "split"
            output_2 = in_file
            output_3 = out_file

            valid, msg = input_validation(pdf_file, output_file)

            if valid:
                break
            else:
                print(
                    f"User inputs are not valid, for the following reason(s):\n{msg}\nPlease Try Again"
                )
        elif option == "p":
            sep_page_num = input("Enter Number of Seperator pages to produce:")
            qr_data = input("QR data, leave blank for default value:")

            # stripping leading and trailing quotation marks and whitespace
            qr_str = qr_data.strip().replace("'", "").replace('"', "")

            # set output values
            type = "print"
            output_2 = str(sep_page_num)
            output_3 = str(qr_str)

    return [type, output_2, output_3]


def args_validation(args: list) -> list:
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

        elif len(args) == 1:
            # default number of pages is 2
            n_copies = str(2)
            QR_data = ""
            return [True, "print", "2", ""]
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

    else:
        return [False]


def input_validation(in_path: str, output: str) -> tuple:
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

    # stripping in_path of any surrounding quotation marks or whitespace
    in_clean = in_path.replace("'", "").replace('"',"")


    # creating absolute file paths
    pdf_path = join(cur_dir, in_clean)


    
    # User can either specify an output file, or leave it blank
    if output == "":
        # If user specified default output behaviour
        in_name = in_clean.removesuffix(".pdf")
        output_dir = join(cur_dir, f"output/{in_name}")
        
        # check existance of default output directory
        if os.path.isdir(output_dir):
            valid = False
            msg = "output directory already exists"

    else:
        # If user has specified an output file
        
        # creating absolute output path
        output_path = join(cur_dir, output)

        # checking if the output file ends with ".pdf"
        if not output.endswith(".pdf"):
            # if input file doesn't end in .pdf, then not valid
            valid = False
            msg = msg + ' Output File Does not end with ".pdf".'

        # Checking output file
        # checking to ensure the output file does not already exist
        output_exists = exists(output_path)
        if output_exists:
            # File exists, not a valid input
            valid = False
            msg = msg + " Output file already exists."


    # Checking input file
    # Does the input File end in ".pdf"?
    if not in_clean.endswith(".pdf"):
        # if input file doesn't end in .pdf, then not valid
        valid = False
        msg = msg + ' Input File Does not end with ".pdf".'

    # Checking whether the input file already exists, if so inform user
    pdf_exists = exists(pdf_path)
    if not pdf_exists:
        # if input file does not exist
        msg = msg + " Input file does not exist."
        valid = False



    # A msg string with leading whitespace can be produced, this strips it

    return valid, msg.strip()


def pdf_2_image_list(file: str) -> list:
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

    # Return list of generated images
    return images


def QR_sep_present(image_list: list, qr_data: str) -> list:
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


def detect_QR_present(image, qr_data: str) -> bool:
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


def pdf_split(pdf_path: str, output: str, doc_tuples: list):
    """Splits the given input pdf, pdf_path, according to a list of tuples containing start and end pages. These sub documents are then saved to output file(s).

    Args:
        pdf_path (string): location of the input pdf. filename
        output (string): desired output file prefix
        doc_tuples (list): A list containing a series of tuples. Each tuple containing a start page and an end page from which each sub-document will be created
    """
    # Open the pdf to be split as a PyMuPDF document
    doc_src = fitz.open(pdf_path)  # type: ignore

    for i in range(len(doc_tuples)):
        # extract start/end position from the list of tuples
        start_page, end_page = doc_tuples[i]

        # create a new blank document
        sub_doc = fitz.open()  # type: ignore

        # insert a given range of pages from a given pdf document, doc_src
        sub_doc.insert_pdf(doc_src, from_page=start_page,
                           to_page=end_page, start_at=-1)

        # save the new sub document as a new file, using the output filename provided by user
        
        # remove file ending from output
        out_file = output.removesuffix(".pdf")
        
        sub_doc.save(f"{out_file}_{i}.pdf")


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


if __name__ == "__main__":
    main()
