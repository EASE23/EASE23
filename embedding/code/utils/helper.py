import dgl
import dgl.data
import dgl.nn.pytorch as dglnn
from dgl.data import save_tensors, load_tensors
import torch as th
import torch.nn as nn
import torch.nn.functional as F
import os,sys,psutil,GPUtil
import pandas as pd
import time
from dgl.dataloading import GraphDataLoader
from scipy import stats
import cudf
import cugraph
from datetime import datetime

GRAPHS = [
    '/home/ubuntu/ceph/temp/merkel/ICDE23/rw-graphs/com-orkut.ungraph',
    '/home/ubuntu/ceph/temp/merkel/ICDE23/rw-graphs/enwiki-2021',
    '/home/ubuntu/ceph/temp/merkel/ICDE23/rw-graphs/eu-2015-tpd',
    '/home/ubuntu/ceph/temp/merkel/ICDE23/rw-graphs/hollywood-2011',
    '/home/ubuntu/ceph/temp/merkel/ICDE23/rw-graphs/out.orkut-groupmemberships',
    '/home/ubuntu/ceph/temp/merkel/ICDE23/rw-graphs/eu-2015-host',
    '/home/ubuntu/ceph/temp/merkel/ICDE23/rw-graphs/gsh-2015-tpd',
]

MODEL = "code/model/graphsage.pt"

def load_features(graph: dgl.DGLGraph, graph_name: str, device: str) -> dgl.DGLGraph:
    node_feat = load_tensors("{}_feat.dgl".format(graph_name))["attr"].to(device)
    graph.ndata["attr"] = node_feat
    return graph

def create_path(graph_name: str, device: str, out_dir: str) :
    short_graph_name = get_short_name_of(graph_name)
    row = [{
        "graph_name": short_graph_name,
        "device": device,
        "time": -1,
    }]
    pd.DataFrame(row).to_csv(out_dir)

def get_short_name_of(path: str):
    return path.split("/")[-1]

def get_time_stamp():
    now = datetime.now() 
    return now.strftime("%m-%d-%Y-%H-%M-%S")

def store_and_print_results(graph_name: str, device: str, duration: int, out_dir: str):
    short_graph_name = get_short_name_of(graph_name)

    row = [{
        "graph_name": short_graph_name,
        "device": device,
        "time": duration,
    }]
    print(row) 
    pd.DataFrame(row).to_csv(out_dir)

def mem_report():
  GPUs = GPUtil.getGPUs()
  for i, gpu in enumerate(GPUs):
    print('GPU {:d} ... Mem Free: {:.0f}MB / {:.0f}MB | Utilization {:3.0f}%'.format(i, gpu.memoryFree, gpu.memoryTotal, gpu.memoryUtil*100))


class SAGE(nn.Module):
    def __init__(self, in_dim, hidden_dim):
        super(SAGE, self).__init__()
        self.conv1 = dglnn.SAGEConv(in_dim, hidden_dim,"mean")
        self.conv2 = dglnn.SAGEConv(hidden_dim, hidden_dim,"mean")     
        
    def forward(self, g, h):
        # Apply graph convolution and activation.
        h = F.relu(self.conv1(g, h))
        h = F.relu(self.conv2(g, h))
        with g.local_scope():
            g.ndata['h'] = h
            # Calculate graph representation by average readout.
            hg = dgl.mean_nodes(g, 'h')
            return hg

# Two-layer graphsage with mean pooling
def graph_sage(in_dim):
    model = SAGE(in_dim=in_dim, hidden_dim=32)
    model.load_state_dict(th.load(MODEL))
    model.eval()
    return model