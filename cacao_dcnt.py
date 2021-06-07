
### CACAO GPAD
cacao_gpad_fh = 'data/cacao_expanded_info.dat'

cols = [
    'database',
    'uniprot_id',
    'qualifier',
    'go_id',
    'reference',
    'evidence',
    'with_from',
    'interacting_taxon_id',
    'date',
    'assigned_by',
    'annotation_extension',
    'annotation_properties',
    'go_name',
    'aspect',
    'taxon',
    'domain',
    'query_taxid',
    'superkingdom',
    'kingdom',
    'phylum',
    'class',
    'order',
    'family',
    'genus',
    'organism',
    'species',
    'user_id',
    'url',
    'notes',
]

cacao = pd.read_csv(cacao_paths, sep="\t", names=cols, comment="!", parse_dates=['date'])
cacao = cacao.drop([0,1,2,3])

### UniProt GAF

uniprot_gaf_fh = "goa_uniprot_all_noiea_120.gaf"
uniprot_paths = data_dir + uniprot_gaf_fh

names = [
    'DB',
    'DB Object ID',
    'DB Object Symbol',
    'Qualifier',
    'GO ID',
    'DB:Reference',
    'Evidence Code',
    'With/From',
    'Aspect',
    'DB Object Name',
    'DB Object Synonym',
    'DB Object Type',
    'Taxon',
    'Date',
    'Assigned By',
    'Annotation Extension',
    'GeneProductID',
]

uniprot = pd.read_csv(uniprot_paths, sep="\t", header=None, names=names, parse_dates=['Date'])
uniprot = uniprot[(uniprot['Date'] < '2019-01-01')]
uniprot_with_cacao = len(uniprot)
uniprot = uniprot.loc[uniprot['Assigned By'] != 'CACAO']
uniprot_without_cacao = len(uniprot)

### dcnt analysis
cacao_stats = 'data/cacao_dcnt-tinfo.txt'
uniprot_stats = 'data/uniprot_dcnt-tinfo.txt'

cols = [
    'aspect',
    'go_id',
    'dcnt',
    'tinfo',
    'depth',
    'go_name',
]

cacao_stat_frame = pd.read_csv(cacao_stats, sep="\t", comment="!", names=cols)
uniprot_stat_frame = pd.read_csv(uniprot_stats, sep="\t", comment="!", names=cols)

uniprot_stat_frame['assigned_by'] = 'UniProtKB'
cacao_stat_frame['assigned_by'] = 'CACAO'

uniprot_stat_frame['depth'] = 'D0' + uniprot_stat_frame['depth'].astype(str)

cacao_stat_frame['logged_dcnt'] = np.log(cacao_stat_frame['dcnt'] + 1)
uniprot_stat_frame['logged_dcnt'] = np.log(uniprot_stat_frame['dcnt'] + 1)

all_data = [cacao_stat_frame, uniprot_stat_frame]
combined_stats = pd.concat(all_data).reset_index(drop=True)

uniprot_subset = uniprot[['DB Object ID', 'GO ID', 'Evidence Code']]
uniprot_subset = uniprot_subset.rename(
    {
        'DB Object ID' : 'uniprot_id',
        'GO ID' : 'go_id',
        'Evidence Code' : 'evidence',
    }
    ,axis=1
)

cacao_subset = cacao[['uniprot_id', 'go_id', 'evidence']]

uniprot_combined = uniprot_subset.merge(
    uniprot_stat_frame,
    left_on = ['go_id'],
    right_on = ['go_id'],
    how = 'left'
)

cacao_combined = cacao_subset.merge(
    cacao_stat_frame,
    left_on = ['go_id'],
    right_on = ['go_id'],
    how = 'left'
)

the_final_data = [cacao_combined, uniprot_combined]
combined_all = pd.concat(the_final_data).reset_index(drop=True)

### Graph
sns.set()
sns.set_style("whitegrid")
sns.set_context("talk")
ax = sns.boxplot(
    data=combined_all, 
    x='aspect',
    y='logged_dcnt',
    hue='assigned_by',
    palette="Greys",
    whis=[5,95]
)
plt.legend(bbox_to_anchor=(1.05, 1), loc=2)
ax.set(xlabel="Aspect",ylabel='log(descendant count)')
labels = [
    'Cellular\nComponent', 
    'Biological\nProcess', 
    'Molecular\nFunction'
]
ax.set_xticklabels(labels)
ax.xaxis.labelpad = 20