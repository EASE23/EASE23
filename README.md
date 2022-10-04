# EASE

# 1 Datasets
The R-MAT graphs were generated with the [R-MAT-Generator](https://github.com/farkhor/PaRMAT). You can create the graphs with this script: [rmat.sh](quality/scripts/rmat.sh)

The Albert-Barabasi graphs where generated with the [SNAP-Generator](https://github.com/snap-stanford/snap/tree/master/examples/graphgen). You can create the graphs with this script: [albert-barabasi.sh](quality/scripts/albert-barabasi.sh)

The Real-world graphs were downloaded from [SNAP](https://snap.stanford.edu/), [Network Repository](http://networkrepository.com/) and [KONECT](http://konect.cc/). You can download the graphs with this script: [realworld.sh](quality/scripts/realworld.sh).

The training and test data for the three prediction tasks can be found here:
1. Graph Processing Run-time: [Training](processing/datasets/graph-processing-run-time_train.csv) and [Test](processing/datasets/graph-processing-run-time_test.csv)
2. Graph Partitioning Run-time: [Training](processing/datasets/graph-partitioning-run-time_train.csv) and [Test](processing/datasets/graph-partitioning-run-time_test.csv)
3. Partitioning Quality Metrics: [Training and Test](quality/data/combined.csv) and [Enrichment](quality/data/enrichment.csv)

# 2 Installation
## 2.1 Clone Repository
Clone the repository and checkout the **submission** branch:
```
git clone https://github.com/EASE23/EASE.git
cd EASE
git checkout submission
```
## 2.2 Jupyter Notebooks
Jupyter Notebooks was used to train the three prediction components of EASE and to create plots.  
In order to run the jupyter notebooks, you need to install *jupyter notebooks* and some additional packages. There are at least two possible ways to do so: 

1. **Anaconda (recommended):** We used this [installer version (directly starts the download)](https://repo.anaconda.com/archive/Anaconda3-2020.11-Linux-x86_64.sh) to install Anaconda on a Ubuntu 18.04.5 LTS machine. Introductions how to run the installer can be found [here](https://docs.anaconda.com/anaconda/install/linux/). In addition, only xgboost needs to be installed. Please follow the official [installation guide](https://xgboost.readthedocs.io/en/latest/install.html).
2. **Pip:** You can create a virtual environment with pip by using the following commands. All packages and the used versions can be found in [requirements.txt](requirements.txt). 
```
python3 -m venv ease
source ease/bin/activate
pip install -r requirements.txt
```

After the installation you can start the jupyter notebooks with the following command:
```
jupyter notebook
```

# 3 Training
If you train a model with EASE, the model will be serialized with Pickle. Please **specify the directory**, where you want to store the models in [file](quality/utils/config.py), [file](processing/notebooks/ProcessingRuntimeLearner.ipynb) and [file](processing/notebooks/PartitioningRuntimeLearner.ipynb) for partitioning quality, graph processing run-time and graph partitioning run-time prediction, respectively. 

## 3.1 Graph Processing Run-time: 
Train models with this [jupyter notebook](processing/notebooks/ProcessingRuntimeLearner.ipynb)

Please find the reported scores in this [notebook](processing/notebooks/run-time-prediction-scores.ipynb)

## 3.2 Graph Partitioning Run-time: 
Train models with this [jupyter notebook](processing/notebooks/PartitioningRuntimeLearner.ipynb)

Please find the reported scores in this [notebook](processing/notebooks/run-time-prediction-scores.ipynb)

## 3.3 Partititioner Quality Predictor Notebooks:   
Train models with the following juyper notebooks:
- [Extreme Gradient Boosting (XGB)](quality/notebooks/XGB.ipynb)
- [K-nearest Neighbors Regressor (KNN)](quality/notebooks/KNN.ipynb)
- [Support Vector Regression (SVR)](quality/notebooks/SVR.ipynb)
- [Random Forest Regressor (RFR)](quality/notebooks/RFR.ipynb)
- [Polynomial Regression](/quality/notebooks/PolyRegression.ipynb)

Please find the reported scores in this [notebook](quality/notebooks/Plotter.ipynb).


# 4. Inference
In order to apply EASE, you need to provide the features (see paper Table 3) in a csv file. An example is given in [example.csv](processing/input/example.csv). You can find EASE in [EASE.py](processing/notebooks/EASE.py), which contains some more documentation. 

Run EASE with the following command to get an overview of the expected parameters:

```
python EASE.py --help
```

It returns the following:
```
usage: EASE.py [-h] --graph_properties  [--partitioners  [...]] --num_partitions  [--processing_algorithm] --num_iterations

optional arguments:
  -h, --help            show this help message and exit
  --graph_properties    Relative path to the file which contains the graph properties.
  --partitioners  [ ...]
                        The partitioners for which EASE should be applied. Default:all, Options: dbh, 2ps, hdrf, crvc, hep100,
                        hep10, 1ds, 1dd, 2d, hep1, ne
  --num_partitions      The number of partitions.
  --processing_algorithm 
                        The graph processing algorithm for which a partitioner should be selected. Default: cc, Options: pr, cc, sssp,
                        k-cores, syn-low, syn-high
  --num_iterations      The number of iterations. Only used for pr, synthetic-low and synthetic-high
```

Example:
```
python EASE.py --graph_properties ../input/example.csv --partitioners dbh 2ps hdrf crvc hep100 hep10 1ds 1dd 2d hep1 ne --num_partitions 4 --optimization_goal end2end --processing_algorithm pr --num_iterations 100
```

It returns:
```
EASE's suggestion: 
 Minimize End-to-End Run-time: hep10 
 Minimize Processing Run-time: hep100
```




