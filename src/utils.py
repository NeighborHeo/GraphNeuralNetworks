import os
import sys
sys.path.append(os.path.abspath('..'))
import pathlib
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns

# load music data from mid file
from music21 import converter, instrument, note, chord, stream   
import collections
from collections import Counter

# In[]:
def readNotes(midi):
    # get note pitch from midi
    notes_to_parse = None
    try: # file has instrument parts
        s2 = instrument.partitionByInstrument(midi)
        notes_to_parse = s2.parts[0].recurse()
    except: # file has notes in a flat structure
        notes_to_parse = midi.flat.notes

    notes = []
    for element in notes_to_parse:
        if isinstance(element, note.Note):
            notes.append(str(element.pitch))
        elif isinstance(element, chord.Chord):
            notes.append('.'.join(str(n) for n in element.normalOrder))
    
    return notes

def readNotesFromPath(path):
    midi = converter.parse(path)
    notes = readNotes(midi)
    notes = removeFloatNumber(notes)
    notes = replaceAlphabetToSymbol(notes)
    return notes

# alphabet letter to symbolic notation
def replaceAlphabetToSymbol(notes):
    alphabet_dict = {"A#": "La#", "A": "La", "B": "Si", "C#": "Do#", "C": "Do", "D#": "Re#", "D": "Re", "E": "Mi", "F#": "Fa#", "F": "Fa", "G#": "Sol#", "G": "Sol"}
    for i in range(len(notes)):
        # replace 
        for key, value in alphabet_dict.items():
            if key in notes[i]:
                notes[i] = notes[i].replace(key, value)
                break
    return notes

def removeFloatNumber(notes):
    # for i in range(len(notes)):
    #     import re
    #     notes[i] = re.sub(r'[0-9.-]', '', notes[i])   
    # notes = [n for n in notes if n != '']
    for i in range(len(notes)):
        # if string has '.'
        if '.' in notes[i]:
            notes[i] = ''
    notes = [n for n in notes if n != '']
    return notes

# In[]:

def getUndirectedGraph(edges, self_edges=False):
    G = nx.Graph()
    G.add_nodes_from(edges)
    G.add_edges_from([(edges[i], edges[i+1]) for i in range(len(edges)-1)])
    if not self_edges:
        G.remove_edges_from(nx.selfloop_edges(G))
    return G

def getDirectedGraph(edges, self_edges=False):
    G = nx.DiGraph()
    G.add_nodes_from(edges)
    G.add_edges_from([(edges[i], edges[i+1]) for i in range(len(edges)-1)])
    if not self_edges:
        G.remove_edges_from(nx.selfloop_edges(G))
    return G

def drawGraph(G, labels=True, node_size=1000, font_size=10):
    plt.Figure()
    nx.draw(G, with_labels=labels, node_size=node_size, font_size=font_size)
    plt.show()

def plotGraph(G, labels=True):
    plt.Figure()
    nx.draw(G, with_labels=labels, node_size=1000, font_size=10)
    plt.show()

def savePlotGraph(Path, G, labels=True):
    plt.Figure()
    nx.draw(G, with_labels=labels, node_size=1000, font_size=10)
    plt.savefig(Path, dpi=300)
    plt.show()

def getDegreeDistribution(G):
    degree_sequence = sorted([d for n, d in G.degree()], reverse=True)  # degree sequence
    degreeCount = collections.Counter(degree_sequence)
    deg, cnt = zip(*degreeCount.items())
    return deg, cnt

def drawCountPlot(notes, title):
    notes_count = Counter(notes)
    notes_count = dict(notes_count)
    notes_count = dict(sorted(notes_count.items(), key=lambda item: item[1], reverse=True))
    plt.figure(figsize=(6, 3))
    sns.barplot(x=list(notes_count.keys()), y=list(notes_count.values()))
    plt.title(title)
    plt.show()
    return notes_count
