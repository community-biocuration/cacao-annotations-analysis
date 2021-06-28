import seaborn as sns
import matplotlib.pyplot as plt

import pandas as pd
import numpy as np

import datetime as dt


"""
NOTE:
This file is derived from a jupyter notebook, and was converted to a script to generate the designated figure.
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

### Setup data for the pie chart

process = expanded_parsed[expanded_parsed["aspect"] == "P"]
function = expanded_parsed[expanded_parsed["aspect"] == "F"]
component = expanded_parsed[expanded_parsed["aspect"] == "C"]

process_gos = (
    process["go_name"]
    .groupby(process["aspect"])
    .value_counts()
    .rename("counts")
    .reset_index()
)
function_gos = (
    function["go_name"]
    .groupby(function["aspect"])
    .value_counts()
    .rename("counts")
    .reset_index()
)
component_gos = (
    component["go_name"]
    .groupby(component["aspect"])
    .value_counts()
    .rename("counts")
    .reset_index()
)

process_diff = len(process) - int(
    process_gos["counts"][:1].values
    + process_gos["counts"][1:2].values
    + process_gos["counts"][2:3].values
)
function_diff = len(function) - int(
    function_gos["counts"][:1].values
    + function_gos["counts"][1:2].values
    + function_gos["counts"][2:3].values
)
component_diff = len(component) - int(
    component_gos["counts"][:1].values
    + component_gos["counts"][1:2].values
    + component_gos["counts"][2:3].values
)


group_names = ["Process", "Function", "Component"]
group_size = [len(process), len(function), len(component)]
subgroup_names = [
    str(process_gos["go_name"][:1].values),
    str(process_gos["go_name"][1:2].values),
    str(process_gos["go_name"][2:3].values),
    "Other",
    str(function_gos["go_name"][:1].values),
    str(function_gos["go_name"][1:2].values),
    str(function_gos["go_name"][2:3].values),
    "Other",
    str(component_gos["go_name"][:1].values),
    str(component_gos["go_name"][1:2].values),
    str(component_gos["go_name"][2:3].values),
    "Other",
]

subgroup_size = [
    int(process_gos["counts"][:1]),
    int(process_gos["counts"][1:2]),
    int(process_gos["counts"][2:3]),
    process_diff,
    int(function_gos["counts"][:1]),
    int(function_gos["counts"][1:2]),
    int(function_gos["counts"][2:3]),
    function_diff,
    int(component_gos["counts"][:1]),
    int(component_gos["counts"][1:2]),
    int(component_gos["counts"][2:3]),
    component_diff,
]


subgroup_percents = [
    subgroup_size[0] / len(process) * 100,
    subgroup_size[1] / len(process) * 100,
    subgroup_size[2] / len(process) * 100,
    subgroup_size[3] / len(process) * 100,
    subgroup_size[4] / len(function) * 100,
    subgroup_size[5] / len(function) * 100,
    subgroup_size[6] / len(function) * 100,
    subgroup_size[7] / len(function) * 100,
    subgroup_size[8] / len(component) * 100,
    subgroup_size[9] / len(component) * 100,
    subgroup_size[10] / len(component) * 100,
    subgroup_size[11] / len(component) * 100,
]

fix_names = []
for name in subgroup_names:
    n = name.lstrip("[").rstrip("]").lstrip("'").rstrip("'")
    fix_names.append(n)

### Plot

sns.set()
r = 1.5  # radius
w = 0.2  # width
fig = plt.figure(figsize=(18.7, 12.27))
ax = fig.add_subplot(121)
angle = -55

t = plt.cm.Greys
all_pie, text = ax.pie(
    [len(expanded_parsed)],
    radius=r - 0.65,
    labels=["Total\nAnnotations:\n" + str(len(expanded_parsed))],
    autopct=None,
    startangle=angle,
    colors=[t(0.85)],
)

text[0].set_x(0.25)
text[0].set_y(0.05)
text[0].set_color("w")
text[0].set_fontsize("x-large")
text[0].set_fontweight("bold")

plt.setp(all_pie, width=r - 0.65, edgecolor="white")

explode = [0, 0, 0]
p, f, c = [plt.cm.Purples, plt.cm.Greys, plt.cm.Blues]
aspect_pie, text = ax.pie(
    group_size,
    radius=r,
    labels=[
        str(group_names[0]) + "\n" + str(len(process)),
        str(group_names[1]) + "\n" + str(len(function)),
        str(group_names[2]) + "\n" + str(len(component)),
    ],
    autopct=None,
    startangle=angle,
    labeldistance=0.5,
    colors=[p(0.7), f(0.7), c(0.7)],
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


plt.setp(aspect_pie, width=r - 0.5, edgecolor="white")


def autopct_format(values):
    def my_format(pct):
        total = sum(values)
        val = int(round(pct * total / 100.0))
        return "{v:d}".format(v=val)

    return my_format


w, x, y, z = [0.1, 0.2, 0.3, 0.4]
p, f, c = [plt.cm.Purples, plt.cm.Greys, plt.cm.Blues]
go_pie, text, autotexts = ax.pie(
    subgroup_size,
    radius=r + 0.1,
    labels=fix_names,
    autopct=autopct_format(subgroup_size),
    startangle=angle,
    pctdistance=0.95,
    labeldistance=1.005,
    colors=[
        p(w + 0.15),
        p(x + 0.15),
        p(y + 0.15),
        p(z + 0.15),
        f(w),
        f(x),
        f(y),
        f(z),
        c(w),
        c(x),
        c(y),
        c(z),
    ],
)
for autotext in autotexts:
    autotext.set_color("white")
    autotext.set_fontsize("x-large")
    autotext.set_fontweight("bold")

for tex in text:
    tex.set_fontsize("x-large")


plt.setp(go_pie, width=w + 0.1, edgecolor="white")

plt.show()
