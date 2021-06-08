import seaborn as sns
import matplotlib.pyplot as plt

import pandas as pd
import numpy as np

import datetime as dt


"""
NOTE:
This file consist of a modified jupyter notebook converted to a script to generate the designated figure
"""

### Bring in CACACO gpad

file = "data/cacao_expanded_info.dat"  # modified CACAO gpad with extra information.

cols = [
    "database",
    "uniprot_id",
    "qualifier",
    "go_id",
    "reference",
    "evidence",
    "with_from",
    "interacting_taxon_id",
    "date",
    "assigned_by",
    "annotation_extension",
    "annotation_properties",
    "go_name",
    "aspect",
    "taxon",
    "domain",
    "query_taxid",
    "superkingdom",
    "kingdom",
    "phylum",
    "class",
    "order",
    "family",
    "genus",
    "organism",
    "species",
    "user_id",
    "url",
    "notes",
]

polished_gpad = pd.read_csv(file, sep="\t", names=cols, comment="!")
expanded_parsed = polished_gpad

replace_with = {
    "cellular_component": "C",
    "molecular_function": "F",
    "biological_process": "P",
}
expanded_parsed = expanded_parsed.replace({"aspect": replace_with})

### Setup functions
def fetch_domain_annotations(df, domain):
    """ Select annotations based on domain from dataframe """

    df = df[df["domain"] == domain]
    return df


def domain_gos(df, domain):
    """ Get all gos & count the amount of times it happens """
    """ couple this with fetch_domain returned dfs"""

    df = (
        df["go_name"]
        .groupby(df["domain"])
        .value_counts()
        .rename("counts")
        .reset_index()
    )
    return df


def calc_the_diff(df1, df2):
    """ Calculate the difference """

    df = len(df1) - int(
        df2["counts"][:1].values
        + df2["counts"][1:2].values
        + df2["counts"][2:3].values
        + df2["counts"][3:4]
    )
    return df


### Setup data for the pie chart

### Subset dataframe based on domains
Euk = fetch_domain_annotations(expanded_parsed, "Eukaryota")
Bac = fetch_domain_annotations(expanded_parsed, "Bacteria")
Vir = fetch_domain_annotations(expanded_parsed, "Viruses")
Arc = fetch_domain_annotations(expanded_parsed, "Archaea")

### Grab GOs based on domain
euk_gos = domain_gos(Euk, "Eukaryota")
bac_gos = domain_gos(Bac, "Bacteria")
vir_gos = domain_gos(Vir, "Viruses")
arc_gos = domain_gos(Arc, "Archaea")


group_names = ["Eukaryota", "Bacteria", "Viruses", "Archaea"]
group_size = [len(Euk), len(Bac), len(Vir), len(Arc)]
numbers = zip(group_names, group_size)

## Grab specifc ranks from domain dataframes
euk_phylum = (
    Euk["phylum"].groupby(Euk["domain"]).value_counts().rename("counts").reset_index()
)  # take top 5
bac_order = (
    Bac["order"].groupby(Bac["domain"]).value_counts().rename("counts").reset_index()
)  # take top 5
vir_family = (
    Vir["family"].groupby(Vir["domain"]).value_counts().rename("counts").reset_index()
)  # take top 5
arc_phylum = (
    Arc["phylum"].groupby(Arc["domain"]).value_counts().rename("counts").reset_index()
)  # take top 2

## Calculate the difference of the total amount of the domain, and the subset top N rank
euk_diff = len(Euk) - (
    int(euk_phylum["counts"][:1].values)
    + int(euk_phylum["counts"][1:2].values)
    + int(euk_phylum["counts"][2:3].values)
    + int(euk_phylum["counts"][3:4].values)
    + int(euk_phylum["counts"][4:5].values)
)

bac_diff = len(Bac) - (
    int(bac_order["counts"][:1].values)
    + int(bac_order["counts"][1:2].values)
    + int(bac_order["counts"][2:3].values)
    + int(bac_order["counts"][3:4].values)
    + int(bac_order["counts"][4:5].values)
)

vir_diff = len(Vir) - (
    int(vir_family["counts"][:1].values)
    + int(vir_family["counts"][1:2].values)
    + int(vir_family["counts"][2:3].values)
    + int(vir_family["counts"][3:4].values)
    + int(vir_family["counts"][4:5].values)
)

arc_diff = len(Arc) - (
    int(arc_phylum["counts"][:1].values) + int(arc_phylum["counts"][1:2].values)
)

