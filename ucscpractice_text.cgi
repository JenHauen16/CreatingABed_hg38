#!/usr/bin/python3
import os
import mysql.connector
import cgi
import operator
import re
   
def main():
    #to save output as a file with a specific file name
    print("Content-Type: application/octet-stream txt")
    print("Content-Disposition: attachment; filename=\"createdbed.bed\"\n\n")
    form = cgi.FieldStorage()
    term = form.getvalue('gene_search')
    genelist = term.split("\r\n")
    genes = list()
    abn = list()
    for line in genelist:
        m = re.match(r'(.*)\s(.*)', line.rstrip())
        g = m.group(2).lower()
        gr = g.replace("gain", "33,46,220").replace("loss", "253,4,4").replace("loh", "213,11,180").replace("mutation", "100,100,100")
        if m:
            genes.append(m.group(1))
            abn.append(gr)

    conn = mysql.connector.connect(user='genomep', password="password", host="genome-mysql.soe.ucsc.edu", database='hg38')
    curs = conn.cursor()
    bed = list() 
    for (gene,rgb) in zip(genes,abn):

        qry = """
            SELECT G.chrom, G.txStart, G.txEnd, X.geneSymbol, G.strand, G.cdsStart, G.cdsEnd,
                 G.exonCount, G.exonStarts, G.exonEnds
            FROM knownGene G
            JOIN kgXref X ON X.kgID=G.name
            JOIN knownCanonical C ON G.name=C.transcript 
            WHERE C.transcript=G.name AND X.geneSymbol LIKE %s
            LIMIT 1;
            """
      
        curs.execute(qry, (gene, ))
  
        for (chrom, txStart, txEnd, geneSymbol, strand, cdsStart, cdsEnd, exonCount, exonStarts, exonEnds) in curs: 
            exonStarts =  exonStarts#.decode('utf-8')
            exonEnds =  exonEnds#.decode('utf-8')
            exonst = exonStarts.split(',')
            exonst1 = list(filter(None, exonst))
            exonst2 = [int(exst) for exst in exonst1]
            exoned = exonEnds.split(',')
            exoned1 = list(filter(None, exoned))
            exoned2 = [int(exed) for exed in exoned1]
            exsub = list(map(operator.sub, exonst2, exoned2))
            exsub1 = [abs(e) for e in exsub]
            exsub2 = str(exsub1).replace(' ', '').replace('[', '').replace(']', '')
            txstart1 = int(txStart)
            txstart2 = [txst - txstart1 for txst in exonst2]
            txstart3 = [abs(txst1) for txst1 in txstart2]
            txstart4 = str(txstart3).replace(' ', '').replace('[', '').replace(']', '')
            bed.append('{0}\t{1}\t{2}\t{3}\t0\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}\t{10}'.format(str(chrom), str(txStart), str(txEnd), str(geneSymbol), str(strand), str(cdsStart), str(cdsEnd), str(rgb), str(exonCount), str(exsub2), str(txstart4)))
    conn.close()
    print("track name=user_defined description=user_defined db=hg38 visibility=2 itemRgb=On" + '\r')
    for entry in bed:
        print(entry + '\r')
           

if __name__ == '__main__':
    main()
