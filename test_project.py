"""test_project.py file, for testing project.py
    executable by pytest

"""
from project import sub_doc_pos, input_validation, QR_data, QR_sep_present, pdf_2_image_list

import pytest
import pickle
import cv2  # used for image loading
import numpy as np


# TODO Add unit tests for each of the functions in project.py


# TODO Add tests for user_input()


# TODO Input Validation - Passing Tests
def test_input_validation_passing():
    ...


# TODO Input Validation - Failing Tests

def test_input_validation_failing():
    ...

# TODO testing of pdf_2_image function, will have to investigate how to best test this, maybe with type?


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

    # TODO Investigate how to assert object is of type class

    # Testing Pdf 2
    # Checking length
    assert len(test_pdf_2) == 7

    # Checking variable type
    assert type(test_pdf_2) == type([])

    # Checking list content variable type
    assert type(test_pdf_2[1]) == type(np.ndarray(3))

# TODO Testing of QR_sep_present


def test_QR_sep_present():
    # loading the test PDF's
    # TODO change this to load a pickle file containing the image list.

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

    assert sub_doc_pos(list_1) == [(1, 7)]
    assert sub_doc_pos(list_2) == [(1, 3), (4, 8)]
    assert sub_doc_pos(list_3) == [(0, 3)]
    assert sub_doc_pos(list_4) == [(4, 6), (1, 3), (8, 11)]

    # what if all pages are seperator pages
    assert sub_doc_pos(list_5) == []

# TODO testing of pdf_split
