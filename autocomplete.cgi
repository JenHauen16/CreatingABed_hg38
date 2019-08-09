#!/usr/bin/python3
import os
import mysql.connector
import cgi, json
    
def main():
    print("Content-Type: applicaton/json\n\n")
    form = cgi.FieldStorage()
    term = form.getvalue('gene_search') #no need for #in front of gene_search
    conn = mysql.connector.connect(user='genomep', password="password", host="genome-mysql.soe.ucsc.edu", database='hg19')
    curs = conn.cursor()

    qry = """
            SELECT kgID, geneSymbol
            FROM kgXref 
            WHERE geneSymbol LIKE %s
            LIMIT 3;
            """

    var = term + '%'
    curs.execute(qry, (var,))

    results = []
    for (kgID, geneSymbol) in curs:
        results.append({"value": geneSymbol, "label": geneSymbol})
       
    conn.close()
    print(json.dumps(results))

if __name__ == '__main__':
    main()
