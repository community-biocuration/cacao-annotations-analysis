## Annotation Analysis
### Crowdsourcing biocuration: The Community Assessment of Community Annotation with Ontologies (CACAO) Figure Generation Code
#### Data
* The `cacao_expanded_info.dat` file is a modified gpad that is a precursor to the final quality checked file sent to GO. Additional taxon information as well as various cacao specific fields have their own respective columns. Like a GPAD, it is a tab-delimited file.
    * The taxon information was retrieved and fetched using [ete3](https://github.com/etetoolkit/ete).
* The `cacao_dcnt-tinfo.txt` and `uniprot_dcnt-tinfo.txt` file are results from the [GOATOOLS](https://github.com/tanghaibao/goatools) analysis where the dcnt count for the used GO terms were retrieved.
* `goa_uniprot_all_noiea_20200101.gaf` can be found in the GO Data Archive, found [here](http://release.geneontology.org/2020-01-01/index.html)
#### Pie Charts
* `cacao_taxon_pie.py` generates the taxonomy pie chart.
* `cacao_go_pie.py` generates the GO aspect pie chart.
#### Descendant Count
* `cacao_dcnt.py` generates the descendant box plot comparison.