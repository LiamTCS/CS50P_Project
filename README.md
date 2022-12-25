# Scanned PDF Document Splitter
#### Video Demo:  https://youtu.be/OFb1Tqq4bxI
#### **Description:**
This program can be used to separate a given scanned PDF document, into multiple separate PDF files, based on the presence of separator pages, that each contain a specific QR code.

The program can also produce a PDF of these separator pages, so the user can print them off, to improve their bulk document scanning experience.

#### **Problem that I am trying to solve:**
I have been scanning a lot of documents recently, mostly so I can have a digital copy of hard to replace documents. My combined printer/scanner is very slow to switch between scanning jobs, and it often takes longer to start a new scanning job than it takes to scan short documents individually.

This situation was the inspiration for this program. By producing this solution, I have solved the time-consuming problem of bulk scanning of documents for users in my situation.

To accomplish this, the documents that I want to scan are assembled into a pile, with a separator page, containing a specific QR code, between each individual document. After the document has been scanned the combined PDF is manually passed by the user to this program. The program searches each page of the PDF file and determines whether or not a separator QR code is present.

Once the locations of the separator pages have been determined by the program the file is split into the desired sub documents by the program, removing the separator pages from the resulting documents.

The resulting files are by default saved into a subfolder with the same name as the input file, with a the same filename as the input file but with a incrementing integer appended to the end. If the user wishes to provide a different output filename then they can do so. After the user has enterred the input and output file information the program checks to ensure that the inputs are valid before proceeding to splitting the document.

This program can be used either by passing arguments to it at run time, or by interacting with it via the terminal.

#### **Other functionality**
The program also has the ability to produce a PDF file of the separator pages. It pages can either contain a QR code containing a default set of data, or with a user provided data string. The user inputs the number of desired separator pages, and the program will produce a pdf file of the appropriate length.

In addition to being able to interact with the program by using the command line, users can also operate the program by passing it arguments at runtime. This allows the program to be operated much more efficiently by the end user.

To make using this program even easier I have included several default behaviours. The most useful of which is the default output file behaviour. The default output file behaviour is to make a subfolder within the output folder, which is named according to the input file name. Within this sub folder each of the sub documents will be saved. This behaviour allows the user to stay more organised when splitting a number of documents

## **Explanation of each file/folder within project**
 
### project.py
This is the python file that contains all of the python functions that make up the program as a whole. It contains 11 function in total, ranging from a function that handles user inputs, to a function to handle appropriately splitting a users pdf document. 

The functionality of each function is explained below:

**main()**

main function first determines by what method the user is interacting with the program. It does this dy determining if any input arguments where passed to the program at when it was launched from the command line. If the user did use command line arguments, it then passes the arguments to the args_validation() function, which interprets the arguments and returns program instructions in a standard format.

If the user is interacting with the program though the interactive terminal experience then it calls the user_input() function, which gets a valid set of inputs from the user.

Once main has a valid set of instructions in a standard format it passes these values onto the work_flow() function. work_flow() is responsible for handling the data flow between different functions within the program.

**user_input()**
This insures that the inputs provided by the user during the interactive terminal experience are valid, and if not, will reprompt the user for a new set of inputs. Once a valid set has been produced it returns these values, in a standardised format to the calling function, in the form of a list


**gen_qr_pdf()**

This is the function to produces the QR code seperator pages based on user inputs. The function is given the number of pages and the data string that the QR code will contain before generating a pdf of the appropriate length.

**work_flow()**

the work_flow() function handles the subsequent calling of interdependant tasks. Originally the majority of this functions functionality was a part of the main() function. This portion was seperated out to make the program more maintainable and testable. By seperating the portion of the program that handles aqcuiring valid intputs (main()), and the portion that runs a series of function in order, passing data between them, the program structure is kept more flat. If the work_flow() function was re-integrated into the main() function the program would have many more nested function calls.

**args_validation()**

This function validates any command line arguments passed to the program by the user. And returns the inputs to the calling function in a standard format

**input_validation()**

This function is responsible for determining the validity of user inputs provided during the interactive terminal experience.

**pdf_2_image_list()**

This function is given the filepath to the input pdf, and returns a list containing image data of each pdf page. Originally this function used the module *pdf_2_image*, which proved problematic to this project as it relied on external dependencies that could not be installed using pip. 

As a result of meeting the project requirements with the initial solution I rewrote this function to use the PyMuPDF library (referred to as fitz within the program). Several benifits arose from this rewrite, the most evident being compliance with project requirements, but a secondary benifit of noticeable improving execution time was also realised.

