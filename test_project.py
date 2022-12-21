"""test_project.py file, for testing project.py
    executable by pytest

"""
from project import sub_doc_pos, input_validation, QR_data

import pytest
import pickle



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
    ...

# TODO Testing of QR_sep_present
def test_QR_sep_present():
    ...

# TODO Testing of QR_Data
def test_QR_Data_passing():
    # Test what happens when a QR code is present
    
    # loading the appropriate pkl files,
    img1 = pickle.load("test_data/QR_data/img_1.pkl")
    img2 = pickle.load("test_data/QR_data/img_2.pkl")
    img3 = pickle.load("test_data/QR_data/img_3.pkl")
    ...


def test_QR_Data_failing():
    # test what happens when no QR code is present
    
    # Loading the appropriate pkl files
    no_qr_1 = pickle.load("test_data/QR_data/no_qr_1.pkl")
    no_qr_2 = pickle.load("test_data/QR_data/no_qr_2.pkl")
    no_qr_3 = pickle.load("test_data/QR_data/no_qr_3.pkl")
    ...

def test_sub_doc_pos():
    list_1 = [True, False, False, False, False, False, False, True]
    list_2 = [True, False, False, True, False, False, False, False]
    list_3 = [False, False, False]  # no sep pages
    list_4 = [True, False, False, True, False,
              False, True, True, False, False, False]

    assert sub_doc_pos(list_1) == [(1, 7)]
    assert sub_doc_pos(list_2) == [(1, 3), (4, 8)]
    assert sub_doc_pos(list_3) == [(0, 3)]
    assert sub_doc_pos(list_4) == [(4, 6), (1, 3), (8, 11)]

# TODO testing of pdf_split










