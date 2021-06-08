## Annotation Analysis
### Crowdsourcing biocuration: The Community Assessment of Community Annotation with Ontologies (CACAO) Figure Generation Code
#### Data
* The `cacao_expanded_info.dat` file is a modified gpad that is a precursor to the final quality checked file sent to GO. Additional taxon information as well as various cacao specific fields have their own respective columns. Like a GPAD, it is a tab-delimited file.
    * The taxon information was retrieved using [ete3](https://github.com/etetoolkit/ete).
* The `cacao_dcnt-tinfo.txt` and `uniprot_dcnt-tinfo.txt` file are results from the [GOATOOLS](https://github.com/tanghaibao/goatools) analysis where the dcnt count for the used GO terms were calculated.
* `goa_uniprot_all_noiea_20200101.gaf` is provided, but can also be located in the [GO Data Archive](http://release.geneontology.org/2020-01-01/index.html).
#### Pie Charts
* `cacao_taxon_pie.py` generates the taxonomy pie chart.
* `cacao_go_pie.py` generates the GO aspect pie chart.
#### Descendant Count
* `cacao_dcnt.py` generates the descendant box plot comparison.
#### Requirements
* `requirements.txt` has all versioned python packages used to generate the figures. [Conda](https://docs.conda.io/en/latest/) was used as the package manager.
#### Notes
* Code was formatted using [Black](https://pypi.org/project/black/)