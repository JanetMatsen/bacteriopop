<div align="justify">
# BacterioPop
Population dynamics for abundances calculated from meta-omics sequencing

<b> Project Background: </b>
<ol>
<li>    88 samples: 4 replicates of high oxygen, 4 replicates of low oxygen, and 11 samples per replicate. 
<li>    Sequenced for 11 weeks:  week 4 - 14. 
<li>    Oxygen conditions were switched for the last 4 samples. 
<li>    Organisms "taxonomy" is described by: Kingdom, Phylum, Class	Order, Family, Genus
</ol>

Visit our:
<ol>
<li><a href = "https://docs.google.com/presentation/d/1D-DkrJsDJCglwkg9zL4Mdhlwke5hMF6LYhDwvJKBrQc/edit?ts=56ce5662#slide=id.g11bd0970be_0_17"> Technology Review </a>
<li><a href = "https://docs.google.com/presentation/d/1Fndc-2GX0K46gXjrjN7TdrYgU6xtomDJBz4vYtf2edc/edit#slide=id.p4"> Project Poster </a>
</ol>

<b> Tools: </b>

|<p align="center"> Name| <p align="center">Source package | <p align="center">Description | <p align="center"> Output  |
| ----------------------- |:--------------------------------:| -----------------------------:| -------------------------: |
|  <p align="left"> Dynamic Mode Decomposition (DMD)| <p align="center">Python modred|<p align="left"> Dimensionality reduction algorithm for a time series of data that computes a set of modes each of which is associated with a fixed oscillation frequency and decay/growth rate | <p align="left">Matrix of interaction values A for every sample, either computed for every time step or bulked over time |
| <p align="left">  NetworkX| <p align="center"> Third party library NetworkX|<p align="left">Software package for the creation, manipulation, and study of the structure, dynamics, and functions of complex networks|<p align="left"> Classic graphs, random graphs, and synthetic networks with any kind of node (e.g. text, images, XML records) and edges holding arbitrary data (e.g. weights, time-series) |
| <p align="left">  Density-based spatial clustering of applications with noise (DBSCAN)| <p align="center"> Python scikit-learn| <p align="left">Density-based data clustering algorithm that groups together points that are closely packed together, marking as outliers points that lie alone in low-density regions| <p align="left">Clusters of data points with performance metrics|
|  <p align="left"> Gaussian Mixture Models (GMM)|   <p align="center"> Python scikit-learn|<p align="left">Parametric probability density function that generates all data points from weighted sum of Gaussian component densities with unknown parameters|  <p align="left">Clusters of data points with performance metrics|

<b> Directory Structure:

<img src="https://raw.githubusercontent.com/JanetMatsen/bacteriopop/master/maker_files/directory_structure.png" alt="Bacteriopop directory structure">
</b>

<b> Why we chose the Apache License 2.0: </b><br>

The Apache License allows us to manage the software package as we please, while providing clear language regarding the terms. It makes it clear that individual contributors grant copyright license to anyone who receives the code, that their contribution is free from patent encumbrances (and if it is not, that they license that patent to anyone who receives the code,) and that use of Trademarks extends only as far as is necessary to use the product. It also includes a patent termination clause, should a lawsuit arise. The Apache licenses <b>encourage open-source development</b> and our software is made better by every person who runs it, files tickets about it, or patches it. This is invaluable contribution – each user is given freedom and respect from the other members of the developer community.

</div><hr>


<b> Next Steps: </b>
<ol>
<li>    Make one A matrix per sample per replicate (2*4*10 A matrices) & compare to the current results with one A per replicate.  
<li>    Test normalization of data before finding the A matrices so total abundance doesn't dominate signal. Remove taxa with small abundances first. 
<li>    Plot networks as node graphs now that data reduction tools are ready
<li>    Train on a subset of the data and see how predictive it is for the rest
<li>    Compare including vs omitting the last 4 samples of each series, which have the oxygen tension reversed. 
<li>    Do multiple hypothesis corrections, and use this to guide the cutoff for plotting and further analysis. 
<li>    Connect these mathematical results to our real biological questions. 
</ol>