euk_names = [
    str(euk_phylum["phylum"][:1].values),
    str(euk_phylum["phylum"][1:2].values),
    str(euk_phylum["phylum"][2:3].values),
    str(euk_phylum["phylum"][3:4].values),
    str(euk_phylum["phylum"][4:5].values),
    "Other",
]
bac_names = [
    str(bac_order["order"][:1].values),
    str(bac_order["order"][1:2].values),
    str(bac_order["order"][2:3].values),
    str(bac_order["order"][3:4].values),
    str(bac_order["order"][4:5].values),
    "Other",
]
vir_names = [
    str(vir_family["family"][:1].values),
    str(vir_family["family"][1:2].values),
    str(vir_family["family"][2:3].values),
    str(vir_family["family"][3:4].values),
    str(vir_family["family"][4:5].values),
    "Other",
]
arc_names = [
    str(arc_phylum["phylum"][:1].values),
    str(arc_phylum["phylum"][1:2].values),
]
#'Other']

all_names = euk_names + bac_names + vir_names + arc_names

fix_names = []
for name in all_names:
    n = name.lstrip("[").rstrip("]").lstrip("'").rstrip("'")
    fix_names.append(n)

euk_counts = [
    int(euk_phylum["counts"][:1]),
    int(euk_phylum["counts"][1:2]),
    int(euk_phylum["counts"][2:3]),
    int(euk_phylum["counts"][3:4]),
    int(euk_phylum["counts"][4:5]),
    euk_diff,
]

bac_counts = [
    int(bac_order["counts"][:1]),
    int(bac_order["counts"][1:2]),
    int(bac_order["counts"][2:3]),
    int(bac_order["counts"][3:4]),
    int(bac_order["counts"][4:5]),
    bac_diff,
]

vir_counts = [
    int(vir_family["counts"][:1]),
    int(vir_family["counts"][1:2]),
    int(vir_family["counts"][2:3]),
    int(vir_family["counts"][3:4]),
    int(vir_family["counts"][4:5]),
    vir_diff,
]

arc_counts = [
    int(arc_phylum["counts"][:1]),
    int(arc_phylum["counts"][1:2]),
]
# arc_diff]

all_counts = euk_counts + bac_counts + vir_counts + arc_counts

### Plot the pie chart

r = 1.5  # radius
w = 0.2  # width
sns.set(rc={"figure.figsize": (11.7, 8.27)})  # alters size of figure

t = plt.cm.Greys
fig, ax = plt.subplots()
ax.axis("equal")
all_pie, text = ax.pie(
    [len(expanded_parsed)],
    radius=r - 0.65,
    labels=["Total Annotations: \n" + str(len(expanded_parsed))],
    autopct=None,
    colors=[t(0.85)],
)


text[0].set_x(0.40)
text[0].set_y(0.05)
text[0].set_color("w")
text[0].set_fontsize("x-large")
text[0].set_fontweight("bold")

plt.setp(all_pie, width=r - 0.65, edgecolor="white")

e, b, v, a = [plt.cm.Reds, plt.cm.Blues, plt.cm.Greens, plt.cm.Purples]
tax_pie, text = ax.pie(
    group_size,
    radius=r,
    labels=[
        str(group_names[0]) + "\n" + str(len(Euk)),
        str(group_names[1]) + "\n" + str(len(Bac)),
        str(group_names[2]) + "\n" + str(len(Vir)),
        str(group_names[3]) + "\n" + str(len(Arc)),
    ],
    autopct=None,
    labeldistance=0.5,
    colors=[e(0.8), b(0.8), v(0.8), a(0.8)],
)

text[0].set_fontsize("xx-large")
text[0].set_color("w")
text[0].set_fontweight("bold")
text[1].set_fontsize("xx-large")
text[1].set_color("w")
text[1].set_fontweight("bold")
text[2].set_fontsize("xx-large")
text[2].set_color("w")
text[2].set_fontweight("bold")
text[3].set_fontsize("xx-large")
text[3].set_color("w")
text[3].set_fontweight("bold")

plt.setp(tax_pie, width=r - 0.5, edgecolor="white")

#################################################
############# Rank Ring #########################
#################################################

e, b, v, a = [plt.cm.Reds, plt.cm.Blues, plt.cm.Greens, plt.cm.Purples]
rank_pie, text = ax.pie(
    all_counts,
    radius=r + 0.1,
    labels=fix_names,
    autopct=None,
    labeldistance=1.005,
    colors=[
        e(0.6),
        e(0.5),
        e(0.4),
        e(0.3),
        e(0.2),
        e(0.1),
        b(0.6),
        b(0.5),
        b(0.4),
        b(0.3),
        b(0.2),
        b(0.1),
        v(0.6),
        v(0.5),
        v(0.4),
        v(0.3),
        v(0.2),
        v(0.1),
        a(0.6),
        a(0.5),
    ],  # , a(0.4)]
)

plt.setp(rank_pie, width=w, edgecolor="white")

#################################################
############# Plot it/check labels ##############
#################################################

plt.title("CACAO Taxon Contributions", y=1.25, fontsize=32)

plt.show()
