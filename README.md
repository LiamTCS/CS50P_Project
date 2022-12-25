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

