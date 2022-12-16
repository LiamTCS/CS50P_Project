# Scanned PDF Document Splitter
#### Video Demo:  <URL HERE>
#### Description:
I have been scanning a lot of documents recently, mostly so I can have a digital copy of hard to replace documents. My combined printer/scanner is very slow to switch between scanning jobs, and it often takes longer to start a new scanning job than it actually takes to scan short documents individually.

I have a large number of documents that I would like to scan. The inspiration for this program was to come up with a program to help me solve this issue, and to allow me to more efficiently scan a large number of documents.

To accomplish this, the documents that I want to scan are assembled into a pile, with a number of seperator pages, containing a QR code, between each individual document. After the document has been scanned the combined PDF is manually passed by the user to this program. The program searches each page of the PDF file, and determines whether or not a seperator QR code is present.

Once the locations of the seperator pages have been determined by the program the file is split into the desired documents by the program, removing the seperator pages from the resulting documents.

The resulting files are named based on user preference, as a default they share the name of the parent file, but with a number increments appended to the end, or it can use a user provided prefix, with an option to append either an incrementing letter or number to the end.

# Other functionality
The program will also have the ability to produce a PDF file of the seperator page. If the user wants to use a custom QR code in the seperator page, it will also produce an information pdf that must be placed first in the document scan. This information page will contain 2 QR codes, both the default QR code, and the Custom QR code seperator that the user wishes to use.