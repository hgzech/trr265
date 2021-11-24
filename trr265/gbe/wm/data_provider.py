# AUTOGENERATED! DO NOT EDIT! File to edit: notebooks/03_gbe.wm.data_provider.ipynb (unless otherwise specified).

__all__ = ['WMDataProvider']

# Cell
import os
from bs4 import BeautifulSoup
from fastcore.foundation import patch
from ..data_provider import GBEProvider
from ...data_provider import get_efficiently
import pandas as pd
import numpy as np
import xmltodict
import collections

# Cell
class WMDataProvider(GBEProvider):
    '''This class builds upon GBEProvider to get the working memory task data.'''
    def __init__(self, data_folder_path):
        GBEProvider.__init__(self, data_folder_path)

# Cell
@patch
def decode_wm_strings(self:WMDataProvider, gbe_data):
    df = self.decode_gbe_strings(gbe_data, 'WorkingMemoryGame')
    df['success'] = df.success.astype(int)
    return df

# Cell
@patch
@get_efficiently
def get_wm_trial_types(self:WMDataProvider):
    '''This checks that each trial type follows the appropriate specifications.'''
    types = open(os.path.join(self.external, "types.xml"),"r", encoding='UTF-8').read().encode('utf-8')
    types_dict = xmltodict.parse(types)
    type_list = types_dict['trials']['trialtype']
    type_df = []
    for i, t in enumerate(type_list):
        # Getting the type and difficulty
        trial_type = t['@type']
        level = int(t['@difficulty'])
        if level > 10:
            continue
        # Geting individual trial specifications for each type
        for trial in t['trial']:
            trial_dict = {}
            trial_dict['trialid'] = trial['@id'] #id
            trial_dict['trial_type'] = trial_type #
            trial_dict['level'] = level

            # Getting additional information

            board = trial['board']
            # Checking if circles were shown delayed
            if type(board) == collections.OrderedDict:
                board = [board]
            trial_dict['trial_boards'] = []
            # Checking if the trial had distractors
            has_distractor = False
            trial_dict['number_of_boards'] = 0
            for b in board:
                try:
                    if '#text' in b.keys():
                        trial_dict['trial_boards'].append(b['#text'])
                        trial_dict['number_of_boards'] += 1
                    if '#text' in b.keys() and 'D' in b['#text']:
                        has_distractor = True
                        break
                except:
                    print(trial_dict, board)
            is_delayed = int(trial_dict['number_of_boards'] > 1)
            trial_dict['has_distractor'] = int(has_distractor)
            trial_dict['is_delayed'] = int(trial_dict['number_of_boards'] > 1)
            type_df.append(pd.Series(trial_dict))
    type_df = pd.DataFrame(type_df)
    type_df.trial_type.replace({'0':'no_distractor_1',
                               '1':'encoding_distractor',
                               '2':'delayed_distractor',
                               '3':'no_distractor_2'}, inplace = True)
    return type_df

# Cell
@patch
def add_trial_types(self:WMDataProvider, df):
    type_df = self.get_wm_trial_types()
    if 'trial_type' in df.columns:
        df = df.drop.columns('trial_type')
    df = df.merge(type_df[['trialid','trial_type','level']], on = 'trialid', how = 'left', validate = 'many_to_one')
    return df


# Cell
@patch
@get_efficiently
def get_wm_data(self:WMDataProvider):
    gbe_data = self.get_gbe_data()
    df = self.decode_wm_strings(gbe_data)
    df = self.add_trial_types(df)
    return df

# Cell
@patch
def filter_old_app_sessions(self:WMDataProvider, df):
    participants_with_old_app = self.get_gbe_data().loc[df[df.trial_type.isin(['4','5'])].gbe_index.unique()].participant.unique()
    sessions_with_old_app = df[df.trial_type.isin(['4','5'])].gbe_index.unique()
    total_sessions = len(df.gbe_index.unique())
    perc_removed = (len(sessions_with_old_app)/total_sessions)*100
    print("%d participants used an old version of the task in some of their sessions.  %d sessions (%.2f%%) were removed from the dataset."%(len(participants_with_old_app), len(sessions_with_old_app), perc_removed))
    df = df[df.gbe_index.isin(sessions_with_old_app)==False]
    return df

# Cell
@patch
def filter_level_two_failures(self:WMDataProvider, df):
    filtered_sessions = df.query("(level==2) and (success==0)").gbe_index.unique()
    total_sessions = len(df.gbe_index.unique())
    perc_removed = (len(filtered_sessions)/total_sessions)*100
    print("%d sessions (%.2f%%) were removed because participants failed a level two trial."%(len(filtered_sessions), perc_removed))
    df = df[df.gbe_index.isin(filtered_sessions)==False]
    return df