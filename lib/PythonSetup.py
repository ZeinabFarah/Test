import os, sys, io
import re
from shutil import copyfile
from pathlib import Path, WindowsPath
import fnmatch
import send2trash

from IPython.display import display, clear_output, HTML
from IPython.core.magic import register_cell_magic, needs_local_scope

from amplpy import AMPL, Environment, DataFrame

import pandas as pd
import numpy as np

import ipywidgets
from ipywidgets import interact, interactive, fixed
from ipywidgets import FileUpload, Image, Layout

import networkx as nx
import plotly.graph_objects as go
import plotly.express as px

import tarfile
# import pygraphviz 

import scipy
from scipy.stats import lognorm
from scipy import stats
import matplotlib.pyplot as plt
import math
import random

from numpy import mean
from statistics import stdev

from scipy.special import expit
# import xlsxwriter

import statistics
import copy

import itertools

from scipy.stats import multivariate_normal

# import statsmodels.api as sm
# from statsmodels.nonparametric.kde import kernel_switch

# from KDEpy import FFTKDE
from scipy.interpolate import interp1d

# from KDEpy import FFTKDE
# from KDEpy.bw_selection import silvermans_rule, improved_sheather_jones

from scipy.interpolate import griddata

from scipy import interpolate

import matplotlib.pyplot as plt
# import seaborn as sns
from scipy import stats

import folium
import geopandas as gpd
from branca.colormap import linear
import branca.colormap as cm

import time

from scipy.stats import gaussian_kde, norm

from lib.Installation.setup_NIST_ARC import ReadConfigFile
import warnings