# Scanned PDF Document Splitter
#### Video Demo:  <URL HERE>
#### Description:
I have been scanning a lot of documents recently, mostly so I can have a digital copy of hard to replace documents. My combined printer/scanner is very slow to switch between scanning jobs, and it often takes longer to start a new scanning job than it actually takes to scan short documents individually.

I have a large number of documents that I would like to scan. The inspiration for this program was to come up with a program to help me solve this issue, and to allow me to more efficiently scan a large number of documents.

To accomplish this, the documents that I want to scan are assembled into a pile, with a number of seperator pages, containing a QR code, between each individual document. After the document has been scanned the combined PDF is manually passed by the user to this program. The program searches each page of the PDF file, and determines whether or not a seperator QR code is present.

Once the locations of the seperator pages have been determined by the program the file is split into the desired documents by the program, removing the seperator pages from the resulting documents.

The resulting files are named based on user preference, as a default they share the name of the parent file, but with a number increments appended to the end, or it can use a user provided prefix, with an option to append either an incrementing letter or number to the end.

## Other functionality
The program will also have the ability to produce a PDF file of the seperator page. If the user wants to use a custom QR code in the seperator page, it will also produce an information pdf that must be placed first in the document scan. This information page will contain 2 QR codes, both the default QR code, and the Custom QR code seperator that the user wishes to use.




# Challenges overcome
# Problem: Initial solution required external dependencies
The original implementation of pdf_2_image used the "pdf2image" module. This worked as expected, but required non pip-intallable dependencies.

As a result of this oversight I rewrote the pdf_2_image function to use the PyMuPDF module, referrenced as "fitz" in the module import section. This allowed the project to satisfy the requirement that all dependencies were to be installed through pip


# Problem: OpenCV takes a long time
While testing the QR_seperator_present function I found that the time it takes to perform the opencv QR code recognition on an image is correlated very strongly with the images resolution. 
To further explore the issue I carried out a few tests, the results of which can be seen in the table below.

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

