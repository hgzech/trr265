# AUTOGENERATED! DO NOT EDIT! File to edit: notebooks/30_gbe.longitudinal_data.ipynb (unless otherwise specified).

__all__ = ['pearson_r', 'lmer', 'cor', 'pearson_r', 'lmer', 'cor', 'pearson_r', 'lmer', 'cor', 'pearson_r', 'lmer',
           'cor', 'pearson_r', 'lmer', 'cor', 'pearson_r', 'lmer', 'cor']

# Cell
%load_ext autoreload
%autoreload 2
from .ist.data_provider import ISTDataProvider
from .wm.data_provider import WMDataProvider
from .sst.data_provider import SSTDataProvider
from .rtt.data_provider import RTTDataProvider

import trr265.gbe.ist.scoring as ist_scoring
import trr265.gbe.wm.scoring as wm_scoring
import trr265.gbe.sst.scoring as sst_scoring
import trr265.gbe.rtt.scoring as rtt_scoring

import pandas as pd

# Cell
cor = pd.concat([drinking, tasks], axis = 1).dropna()
import biuR

def pearson_r(x, y, df):
    return scipy.stats.pearsonr(df[x], df[y])


#export
def lmer(x, y, df):
    R = biuR.wrapper.R()
    p = R("""
    library(lmerTest)
    library(ggeffects)
    # Running the model
    control=lmerControl(optimizer = "bobyqa", optCtrl=list(maxfun=1e6))
    m = lmer(%(y)s ~ %(x)s + (1 | participant), data=df, na.action = na.exclude)
    estimate = summary(m)$coefficients[2]
    p_value = summary(m)$coefficients[10]
    """%{'x':x,'y':y},push=dict(df=df))


    m = R("""m""")
    estimate = R("""estimate""")
    p_value = R("""p_value""")

    return estimate[0], p_value[0]

lmer('wm_no_1','g_alc_mean',cor)

# Cell
%load_ext autoreload
%autoreload 2
from .ist.data_provider import ISTDataProvider
from .wm.data_provider import WMDataProvider
from .sst.data_provider import SSTDataProvider
from .rtt.data_provider import RTTDataProvider

import trr265.gbe.ist.scoring as ist_scoring
import trr265.gbe.wm.scoring as wm_scoring
import trr265.gbe.sst.scoring as sst_scoring
import trr265.gbe.rtt.scoring as rtt_scoring

import pandas as pd

# Cell
cor = pd.concat([drinking, tasks], axis = 1).dropna()
import biuR

def pearson_r(x, y, df):
    return scipy.stats.pearsonr(df[x], df[y])


#export
def lmer(x, y, df):
    R = biuR.wrapper.R()
    p = R("""
    library(lmerTest)
    library(ggeffects)
    # Running the model
    control=lmerControl(optimizer = "bobyqa", optCtrl=list(maxfun=1e6))
    m = lmer(%(y)s ~ %(x)s + (1 | participant), data=df, na.action = na.exclude)
    estimate = summary(m)$coefficients[2]
    p_value = summary(m)$coefficients[10]
    """%{'x':x,'y':y},push=dict(df=df))


    m = R("""m""")
    estimate = R("""estimate""")
    p_value = R("""p_value""")

    return estimate[0], p_value[0]

lmer('wm_no_1','g_alc_mean',cor)

# Cell
%load_ext autoreload
%autoreload 2
from .ist.data_provider import ISTDataProvider
from .wm.data_provider import WMDataProvider
from .sst.data_provider import SSTDataProvider
from .rtt.data_provider import RTTDataProvider

import trr265.gbe.ist.scoring as ist_scoring
import trr265.gbe.wm.scoring as wm_scoring
import trr265.gbe.sst.scoring as sst_scoring
import trr265.gbe.rtt.scoring as rtt_scoring

import pandas as pd

# Cell
cor = pd.concat([drinking, tasks], axis = 1).dropna()
import biuR

def pearson_r(x, y, df):
    return scipy.stats.pearsonr(df[x], df[y])


#export
def lmer(x, y, df):
    R = biuR.wrapper.R()
    p = R("""
    library(lmerTest)
    library(ggeffects)
    # Running the model
    control=lmerControl(optimizer = "bobyqa", optCtrl=list(maxfun=1e6))
    m = lmer(%(y)s ~ %(x)s + (1 | participant), data=df, na.action = na.exclude)
    estimate = summary(m)$coefficients[2]
    p_value = summary(m)$coefficients[10]
    """%{'x':x,'y':y},push=dict(df=df))


    m = R("""m""")
    estimate = R("""estimate""")
    p_value = R("""p_value""")

    return estimate[0], p_value[0]

lmer('wm_no_1','g_alc_mean',cor)

