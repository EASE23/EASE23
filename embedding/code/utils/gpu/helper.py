import dgl
import dgl.data
import cudf
import cugraph
def load_graph(path: str) -> dgl.DGLGraph:     
    M = cudf.read_csv(path, delimiter=' ', dtype=['int64', 'int64'], header=None)
    G = cugraph.Graph()
    G = cugraph.from_edgelist(M, source='0', destination='1')
    return  dgl.from_cugraph(G)