While developing the QR_sep_present function it quickly became apparent that the execution time was stronly dependent on the image size of the image that the opencv function was run against. To improve operational speed of this program functionality was added to this function to resize any generated images to have a maximum width of 600 pixels. This substantially improved user experience. Without resizing the images of the pdf pages it took on average 1.86 seconds per image (page), by resizing the images to a maximum width of 600 pixels the average time taken by openCV per image was substantially reduced to 0.1 seconds, with no reduction in detection accuracy.

**QR_sep_present()**

This function is given the list of image data produced by the pdf_2_image_list() function, and returns a boolean list of the same length indicating if each image contains a qr code containing a given set of data.

It accomplishes this by calling the QR_match function on each image individually, then recording the result.

**QR_match()**
This function is passed a single set of image data, and returns a boolean value depending on whether or not it contains a QR code containing a given set of data

**sub_doc_pos()**

This function is passed the boolean list produced by QR_sep_present(), and returns a list of tuples describing where each of the sub-documents are located witin the large pdf.

It accomplishes this by converting the boolean list into a binary string, for example a boolean list of 

[True, False, False, False, True, False]

would convert to a binary string of 

100010

once converted into a binary string regex is used to find the start and end positions of each match, more specifically the re.finditer() method was used.


**pdf_split()**

This function is passed the file path location of the input pdf and the list of tuples produced by the sub_doc_pos function, and output a series of sub documents produced from these page ranges.

It also handles saving the produced sub-documents, by default placing them in a subfolder within the output folder. All files and directories created are named by default based upon the input file name.

**QR_data()**

This function is passed a single image, and returns two values. The first value is a boolean, indicating whether or not a QR code was present within the image. If a QR code was present then it also returns the data that the QR code contains.

This function is only used on the first scanned page, to determine what the seperator QR code is for this specific document. Although this program is perfectly happy just using the default QR code as an indication as to where to seperate the documents, it can also use a custom QR code seperator. The user can use a custom seperator by ensuring that a page containing their custom seperator is the the first page of the document that they are splitting.

  


## **Challenges overcome**
### **Problem: Initial solution required external dependencies**
The original implementation of pdf_2_image used the "pdf2image" module. This worked as expected but required non pip-installable dependencies.

As a result of this oversight, I rewrote the pdf_2_image function to use the PyMuPDF module, referenced as "fitz" in the module import section. This allowed the project to satisfy the requirement that all dependencies were to be installed through pip. As a bonus this implementation was more performant than the initial one, which will improve user experience.

### **Problem: OpenCV takes a long time**
While testing the QR_seperator_present function I found that the time it takes to perform the opencv QR code recognition on an image is correlated very strongly with the image’s resolution. 
To further explore the issue, I carried out a few tests, through these test I found that by reducing the image resolution to a maximum width of 600 pixels, I was able to substantially improve the time taken by openCv to scan the images. Originally it took roughly 2 seconds per image, by reducing the images to a maximum width of 600 pixels, this time was reduced to 0.1 seconds, a substantial improvement. 

<!-- 

|Size Name|Image Size (px) | Average Run Completion (s)|
|Original|2550x3300 |1.846|
|Large|1080x1398|0.296|
|Medium|768x994|0.169|
|Small|480x621|0.076|

Size Name	Image Size (px) 	 Average Run Completion (s)
Original	2550x3300 	1.846
Large	1080x1398	0.296
Medium	768x994	0.169
Small	480x621	0.076



Size Name	height (px)	width (px)	Avg Time (s)	Total (Mpx)	Mpx/s
Original	2550	3300	1.846	8.415	4.56
Large	1080	1398	0.296	1.50984	5.10
Medium	768	994	0.169	0.763392	4.52
Small	480	621	0.076	0.29808	3.92 -->




### **Problem: Keeping track of the outputs of multiple split documents became a hassle**
Originally the default file output behaviour was to save all of the split documents into the "output" folder. After testing a number of pdf files during development it quickly became apparent that this wasn't a good user experience. Having a multitude of files, all with similiar names, all with appended numbers got troublesome to wade through very quickly. To solve this issue I changed the program to instead produce a sub-folder within the output folder for each input file, with the same name as the input file.
    This ensured that the split documents would remain easy to find for the user, and that the output folder would remain neat and understandable, even after splitting numerous pdf files



## Other notes
This project was developed on a different git repo than it was submitted from. This is because I was travelling while working on this project and could not always access reliable internet. As a result I could not rely on codespaces. To allow myself to continue development independant of internet connectivity I started a new git-repo for this project.

Which can be found at the link below:
https://github.com/LiamTCS/CS50P_Project

This git-repo, which is under the same github account as the codespaces account associated with the other submissions I have made while carrying out the course.

