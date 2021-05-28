# %%
# import pandas as pd
# import numpy as np
# import lightgbm as lgb
import pickle
# %%
file_name = 'KAERI_lgb_model.pickle'
# %%
with open(file_name, 'rb') as f:
    loaded_model = pickle.load(f)
# %%
loaded_model['X']
# %%
loaded_model['submit']['X'][1756]
# %%
