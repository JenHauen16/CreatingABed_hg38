# CreateBED_AdvFinalProject
Creating a BED

This stack is used to create a 12-column BED file used to assist with genomic analysis. Using the search.html file, users will input a gene list, with the common abnormality, into the text area. After hitting the submit button, a SQL query of the UCSC genome browser's hg19 database returns genomic information necessary to create a 12-column bed file. The CGI file contains python programming to obtain exon sizes and exon start locations to create gene structure and add color to the genes based on the given abnormality.

1) Install Python 3.6.1

2) Install Python modules mysql.connector, cgi, json, operator

3) RGB values for colors are set as: gain=blue, loss=red, loh=purple, and mutation=gray. These can be changed to user preferences in the ucscpractice.cgi.

4) Downloadable file can be loaded as is into programs that accept BED. Header information can be changed to user preferences. Remember to use quotes if spaces are used.




