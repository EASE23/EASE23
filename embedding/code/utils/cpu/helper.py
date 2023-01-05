import pandas as pd
import dgl
import dgl.data
import torch as th

def load_graph(path: str) -> dgl.DGLGraph:
    edges = pd.read_csv(path, header=None,  names=["src", "dst"], sep=" ")
    u = th.tensor(edges["src"])
    v = th.tensor(edges["dst"])
    graph = dgl.graph((u, v))
    return graph