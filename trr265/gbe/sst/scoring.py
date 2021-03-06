# AUTOGENERATED! DO NOT EDIT! File to edit: notebooks/10_gbe.sst.scoring.ipynb (unless otherwise specified).

__all__ = ['integration_methods_wrapper', 'verbruggen_quantile', 'integration_without_replacement',
           'get_integration_without_replacement_ssrts', 'mean_method_ssrt', 'get_mean_method_ssrts',
           'get_ssrt_predicted_sep_r', 'get_ssrt_sep', 'get_ssrt_predicted_joint_r', 'get_ssrt_predicted_joint']

# Cell
from .data_provider import SSTDataProvider
import pandas as pd
import numpy as np
from scipy import stats
import biuR.wrapper

# Cell
def integration_methods_wrapper(find_nth_rt):
    def wrapper(df):
        # Calculating the average SSD
        signal = df.query("is_stop==1")
        mean_ssd = signal.ssd.mean()
        # The nth RT is calculated differently by the different integration methods
        nth_rt = find_nth_rt(df) # <- This function is defined by different integration methods (see below).
        # Calculating ssrt
        ssrt = nth_rt - mean_ssd
        return ssrt
    return wrapper

#export
def verbruggen_quantile(rts, p_resp):
    R = biuR.wrapper.R()
    nth = R("""
    nth <- round(quantile(rts, probs = p_resp, type = 6))
    """, push = dict(rts = rts, p_resp = p_resp))
    return nth[0]

# Cell
@integration_methods_wrapper
def integration_without_replacement(df):
    # p_stop is calculated
    p_resp = df.query("is_stop==1").responded.mean() # p_resp matches
    # We include all valid go RTs (this means we exclude premature and late responses)
    no_signal_resp_rts = df.query("is_stop==0 and accuracy==1").rt
    nth_rt = verbruggen_quantile(no_signal_resp_rts, p_resp)
    return nth_rt

def get_integration_without_replacement_ssrts(df):
    return df.groupby('gbe_index').apply(integration_without_replacement).to_frame(name = "ssrt_integration_without_replacement")

# Cell
def mean_method_ssrt(df):
    return df.query("is_stop==0").rt.mean() - df.ssd.mean()

def get_mean_method_ssrts(df):
    return df.groupby('gbe_index').apply(mean_method_ssrt).to_frame(name = "ssrt_mean_method")

# Cell
def get_ssrt_predicted_sep_r(df):
    R = biuR.wrapper.R()
    p = R("""
    library(lmerTest)
    library(ggeffects)
    # Running the model
    control=lmerControl(optimizer = "bobyqa", optCtrl=list(maxfun=1e6))
    m = lmer(ssd_rt ~ 1 + (1 + is_stop | participant), data=df, na.action = na.exclude)
    # Extracting predicted values
    ggpredict(m, terms=c("is_stop","participant"), type="re",ci.lvl = NA)
    """,push=dict(df=df))
    m = R("""m""")
    return p, m

def get_ssrt_sep(df):
    # Creating combined variable for ssd and rt
    df['ssd_rt'] = (df['ssd']).fillna((df.query("is_stop==0").rt))
    dfs = []
    # Looping through sessions
    for session in [2,1]:
        # Extracting data for specific session and trial type
        _df = df.query('(session_number==@session)')
        # Predicting scores
        predicted, m = get_ssrt_predicted_sep_r(_df)
        predicted.columns = ['is_stop','predicted','participant']
        predicted = predicted.set_index(['participant','is_stop']).unstack()
        predicted['ssrt_predicted'] = predicted[('predicted',0.0)] - predicted[('predicted',1.0)]
        predicted = predicted[('ssrt_predicted',  '')].to_frame(name="ssrt_predicted_sep").reset_index()
        # Labeling variables
        predicted['session'] = session
        predicted['gbe_index'] = predicted.participant.astype(str) + '_%03d'%session
        predicted = predicted.set_index('gbe_index')['ssrt_predicted_sep'].to_frame()
# Combining everything into one dataframe
        dfs.append(predicted)
    perc_predicted_sep = pd.concat(dfs)
    return perc_predicted_sep, m

# Cell
def get_ssrt_predicted_joint_r(df):
    R = biuR.wrapper.R()
    p = R("""
    library(lmerTest)
    library(ggeffects)
    # Running the model
    control=lmerControl(optimizer = "bobyqa", optCtrl=list(maxfun=1e6))
    m = lmer(ssd_rt ~ 1 + (1 | is_stop / participant / session), data=df, na.action = na.exclude)
    # Extracting predicted values
    ggpredict(m, terms=c("participant", "is_stop", "session"), type="re",ci.lvl = NA)
    """,push=dict(df=df))

    m = R("""m""")
    return p, m

def get_ssrt_predicted_joint(df):
    df['ssd_rt'] = (df['ssd']).fillna((df.query("is_stop==0").rt))
    df['session'] = df.session_number.astype(str) # making session a factor
    # Predicting scores
    predicted, m = get_ssrt_predicted_joint_r(df)
    predicted.columns = ['participant','predicted','is_stop','session']
    predicted = predicted.set_index(['participant','session','is_stop']).unstack()
    predicted['ssrt_predicted_joint'] = predicted[('predicted','0')] - predicted[('predicted','1')]
    predicted = predicted[('ssrt_predicted_joint','')].to_frame(name="ssrt_predicted_joint").reset_index()
    predicted['gbe_index'] = predicted.participant.astype(str) + predicted.session.apply(lambda x: '_%03d'%int(float(x))).astype(str)
    predicted = predicted.set_index('gbe_index')['ssrt_predicted_joint'].to_frame()
    # Removing sessions that were not in initial dataframe
    predicted = predicted.loc[df.gbe_index.unique()]
    return predicted, m