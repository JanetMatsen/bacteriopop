# BacterioPop Tasks

Population dynamics for abundances calculated from meta-omics sequencing

<b> Vocabulary: </b>
* node : a node in a network can represent a bacteria or a group of bacteria (super node)
* edge: an edge between two nodes in a network represents an interaction between the corresponding nodes. The edges can be time varying and be added or removed over time. 
* phylogeny: the evolution of a genetically related group of organisms as distinguished from the development of the individual organism

<b> Project Background:</b>
* 88 samples: 4 replicates of high oxygen, 4 replicates of low oxygen, 11 samples per replicate, and 68000 bacteria in each sample. 
* Organisms "phylogeny" is described by: Kingdom, Phylum, Class	Order, Family, Genus

<b> Project Goals: </b>
<ol>
<li>Data Pre-Processing and Visualization: 
    <ol type = "1">
    <li> Center and scale predictors/features (elements of phylogeny) for each sample in order to improve the prediction model as well as detetcting correlations among them. 
    <li> Plot heat maps for the correlation factor between predictors/features for each sample. 
    <li> Plot histograms for detecting class imbalance or skewed distributions of predictors for each sample. 
    <li> Reduce sample size be removing highly correlated predictors using correlation factors (good for interpretation) or Principal Component Analysis method (good for prediction). 
    </ol>

<li> Infer an Interaction Network using Machine Learning Methods:
    <ol type = "1">
    <li> Fixed interaction network:<ol>
        <li> cluster the bacterias based on their phylogeny using unsupervised learning approaches (K-means)
        <li> represent the fixed network for cluster-cluster interactions with a matrix
        <li> find the fixed interaction matrix by fitting the data using least square cost function </ol>
    <li> Propose a distributed dynamic model for bacteria-bacteria interactions.
    <li> Propose a state dependent interaction network:
        <ol>
        <li> define a distance function that determines the existance of interaction between the nodes. This distance function can be         the euclidean distance or inverse distance between the phylogeny of two bacteria
        <li> fit the time-varying interaction matrix to the data using a stochastic regression method. 
        </ol>
    <li> Propose a network dynamic based on the distributed interaction dynamics (part 2) and state-dependent network model (part 3) 
    </ol>
</ol>

<b> To-do: </b> 
<ol type = "1">
    <li> Papers that give context to our data. </li> 
    <li> Put a link to this public repo in each of our private repositories. </li> 
</ol>
