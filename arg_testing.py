"""this file will be used to help me implemenet argv detection/usage in the project file
Its a bit easier to dev if the runs are instant
"""

import sys






def main():
    
    args = sys.argv[1:]
    
    if len(args) > 0:
        results = args_validation(args)
        print(f"result of args_validation:\n{results}")
    else:
        user_input()
    #print(f"argv's:\n{args}")
    
    ...
    

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



    
    
def user_input():
    usr_in = input("User Input:\n")
    return usr_in    
if __name__ == "__main__":
    main()