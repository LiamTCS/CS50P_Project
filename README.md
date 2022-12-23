# Scanned PDF Document Splitter
#### Video Demo:  <URL HERE>
#### Description:
This program can be used to separate a given scanned PDF document, into multiple separate PDF files, based on the presence of separator pages, that each contain a specific QR code.

The program can also produce a PDF of these separator pages, so the user can print them off, to improve their bulk document scanning experience.

#### Problem that I am trying to solve
I have been scanning a lot of documents recently, mostly so I can have a digital copy of hard to replace documents. My combined printer/scanner is very slow to switch between scanning jobs, and it often takes longer to start a new scanning job than it takes to scan short documents individually.

This situation was the inspiration for this program. By producing this solution, I have solved the time-consuming problem of bulk scanning of documents for users in my situation.

To accomplish this, the documents that I want to scan are assembled into a pile, with a separator page, containing a specific QR code, between each individual document. After the document has been scanned the combined PDF is manually passed by the user to this program. The program searches each page of the PDF file and determines whether or not a separator QR code is present.

Once the locations of the separator pages have been determined by the program the file is split into the desired sub documents by the program, removing the separator pages from the resulting documents.

The resulting files are named based according to user preference, with an incrementing number appended to the end of the filename, to ensure each produced pdf document has a different file name.

This program can be used either by passing arguments to it at run time, or by interacting with it via the terminal.

## Other functionality
The program also has the ability to produce a PDF file of the separator pages. It pages can either contain a QR code containing a default set of data, or with a user provided data string. The user inputs the number of desired separator pages, and the program will produce a pdf file of the appropriate length.

In addition to being able to interact with the program by using the command line, users can also operate the program by passing it arguments at runtime. This allows the program to be operated much more efficiently by the end user.



# Challenges overcome
# Problem: Initial solution required external dependencies
The original implementation of pdf_2_image used the "pdf2image" module. This worked as expected but required non pip-installable dependencies.

As a result of this oversight, I rewrote the pdf_2_image function to use the PyMuPDF module, referenced as "fitz" in the module import section. This allowed the project to satisfy the requirement that all dependencies were to be installed through pip

# Problem: OpenCV takes a long time
While testing the QR_seperator_present function I found that the time it takes to perform the opencv QR code recognition on an image is correlated very strongly with the image’s resolution. 
To further explore the issue, I carried out a few tests, through these test I found that by reducing the image resolution to a maximum width of 600 pixels, I was able to substantially improve the time taken by openCv to scan the images. Originally it took roughly 2 seconds per image, by reducing the images to a maximum width of 600 pixels, this time was reduced to 0.1 seconds, a substantial improvement. 



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
Small	480	621	0.076	0.29808	3.92






