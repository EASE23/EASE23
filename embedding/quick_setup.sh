#!/usr/bin/env bash

conda create -n gc_inference_test python=3.9 -y
conda activate gc_inference_test

conda install pytorch torchvision torchaudio pytorch-cuda=11.6 -c pytorch -c nvidia -y
conda install -c dglteam dgl-cuda11.6 -y
conda install -c conda-forge jupyterlab -y
conda install -c conda-forge ipywidgets -y
conda install -c conda-forge pyarrow -y
conda install pandas -y
conda install -c nvidia -c rapidsai -c numba -c conda-forge cugraph cudatoolkit=11.5

