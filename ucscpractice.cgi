#!/usr/bin/python3
import os
import mysql.connector
import cgi, json
import operator
import re
   
def main():
    print("Content-Type: applicaton/json\n\n")
    form = cgi.FieldStorage()
    term = form.getvalue('gene_search')
    genelist = term.split("\r\n")
    #genes2 = ("CDK4 gain", "VHL LOH", "PAX5 mutation") 
    genes = list()
    abn = list()
    for line in genelist:
        m = re.match(r'(.*)\s(.*)', line.rstrip())
        g = m.group(2).lower()
        gr = g.replace("gain", "33,46,220").replace("loss", "253,4,4").replace("loh", "213,11,180").replace("mutation", "100,100,100")
        if m:
            genes.append(m.group(1))
            abn.append(gr)

    conn = mysql.connector.connect(user='genomep', password="password", host="genome-mysql.soe.ucsc.edu", database='hg19')
    curs = conn.cursor()
    results = { 'match_count': 0, 'matches': list()}
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
            results['matches'].append({'chrom':chrom, 'txStart': txStart, 'txEnd':txEnd, 'geneSymbol': geneSymbol, 'score': "0", 'strand':strand, 'cdsStart':cdsStart, 'cdsEnd':cdsEnd, 'rgb': rgb, 'exonCount':exonCount, 'exonsizes': exsub2, 'exonStarts': txstart4})
            results['match_count'] += 1
            bed.append('{0} {1} {2} {3} 0 {4} {5} {6} {7} {8} {9} {10}'.format(str(chrom), str(txStart), str(txEnd), str(geneSymbol), str(strand), str(cdsStart), str(cdsEnd), str(rgb), str(exonCount), str(exsub2), str(txstart4)))
    print(json.dumps(results))
    conn.close()
    
if __name__ == '__main__':
    main()
