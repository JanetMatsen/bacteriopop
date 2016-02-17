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
### Data Pre-Processing and Visualization: 
* 1- Center and scale predictors/features (elements of phylogeny) for each sample in order to improve the prediction model as well as detetcting correlations among them.
* 2- Plot heat maps for the correlation factor between predictors/features for each sample
* 3- Plot histograms for detecting class imbalance or skewed distributions of predictors for each sample
* 4- Reduce sample size be removing highly correlated predictors using correlation factors (good for interpretation) or Principal Component Analysis method (good for prediction).

### Infer an Interaction Network using Machine Learning Methods:
* 1- Fixed interaction network:
    * cluster the bacterias based on their phylogeny using unsupervised learning approaches (K-means)
    * represent the fixed network for cluster-cluster interactions with a matrix
    * find the fixed interaction matrix by fitting the data using least square cost function
* 2- Propose a distributed dynamic model for bacteria-bacteria interactions
* 3- Propose a state dependent interaction network:
    * define a distance function that determines the existance of interaction between the nodes. This distance function can be the euclidean distance or inverse distance between the phylogeny of two bacteria
    * fit the time-varying interaction matrix to the data using a stochastic regression method.
* 4- Propose a network dynamic based on the distributed interaction dynamics (part 2) and state-dependent network model (part 3)

# To-do:
* Papers that give context to our data. 
* put a link to this public repo in each of our private repositories. 