# Cell
%load_ext autoreload
%autoreload 2
from .ist.data_provider import ISTDataProvider
from .wm.data_provider import WMDataProvider
from .sst.data_provider import SSTDataProvider
from .rtt.data_provider import RTTDataProvider

import trr265.gbe.ist.scoring as ist_scoring
import trr265.gbe.wm.scoring as wm_scoring
import trr265.gbe.sst.scoring as sst_scoring
import trr265.gbe.rtt.scoring as rtt_scoring

import pandas as pd

# Cell
cor = pd.concat([drinking, tasks], axis = 1).dropna()
import biuR

def pearson_r(x, y, df):
    return scipy.stats.pearsonr(df[x], df[y])


#export
def lmer(x, y, df):
    R = biuR.wrapper.R()
    p = R("""
    library(lmerTest)
    library(ggeffects)
    # Running the model
    control=lmerControl(optimizer = "bobyqa", optCtrl=list(maxfun=1e6))
    m = lmer(%(y)s ~ %(x)s + (1 | participant), data=df, na.action = na.exclude)
    estimate = summary(m)$coefficients[2]
    p_value = summary(m)$coefficients[10]
    """%{'x':x,'y':y},push=dict(df=df))


    m = R("""m""")
    estimate = R("""estimate""")
    p_value = R("""p_value""")

    return estimate[0], p_value[0]

lmer('wm_no_1','g_alc_mean',cor)

# Cell
%load_ext autoreload
%autoreload 2
from .ist.data_provider import ISTDataProvider
from .wm.data_provider import WMDataProvider
from .sst.data_provider import SSTDataProvider
from .rtt.data_provider import RTTDataProvider

import trr265.gbe.ist.scoring as ist_scoring
import trr265.gbe.wm.scoring as wm_scoring
import trr265.gbe.sst.scoring as sst_scoring
import trr265.gbe.rtt.scoring as rtt_scoring

import pandas as pd

# Cell
cor = pd.concat([drinking, tasks], axis = 1).dropna()
import biuR

def pearson_r(x, y, df):
    return scipy.stats.pearsonr(df[x], df[y])


#export
def lmer(x, y, df):
    R = biuR.wrapper.R()
    p = R("""
    library(lmerTest)
    library(ggeffects)
    # Running the model
    control=lmerControl(optimizer = "bobyqa", optCtrl=list(maxfun=1e6))
    m = lmer(%(y)s ~ %(x)s + (1 | participant), data=df, na.action = na.exclude)
    estimate = summary(m)$coefficients[2]
    p_value = summary(m)$coefficients[10]
    """%{'x':x,'y':y},push=dict(df=df))


    m = R("""m""")
    estimate = R("""estimate""")
    p_value = R("""p_value""")

    return estimate[0], p_value[0]

lmer('wm_no_1','g_alc_mean',cor)

# Cell
%load_ext autoreload
%autoreload 2
from .ist.data_provider import ISTDataProvider
from .wm.data_provider import WMDataProvider
from .sst.data_provider import SSTDataProvider
from .rtt.data_provider import RTTDataProvider

import trr265.gbe.ist.scoring as ist_scoring
import trr265.gbe.wm.scoring as wm_scoring
import trr265.gbe.sst.scoring as sst_scoring
import trr265.gbe.rtt.scoring as rtt_scoring

import pandas as pd

# Cell
%load_ext autoreload
%autoreload 2
from .ist.data_provider import ISTDataProvider
from .wm.data_provider import WMDataProvider
from .sst.data_provider import SSTDataProvider
from .rtt.data_provider import RTTDataProvider

import trr265.gbe.ist.scoring as ist_scoring
import trr265.gbe.wm.scoring as wm_scoring
import trr265.gbe.sst.scoring as sst_scoring
import trr265.gbe.rtt.scoring as rtt_scoring

import pandas as pd

# Cell
cor = pd.concat([drinking, tasks], axis = 1).dropna()
import biuR

def pearson_r(x, y, df):
    return scipy.stats.pearsonr(df[x], df[y])


#export
def lmer(x, y, df):
    R = biuR.wrapper.R()
    p = R("""
    library(lmerTest)
    library(ggeffects)
    # Running the model
    control=lmerControl(optimizer = "bobyqa", optCtrl=list(maxfun=1e6))
    m = lmer(%(y)s ~ %(x)s + (1 | participant), data=df, na.action = na.exclude)
    estimate = summary(m)$coefficients[2]
    p_value = summary(m)$coefficients[10]
    """%{'x':x,'y':y},push=dict(df=df))


    m = R("""m""")
    estimate = R("""estimate""")
    p_value = R("""p_value""")

    return estimate[0], p_value[0]