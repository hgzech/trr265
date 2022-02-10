# AUTOGENERATED! DO NOT EDIT! File to edit: notebooks/11_gbe.rtt.scoring.ipynb (unless otherwise specified).

__all__ = ['get_percentage_gamble', 'get_perc_gamble_predicted_sep_r', 'get_perc_gamble_predicted_sep',
           'get_perc_gamble_predicted_joint_r', 'get_perc_gamble_predicted_joint']

# Cell
from .data_provider import RTTDataProvider
import pandas as pd
import numpy as np
from scipy import stats
import biuR.wrapper

# Cell
def get_percentage_gamble(df):
    percentage_gamble = df.groupby(['gbe_index','trial_type'])['gambled'].mean().unstack()
    percentage_gamble = percentage_gamble.add_prefix('perc_gamble_')
    return percentage_gamble

# Cell
def get_perc_gamble_predicted_sep_r(df):
    R = biuR.wrapper.R()
    p = R("""
    library(lmerTest)
    library(ggeffects)
    # Running the model
    control=glmerControl(optimizer = "bobyqa", optCtrl=list(maxfun=1e6))
    m = glmer(is_gamble ~ 1 + (1 | participant), data=df, family=binomial, control = control, na.action = na.exclude)
    # Extracting predicted values
    ggpredict(m, terms=c("participant"), type="re",ci.lvl = NA)
    """,push=dict(df=df))
    return p

def get_perc_gamble_predicted_sep(df):
    df['is_gamble'] = df.gambled.astype(int)
    dfs = []
    # Looping through trial types
    for trial_type in ['win','loss','mixed']:
        session_dfs = []
        # Looping through sessions
        for session in [2,1]:
            # Extracting data for specific session and trial type
            _df = df.query('(session_number==@session) and (trial_type==@trial_type)')
            # Predicting scores
            predicted = get_perc_gamble_predicted_sep_r(_df)
            # Labeling variables
            predicted.columns = ['participant','perc_gamble_sep_%s'%trial_type,'session']
            predicted['session'] = session
            predicted['gbe_index'] = predicted.participant.astype(str) + '_%03d'%session
            predicted = predicted.set_index('gbe_index')['perc_gamble_sep_%s'%trial_type].to_frame()
    # Combining everything into one dataframe
            session_dfs.append(predicted)
        dfs.append(pd.concat(session_dfs))
    perc_gamble_sep = pd.concat(dfs, axis = 1)
    return perc_gamble_sep

# Cell
def get_perc_gamble_predicted_joint_r(df):
    R = biuR.wrapper.R()
    p = R("""
    library(lmerTest)
    library(ggeffects)
    # Running the model
    control=glmerControl(optimizer = "bobyqa", optCtrl=list(maxfun=1e6))
    m = glmer(is_gamble ~ 1 + (1 | participant/session), data=df, family=binomial, control = control, na.action = na.exclude)
    # Extracting predicted values
    ggpredict(m, terms=c("participant","session"), type="re",ci.lvl = NA)
    """,push=dict(df=df))

    m = R("""m""")
    return p, m

def get_perc_gamble_predicted_joint(df):
    df['is_gamble'] = df.gambled.astype(int)
    dfs = []
    ms = {}
    # Looping through trial types
    for trial_type in ['win','loss','mixed']:
        # Extracting data for specific trial type
        _df = df.query('(trial_type==@trial_type)')
        _df['session'] = _df.session_number.astype(str) # making session a factor
        # Predicting scores
        predicted, m = get_perc_gamble_predicted_joint_r(_df)
        # Labeling variables
        predicted.columns = ['participant','perc_gamble_joint_%s'%trial_type,'session']
        #predicted['session'] = session
        predicted['gbe_index'] = predicted.participant.astype(str) + predicted.session.apply(lambda x: '_%03d'%int(float(x))).astype(str)
        predicted = predicted.set_index('gbe_index')['perc_gamble_joint_%s'%trial_type].to_frame()
    # Combining everything into one dataframe
        dfs.append(predicted)
        ms[trial_type] = m
    perc_predicted_sep_trial = pd.concat(dfs, axis = 1)
    # Removing sessions that were not in initial dataframe
    perc_predicted_sep_trial = perc_predicted_sep_trial.loc[df.gbe_index.unique()]
    return perc_predicted_sep_trial, ms