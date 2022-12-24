"""test_project.py file, for testing project.py
    executable by pytest

"""
import cv2  # used for image loading
import numpy as np

from project import (QR_data, QR_sep_present, args_validation, gen_qr_pdf,
                     input_validation, pdf_2_image_list, sub_doc_pos)


def test_gen_pdf():
    # testing gen_pdf function
    assert gen_qr_pdf(6, "Other test Data") == "pdf of length 6 pages produced"
    assert gen_qr_pdf(12, "test Qr Code") == "pdf of length 12 pages produced"


def test_args_validation_passing():
    """This test function test the passing case of the args_validation function
    """

    # input lists for testing print branch
    args_p_1 = ["-p", "3", ""]
    args_p_2 = ["--print", "2", "test_qr"]
    args_p_3 = ["--print"]

    # input lists for testing split branch
    args_s_1 = ["-s", "input.pdf", "output.pdf"]
    args_s_2 = ["--split", "input.pdf", "output.pdf", "test_qr"]

    # testing print branch
    assert args_validation(args_p_1) == [True, "print", "6", ""]
    assert args_validation(args_p_2) == [True, "print", "4", "test_qr"]
    assert args_validation(args_p_3) == [True, "print", "2", ""]

    # testing split branch
    assert args_validation(args_s_1) == [
        True, "split", "input.pdf", "output.pdf", ""]
    assert args_validation(args_s_2) == [
        True, "split", "input.pdf", "output.pdf", "test_qr"]


def test_args_validation_failing():
    """This test function tests the failing case of the args_validation function
    """

    # input lists for testing print branch
    f_args_p_1 = ["--print", "1", "2", "3", "4"]  # Too many args
    f_args_p_2 = ["-p", "1", "Bobby", "hat",
                  "cat", "sailboat"]  # Too many args

    # input lists for testing split branch
    f_args_s_1 = ["--split", "1", "2", "3", "4"]
    f_args_s_2 = ["-s", "1", "Bobby", "hat", "cat", "sailboat"]

    # input lists for general failing cases
    f_args_1 = ["-test"]
    f_args_2 = ["--p"]
    f_args_3 = ["-print"]
    f_args_4 = ["--s"]
    f_args_5 = ["-split"]

    # invalid flag
    assert args_validation(f_args_1) == [False]
    assert args_validation(f_args_2) == [False]
    assert args_validation(f_args_3) == [False]
    assert args_validation(f_args_4) == [False]
    assert args_validation(f_args_5) == [False]

    # testing invalid print, too many arguments
    assert args_validation(f_args_p_1) == [False, "print", "", ""]
    assert args_validation(f_args_p_2) == [False, "print", "", ""]

    # testing invalid split, too many arguments
    assert args_validation(f_args_s_1) == [False, "split", "", "", ""]
    assert args_validation(f_args_s_2) == [False, "split", "", "", ""]


def test_input_validation_passing():
    pdf_1_path = "test_data/input_val/pdf_test_file.pdf"
    pdf_not_real = "test_data/input_val/output.pdf"

    existing_output = "test_data/input_val/existing_output.pdf"

    assert input_validation(pdf_1_path, pdf_not_real) == (True, "")
    assert input_validation(existing_output, pdf_not_real) == (True, "")


def test_input_validation_failing():
    pdf_1_path = "test_data/input_val/pdf_test_file.pdf"
    pdf_not_real = "test_data/input_val/output.pdf"

    existing_output = "test_data/input_val/existing_output.pdf"
    # does input file not exist?
    assert input_validation(pdf_not_real, "output.pdf") == (
        False, "Input file does not exist.")

    # does output file already exist?
    assert input_validation(pdf_1_path, existing_output) == (
        False, "Output file already exists.")

    # Input file doesnt exist, and output file exists
    assert input_validation(pdf_not_real, existing_output) == (
        False, "Output file already exists. Input file does not exist.")

    # Does Input file end in ".pdf"?
    assert input_validation("test_data/input_val/pdf_test_file", pdf_not_real) == (
        False, 'Input File Does not end with ".pdf". Input file does not exist.')

    # Does output file end in ".pdf"?
    assert input_validation(pdf_1_path, "pdf_test_output.doc") == (
        False, 'Output File Does not end with ".pdf".')


def test_pdf_2_image_list():
    # things we can check
    # var type within list
    # list length

    # Running pdf_2_image_list
    test_pdf_1 = pdf_2_image_list("test_data/pdf_2_img/test_pdf_1.pdf")
    test_pdf_2 = pdf_2_image_list("test_data/pdf_2_img/test_pdf_2.pdf")

    # Testing Pdf 1
    # checking length
    assert len(test_pdf_1) == 20

    # Checking variable type
    assert type(test_pdf_1) == type([])
    # checking list content variable type
    assert type(test_pdf_1[1]) == type(np.ndarray(3))

    # Testing Pdf 2
    # Checking length
    assert len(test_pdf_2) == 7

    # Checking variable type
    assert type(test_pdf_2) == type([])

    # Checking list content variable type
    assert type(test_pdf_2[1]) == type(np.ndarray(3))


def test_QR_sep_present():
    # loading the test PDF's
    test_pdf_1 = pdf_2_image_list("test_data/pdf_2_img/test_pdf_1.pdf")
    test_pdf_2 = pdf_2_image_list("test_data/pdf_2_img/test_pdf_2.pdf")

    # assertions
    assert QR_sep_present(test_pdf_1, "Default_Seperator") == [
        True, True, False, False, False, False, False, False,
        False, False, True, False, False, False, False, False,
        False, False, False, False]

    assert QR_sep_present(test_pdf_2, "Default_Seperator") == [
        True, True, False, False, True, True, False]


def test_QR_Data_passing():
    """Verifying correct behaviour of the QR_Data function
    """

    # Loading the test images
    img1 = cv2.imread("test_data/QR_data/img_1.png")
    img2 = cv2.imread("test_data/QR_data/img_2.png")
    img3 = cv2.imread("test_data/QR_data/img_3.png")

    # assertions
    assert QR_data(img1) == (True, 'test qr code')
    assert QR_data(img2) == (True, 'Default_Seperator')
    assert QR_data(img3) == (True, 'Default_Seperator')


def test_QR_Data_failing():
    """Verifying correct behaviour of the QR_Data function when a QR code is not present
    """

    # Loading the test images
    img1 = cv2.imread("test_data/QR_data/no_qr_1.png")
    img2 = cv2.imread("test_data/QR_data/no_qr_2.png")
    img3 = cv2.imread("test_data/QR_data/no_qr_3.png")

    # assertions
    assert QR_data(img1) == (False, '')
    assert QR_data(img2) == (False, '')
    assert QR_data(img3) == (False, '')


def test_sub_doc_pos():
    """This test checks to ensure that the sub document page ranges are found correctly
    """
    list_1 = [True, False, False, False, False, False, False, True]
    list_2 = [True, False, False, True, False, False, False, False]
    list_3 = [False, False, False]  # no sep pages
    list_4 = [True, False, False, True, False,
              False, True, True, False, False, False]
    list_5 = [True, True, True]

    assert sub_doc_pos(list_1) == [(1, 6)]
    assert sub_doc_pos(list_2) == [(1, 2), (4, 7)]
    assert sub_doc_pos(list_3) == [(0, 2)]
    assert sub_doc_pos(list_4) == [(4, 5), (1, 2), (8, 10)]

    # what if all pages are seperator pages
    assert sub_doc_pos(list_5) == []
