"""test_project.py file, for testing project.py
    executable by pytest

"""
from project import sub_doc_pos

import pytest
import pickle



# TODO Add unit tests for each of the functions in project.py




# TODO Add tests for user_input()




# TODO Input Validation - Passing Tests


# TODO Input Validation - Failing Tests


# TODO testing of pdf_2_image function, will have to investigate how to best test this, maybe with type?


# TODO Testing of QR_seperator_present


# TODO Testing of QR_Data


# TODO testing of sub_doc_pos
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










