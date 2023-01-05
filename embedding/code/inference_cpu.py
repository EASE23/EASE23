import argparse
import time
from utils.cpu.helper import *
from utils.helper import *


parser = argparse.ArgumentParser()
parser.add_argument('--graph', metavar="",  type=str, required=False, default="", help="Path to graph")
parser.add_argument('--out_dir', metavar="",  type=str, required=False, default="", help="Path to directory where the duration is stored.")

args, unknown = parser.parse_known_args()

graph_name = args.graph
device = "cpu"
create_path(graph_name=graph_name, device=device, out_dir=args.out_dir )

mem_report()

START = time.time()
g = load_graph(graph_name).to(device)
load_features(g, graph_name, device)
model = graph_sage(in_dim=g.ndata["attr"].shape[1])
model.to(device)
feats = g.ndata['attr']
embedding = model(g, feats)
DURATION = time.time() - START

mem_report()
store_and_print_results(graph_name=graph_name, device=device, duration=DURATION, out_dir=args.out_dir )