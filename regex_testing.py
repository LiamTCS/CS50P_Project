import re



sep_pos_string = "11000000001000"


# desired output, tuples containing 


# This is working, definently use this

def main():
    
    doc_list = subdoc_split(sep_pos_string)
    print("Testing seperating the docs, using regex to find page ranges for docs")
    print(f"The returned tuples are:\n{doc_list}")


def subdoc_split(doc_contents):
    
    doc_page_list = tuple(re.finditer(r"[0]+", doc_contents))
    return doc_page_list


if __name__ == "__main__":
    main()