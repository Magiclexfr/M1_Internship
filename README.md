# Introduction
This repository is for showing the code made during an Master 1 Internship, whose subject was "Identification de règles de régulation du métabolisme sur des réseaux biologiques à grande échelle".
Due to privacy issues, the code used to create the files analyzed by the scripts of this repository couldn't be displayed here. The name of the algorithm is MERRIN, described in this paper: https://centralesupelec.hal.science/hal-03701755/ .

# Content

## Instances
In the optic of showing that the code works, some instances used during the internship have been saved. The output from MERRIN, the regulatory_rules files, contains the inferred regulatory rules from the experiences of each instance. They are the input for our analysis.
Other files are present. The truthtables are files made by MERRIN, prior to make the regulatory_rules, the final output; they can be ignored. The other files are the results of the analysis and representation, the scripts putting them in the instance to keep some cohesion in the files.

## Scripts

### Disclaimer
The scripts presented here are only the ones used for the analysis of the output from MERRIN and the visualisation on heatmap. Due to some other files required, the scripts for the visualisation of the PKN (GCA in french) and the graph of the analysis weren't added in this repository.
That means that every script here should be usable with the instances files.

### 3-multiple_analysis.ipynb
This script is the one used to analyse, in the form of a Jupyter Notebook. The input will be a folder containing the different files created by MERRIN to infer regulatory rules. The output will be a csv file containing each "mapping" ("node<-clause"), its frequency, the inclusive mappings of this mappings and the exclusives. See the report to understand the meaning behind "mapping". 
This notebook will also print an histogram of the frequency of the mappings, in a growing manner.

### 4-Matrix_analysis.ipynb
This script is also a Jupyter Notebook. It will take the same input but this time the output will be an heatmap of the mappings: if we have one mapping, what will be the frequency of the other mappings. The result will be printed and saved in a png file. The matrix used to create the heatmap is also saved in a csv file.
In an effort to simplify the readings, the omnipresent mappings, which aren't providing any information, are omitted.

## Report files
Since the scripts to make the graph representations aren't available, here is presented the representation of the PKN (GCA in french), and the result of the analysis (as a graph) of the basic instance (named "covert2002_clean"). 

# How to
For each script, there is variable(s) at the top of the notebook (just after the necessary imports) to specify the path of the instance we want to work with, in "Loading inputs".

For "3-mutliple_analysis.ipynb", it's the variable "rules_folder". For example, for the basic instance from the report, '../../instances/covert2002/cov2002_clean/out/truth-tables" should be used. The output will be in a "new" folder (it will erase the previous one) named "Multiple_Analysis" in the folder "cov2002_clean/out/". "cov2002_clean" is the name of the basic instance, and since we used different models the parent folder "covert2002" indicates we used the model "covert2002".

For "4-Matrix_analysis.ipynb", only the "instance_name" variable should be changed. If we use the basic instance of the report, it should be "cov2002_clean". In case another model is used, the name of the folder should be changed in the variable "rules_folder". Again a new folder will erase a previous one, containing the matrix and heatmaps of mapping vs mapping and node vs mapping. Sometimes, the node vs mapping matrix can't be rendered into a heatmap for some reason (the algorithms imported will create the error).

