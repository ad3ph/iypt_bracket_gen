import pickle
import numpy as np
import pandas as pd
import glob

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
device = torch.device('cpu')

from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error

from src.genetic_generator import decode_bracket

model = nn.Sequential(
  nn.Linear(70, 700),
  nn.ReLU(),
  nn.Linear(700, 350),
  nn.ReLU(),
  nn.Linear(350, 140),
  nn.ReLU(),
  nn.Linear(140, 35),  
  nn.ReLU(),
  nn.Linear(35, 2),
  )
model.to(device)

model.load_state_dict(torch.load('model_big_14.pkl'))
model.eval()

def get_swap(bracket_as_list):
    print(np.array(decode_bracket(bracket_as_list)[0]))
    return model(torch.tensor(np.array(decode_bracket(bracket_as_list)[0]).reshape((14*len(decode_bracket(bracket_as_list)[0]),)).astype('float32'))).detach().floor().numpy().astype('int')