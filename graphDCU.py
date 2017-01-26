import argparse
import ROOT
from ROOT import TFile, TGraph, TTree, TH1F, TBranch, TMultiGraph, TCanvas
import array 
import time

chCount = 7

parser = argparse.ArgumentParser(description='Parse DCU Data')
parser.add_argument('-f', '--file', type=str, nargs='?', default=None,
                    help="Input data file")

args = parser.parse_args()
if args.file is None:
    print 'Give me a file!'
    exit()

print 'Processing {0}'.format(args.file)




f = TFile(args.file)
tree = f.Get('DCUdata')
branches = tree.GetListOfBranches()

dbl = array.array('d', [0,0,0,0,0,0,0])

data = {}

for i in range(0, branches.GetEntries()):

    branch = branches.At(i)
    name = branch.GetName()
    branch.SetAddress(dbl)
    data[name] = {}
    for ch in xrange(chCount):
        data[name][ch] = []
        
    for entry in xrange(branch.GetEntries()): 
        branch.GetEntry(entry)
        for i in xrange(chCount):
            data[name][i].append(dbl[i])



f.Close()

c = TCanvas("c1", "c1", 600, 600)

for key in data.keys():
    mg = TMultiGraph()
    graphs = []
    for ch in data[key]:
        vals = data[key][ch]
        y = array.array('d', vals)
        x = array.array('d', range(0, len(vals)))
        graph = TGraph(len(vals), x, y)
        graph.SetTitle("{0}, Channel {1}".format(key, ch+1))
        graphs.append(graph)

    marker = 20
    for graph in graphs:
        graph.SetMarkerStyle(marker)
        graph.SetMarkerColor(marker-18)
        graph.SetFillStyle(0)

        mg.Add(graph, "ALP")
        marker += 1

    mg.SetTitle('{0} Channels'.format(key))
    mg.Draw('{0} Channels'.format(key))
    c.BuildLegend()
    c.Update()
    
    time.sleep(3)






