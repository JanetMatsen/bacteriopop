# Topic: BacterioPop
Population dynamics for abundances calculated from meta-omics sequencing
## Vocabulary: 
* node : a node in a network can represent a bacteria or a group of bacteria (super node)
* edge: an edge between two nodes in a network represents an interaction between the corresponding nodes. The edges can be time varying and be added or removed over time. 
* phylogeny: 
# Project Background:
* 88 samples: 4 replicates of high oxygen, 4 replicates of low oxygen, 11 samples per replicate, and 68000 bacteria in each sample. 
* Organisms "phylogeny" is described by: Kingdom, Phylum, Class	Order, Family, Genus

# Project Goals: 
### Data Pre-Processing and Visualization: <ol type = "1">
<li> Center and scale predictors/features (elements of phylogeny) for each sample in order to improve the prediction model as well as detetcting correlations among them. </li>
<li> Plot heat maps for the correlation factor between predictors/features for each sample. </li> 
<li> Plot histograms for detecting class imbalance or skewed distributions of predictors for each sample. </li> 
<li> Reduce sample size be removing highly correlated predictors using correlation factors (good for interpretation) or Principal Component Analysis method (good for prediction). </li> </ol>

### Infer an Interaction Network using Machine Learning Methods:<ol type = "1">
<li> Fixed interaction network:
    * cluster the bacterias based on their phylogeny using unsupervised learning approaches (K-means)
    * represent the fixed network for cluster-cluster interactions with a matrix
    * find the fixed interaction matrix by fitting the data using least square cost function </li> 
<li> Propose a distributed dynamic model for bacteria-bacteria interactions </li> 
<li> Propose a state dependent interaction network:
    * define a distance function that determines the existance of interaction between the nodes. This distance function can be the euclidean distance or inverse distance between the phylogeny of two bacteria
    * fit the time-varying interaction matrix to the data using a stochastic regression method. </li> 
<li> Propose a network dynamic based on the distributed interaction dynamics (part 2) and state-dependent network model (part 3) </li></ol> 

# To-do: <ol type = "1">
<li> Papers that give context to our data. </li> 
<li> Put a link to this public repo in each of our private repositories. </li> 
</ol>
