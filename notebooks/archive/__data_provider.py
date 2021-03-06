#!/usr/bin/env python
# coding: utf-8

# In[2]:


from bs4 import BeautifulSoup as bs
import great_expectations as ge
import numpy as np
import os
import pandas as pd
import types
import dotenv


def get_data_folder():
    return dotenv.dotenv_values()['DATA_FOLDER_PATH']

def get_raw():
    return os.path.join(get_data_folder(), 'raw')

def get_external():
    return os.path.join(get_data_folder(), 'external')

def get_interim():
    return os.path.join(get_data_folder(), 'interim')

def get_processed():
    return os.path.join(get_data_folder(), 'processed')

def store_interim(df, filename):
    path = os.path.join(get_interim(),"%s.parquet"%filename)
    df.to_parquet(path)
    
def load_interim(filename):
    return pd.read_parquet(os.path.join(get_interim(),"%s.parquet"%filename))



def get_efficiently(func):
    """
    This decorator wraps around functions that get data and handles data storage.
    If the output from the function hasn't been stored yet, it stores it in a .parquet file
    If the output from the function has been stored already, it loads the stored file instead of running the function (unless update is specified as True)
    """
    def wrapper(update = False, columns = None, *args, **kw):
        var_name = func.__name__.replace('get_','')
        file_path = os.path.join(get_interim(), "%s.parquet"%var_name)
        if os.path.exists(file_path) and (update == False):
            result =  pd.read_parquet(file_path, columns = columns)
        else:
            print("Preparing %s"%var_name)
            result = func()
            result.to_parquet(file_path)
        return result
    w = wrapper
    w.__wrapped__ = func # Specifying the wrapped function for inspection
    w.__doc__ = func.__doc__
    return w


# In[4]:


def get_alcohol_per_drink():
    return pd.read_csv(os.path.join(get_external(),'alcohol_per_drink.csv'))



def check_participant_id(x):
    '''This function checks whether a participant ID is numerical and lower than 20000.'''
    if str(x) == x:
        if x.isnumeric():
            x = float(x)
        else:
            return False
    if x > 20000:
        return False
    return True

def get_duplicate_mov_ids():
    '''This function creates a dictionary mapping old to new movisens IDs.'''
    df = get_ba_data()
    replace_dict_1 = dict(zip(df.mov_id_old, df.mov_id))
    replace_dict_2 = dict(zip(df.mov_id_old_2, df.mov_id))
    replace_dict = {**replace_dict_1, **replace_dict_2}
    try:
        del replace_dict[np.nan]
    except:
        pass
    return replace_dict
    
def set_dtypes(data, codebook):
    # Parsing type
    codebook['type'] = codebook["Feld Attribute (Feld-Typ, Pr??fung, Auswahlen, Verzweigungslogik, Berechnungen, usw.)"].apply(lambda x: x.split(',')[0]) 
    # Descriptives (not in data)
    desc_columns = list(codebook[codebook.type.str.contains('descriptive')].variable)
    # Datetime
    dt_columns = codebook[(codebook.type.isin(['text (datetime_dmy)','text (date_dmy)']))].variable
    dt_columns = list(set(data.columns).intersection(dt_columns))
    # Numerical
    num_columns = []
    num_columns += list(codebook[codebook.type.str.contains('calc')].variable)
    num_columns += list(codebook[codebook.type.str.contains('checkbox')].variable)
    num_columns += list(codebook[codebook.type.str.contains('radio')].variable)
    num_columns += list(codebook[codebook.type.str.contains('text \(number')].variable)
    num_columns += list(codebook[codebook.type.str.contains('yesno')].variable)
    num_columns += list(codebook[codebook.type.str.contains('dropdown')].variable)
    num_columns += list(codebook[codebook.type.str.contains('slider')].variable)
    num_columns = list(set(data.columns).intersection(num_columns))
    # Text
    text_columns = []
    text_columns += list(codebook[(codebook.type.str.contains('text')) & (~codebook.type.str.contains('date_dmy|datetime_dmy'))].variable)
    text_columns += list(codebook[(codebook.type.str.contains('notes'))].variable)
    text_columns += list(codebook[(codebook.type.str.contains('file'))].variable)
    text_columns = list(set(data.columns).intersection(text_columns))
    assert len(set(num_columns).intersection(set(dt_columns)))==0, set(num_columns).intersection(set(dt_columns))
    assert len(set(text_columns).intersection(set(dt_columns)))==0, set(text_columns).intersection(set(dt_columns))
    
    for c in num_columns:
        data[c].replace("A 'MySQL server has gone away' error was detected.  It is possible that there was an actual database issue, but it is more likely that REDCap detected this request as a duplicate and killed it.", np.nan, inplace = True)
        data[c] = data[c].astype(float)
    data[text_columns] = data[text_columns].astype(str).replace('nan',np.nan)
    
    for c in dt_columns:
        data[c] = pd.to_datetime(data[c])
    return data
    
@get_efficiently
def get_ba_codebook():
    tables = pd.read_html(open(os.path.join(get_external(), "ba_codebook.html","r").read()))
    df = tables[1]
    # Note that str.contains fills NaN values with nan, which can lead to strange results during filtering
    df = df[df.LabelHinweistext.str.contains('Fragebogen:',na=False)==False]
    df = df.set_index('#')
    # Parsing variable name
    df['variable'] = df["Variable / Feldname"].apply(lambda x: x.split(' ')[0])
    # Parsing condition under which variable is displayed
    df['condition'] = df["Variable / Feldname"].apply(lambda x: ' '.join(x.split(' ')[1:]).strip() if len(x.split(' '))>1 else '')
    df['condition'] = df.condition.apply(lambda x: x.replace('Zeige das Feld nur wenn:  ',''))
    # Parsing labels for numerical data
    df['labels'] = np.nan
    labels = tables[2:-1]
    try:
        labels = [dict(zip(l[0],l[1])) for l in labels]
    except:
        display(table)
    searchfor = ["radio","dropdown","yesno","checkbox"]
    with_table = df['Feld Attribute (Feld-Typ, Pr??fung, Auswahlen, Verzweigungslogik, Berechnungen, usw.)'].str.contains('|'.join(searchfor))
    df.loc[with_table,'labels'] = labels
    df = df.astype(str)
    return df

@get_efficiently
def get_ba_data():
    '''This function reads in baseline data from redcap, filters out pilot data, and creates movisens IDs.'''
    df = pd.read_csv(os.path.join(get_raw(),"ba.csv"))
    df['center'] = df.groupby('participant_id').bx_center.transform(lambda x: x.ffill().bfill())
    df['center'] = df.center.replace({1:'b',2:'d',3:'m'})
    # Creating new movisense IDs (adding center prefix to movisense IDs)
    for old_id in ['bx_movisens','bx_movisens_old','bx_movisens_old_2']:
        new_id = old_id.replace('bx_','').replace('movisens','mov_id')
        df[new_id] = df.groupby('participant_id')[old_id].transform(lambda x: x.ffill().bfill())
        df[new_id] = df.center + df[new_id].astype('str').str.strip('0').str.strip('.').apply(lambda x: x.zfill(3))
        df[new_id].fillna('nan',inplace = True)
        df.loc[df[new_id].str.contains('nan'),new_id] = np.nan
    # Removing test participants 
    remove = ['050744', 'hdfghadgfh', 'LindaEngel', 'test', 'Test001', 'Test001a', 'test0011', 'test0012', 'test0013', 'test0014', 'test0015', 'test002', 'test00229', 'test007', 'test01', 'test012', 'test013', 'test1', 'test2', 'test4', 'test12', 'test999', 'test2021', 'test345345', 'testneu', 'testtest', 'test_0720', 'test_10', 'test_GA', 'Test_JH','test0016','891752080', 'pipingTest', 'test0001', 'test00012', 'test0012a', 'test0015a', 'test0017', 'test10', 'test20212', 'testJohn01', 'test_00213', 'test_00233', 'test_00271', 'test_003', 'test_004', 'test_11_26', 'Test_MS']
    df = df[~df.participant_id.astype(str).isin(remove)]
    # Checking participant ids (to find new test participants)
    bad_ids = df[~df.participant_id.apply(check_participant_id)].participant_id.unique()
    assert len(bad_ids)==0, "Bad participant IDs (should be added to remove): %s"%', '.join(["'%s'"%b for b in bad_ids])
    # labeling B07 participant
    b07_pps = pd.read_excel(os.path.join(get_external(), 'b7_participants.xlsx'))['Participant ID'].astype(str)
    df['is_b07'] = False
    df.loc[df.participant_id.isin(b07_pps),'is_b07'] = True
    # Setting dtypes based on codebook
    df = set_dtypes(df, get_ba_codebook())
    # Creating convenience variables
    df['is_female'] = df.screen_gender.replace({1:True,2:False})
    # Filling in missings from baseline
    df['is_female'].fillna(df.bx_sozio_gender.replace({1:False,2:True}), inplace = True)
    df['is_female'] = df.groupby('participant_id')['is_female'].transform(lambda x: x.ffill().bfill())
    return df


@get_efficiently
def get_gbe_data():
    """
    This function gets GBE data.
    1) 
    """
    # Filtering GBE-data from mov-data
    df = get_mov_data()
    gbe_columns = ['FruitTapGame','WorkingMemoryGame','CardGame','RewardAndHappinessGame']
    df[gbe_columns] = df[gbe_columns].replace({'{canceled": true}"':None})
    # We include partial GBE sessions
    df = df[~df[gbe_columns].isna().all(axis=1)]
    # Calculating times since last gbe
    df['time_since_last_gbe'] = df['sampling_day'] - df['sampling_day'].shift(1)
    df.loc[df.groupby('participant')['time_since_last_gbe'].head(1).index, 'time_since_last_gbe'] = np.nan
    df = df.reset_index()
    initial_pps = df.groupby('participant').starting_date.first().sort_values().reset_index().iloc[:300].participant.values
    df['initial'] = df.participant.isin(initial_pps)
    df.index.rename('gbe_index',inplace = True)
    return df


# In[ ]:


@get_efficiently
def get_gbe_baseline_data():
    """This function gets baseline GBE data.
    
    We define baseline data as the first two GBEs each participnat completed on the same day.
    """
    # Filtering baseline data from gbe data
    df = get_gbe_data()
    df = df.groupby('participant').head(2)
    # Selecting only first sessions and sessions that happened one the same day as first
    df['time_since_last_gbe'].fillna(0, inplace = True)
    df = df.query('time_since_last_gbe==0')
    df['baseline_session'] = "Session " + (df.groupby('participant').cumcount()+1).astype(str)
    df = df.reset_index()
    df.index.rename('gbe_baseline_index',inplace = True)    
    return df


# In[ ]:


@get_efficiently
def get_mov_data():
    """
    This function gets Movisense data
    1) We create unique participnat IDs (e.g. "b001"; this is necessary as sites use overapping IDs)
    2) We merge double IDs, so participants with two IDs only have one (for this duplicate_ids.csv has to be updated)
    3) We remove pilot participants
    4) We get starting dates (from the participant overviews in movisense; downloaded as html)
    5) We calculate sampling days and end dates based on the starting dates
    """
    # Loading raw data
    mov_berlin = pd.read_csv(os.path.join(get_raw(), "mov_data_b.csv"), sep = ';')
    mov_dresden = pd.read_csv(os.path.join(get_raw(), "mov_data_d.csv"), sep = ';')
    mov_mannheim = pd.read_csv(os.path.join(get_raw(), "mov_data_m.csv"), sep = ';')
        
    # Merging (participant numbers repeat so we add the first letter of location)
    mov_berlin['location'] = 'berlin'
    mov_dresden['location'] = 'dresden'
    mov_mannheim['location'] = 'mannheim'
    df = pd.concat([mov_berlin,mov_dresden,mov_mannheim])
    df['participant'] =  df['location'].str[0] + df.Participant.apply(lambda x: '%03d'%int(x))
    df['trigger_date'] = pd.to_datetime(df.Trigger_date + ' ' + df.Trigger_time)
    
    # Merging double IDs (for participants with several movisense IDs)
    df['participant'] = df.participant.replace(get_duplicate_mov_ids())
    
    # Removing pilot participants
    df = df[~df.Participant.astype(str).str.contains('test')]
    df = df[~df.participant.isin(['m157'])]
    
    # Adding starting dates to get sampling days
    def get_starting_dates(path, pp_prefix = ''):
        soup = bs(open(path).read())
        ids = [int(x.text) for x in soup.find_all("td", class_ = 'simpleId')]
        c_dates = [x.find_all("span")[0]['title'] for x in soup.find_all("td", class_ = 'coupleDate')]
        s_dates = [x['value'] for x in soup.find_all("input", class_ = 'dp startDate')]
        df = pd.DataFrame({'participant':ids,'coupling_date':c_dates,'starting_date':s_dates})
        df['coupling_date'] = pd.to_datetime(df.coupling_date)
        df['starting_date'] = pd.to_datetime(df.starting_date)
        df.starting_date.fillna(df.coupling_date,inplace = True)
        df['participant'] = pp_prefix + df.participant.apply(lambda x: '%03d'%int(x))
        return df
    
    starting_dates = pd.concat([
    get_starting_dates(os.path.join(get_raw(), "starting_dates_b.html"), 'b'),
    get_starting_dates(os.path.join(get_raw(), "starting_dates_d.html"), 'd'),
    get_starting_dates(os.path.join(get_raw(), "starting_dates_m.html"), 'm')
    ])
    # For participants with several movisense IDs we use the first coupling date
    starting_dates.participant.replace(get_duplicate_mov_ids(), inplace = True)
    starting_dates = starting_dates.groupby('participant')[['starting_date','coupling_date']].min().reset_index()
    df = df.merge(starting_dates, on="participant", how = 'left', indicator = True)
    # Checking if starting dates were downloaded
    if "left_only" in df._merge.unique():
        no_starting_dates = df.query('_merge == "left_only"').participant.unique()
        print("Starting dates missing for participants below.  Did you download the participant overviews as html?", no_starting_dates)
    # Calculating movisense sampling day, adding date and end_date
    df['sampling_day'] = (df['trigger_date'] - df['starting_date']).dt.days + 1
    df['date'] = df.trigger_date.dt.date
    df['end_date'] = df.date + pd.DateOffset(days = 365)
    df.index.rename('mov_index',inplace = True)
    return df


@get_efficiently
def get_two_day_data():
    """Gets two-day which are a subset of mov_data
    1) We select two-day forms and turn the dataframe into one row per participant-date (Form repetitions on the same day are removed)
    2) We reduce all drinking questions to an easily readable dictionary of drink amounts.
    3) We add missing data for dates on which we did not receive answers (starting 2 days before starting date up to 365 days after)
    4) We shift answers from retrospective drinking questions backwards to the adequate date (e.g. one day back for yesterday questions) 
    """
    mov_data = get_mov_data().reset_index()
    drinking_columns = [c for c in mov_data.columns if c.startswith("Anzahl") and "10day" not in c]
    mdbf_columns = [c for c in mov_data.columns if "MDBF" in c and "INT" not in c]
    two_day_columns = ['mov_index','starting_date','end_date','sampling_day'] + drinking_columns + mdbf_columns + ['soziale_isolation','alternative_rewards','craving','Limit','Kontrolle']
    # 1) Turning df into one line per date
    two_day_forms = ["Coverage","Soziale Isolation","Craving","MDBF","Alternative Rewards","Limits & Control"]
    df = mov_data.sort_values(by=['participant','trigger_date','Form','Trigger_counter'])
    df = df[df.Form.isin(two_day_forms)].groupby(["participant","date"])[two_day_columns].first().dropna(how='all').reset_index()
    # 2) Turning drinking answers into dictionaries
    df[drinking_columns].fillna(0,inplace = True)
    df['drinks_gestern'] = df[[c for c in drinking_columns if "vorgestern" not in c]].fillna(0).agg(lambda x: x.to_dict(), axis=1)
    df['drinks_vorgestern'] = df[[c for c in drinking_columns if "vorgestern" in c]].fillna(0).agg(lambda x: x.to_dict(), axis=1)
    # Adding missing values
    def add_missing_data(df):
        dates = pd.date_range(df.starting_date.iloc[0]-pd.DateOffset(days = 2), df.end_date.iloc[0])
        df = df.reindex(dates)
        df.index.names = ['date']
        df[['starting_date','sampling_day']] = df[['starting_date','sampling_day']].bfill().ffill()
        return df
    df = df.set_index('date').groupby('participant').apply(add_missing_data).drop(columns='participant').reset_index()
    
    # 3) Shifting back retrospective answers
    df['drinks'] = df['drinks_gestern'].shift(-1) # Drinks yesterday get shifted back one day
    df['drinks'].fillna(df['drinks_vorgestern'].shift(-2), inplace = True) # Drinks before yesterday shift back two days
    df['limit'] = df.Limit.ffill(limit=8) # Limit gets repeated forward for eight days
    df['control'] = df.Kontrolle.bfill(limit=8) # Control is repeated backward for eight days
    # 4) Calculating daily alcohol consumption in grams
    alc_dict = {"Anzahl"+k:v for k,v in get_alcohol_per_drink().set_index('drink')['ml_alc_per_drink'].to_dict().items()}
    def calculate_g_alc(x):
        if x != x:
            ml_alc = np.nan
        else:
            ml_alc = 0
            for k,v in x.items():
                if v > 0:
                    ml_alc += alc_dict[k.split('_')[0]] * v
        return ml_alc * .8
    df['g_alc']  = df.drinks.apply(calculate_g_alc)
    # Returning relevant columns only
    df = df.reset_index()
    df.index.rename('two_day_index',inplace = True)
    return df[['mov_index','participant','starting_date','date','sampling_day'] + mdbf_columns + ['soziale_isolation','alternative_rewards','craving','limit','control','drinks','g_alc']]

def decode_gbe_string(s):
    """This helper function turns gbe output strings into dataframes"""
    columns, df = s.replace('","',';').replace('"','').split('\n')
    df = pd.DataFrame([column.split(',') for column in df.split(';')][:-1]).transpose().ffill().iloc[:-1]
    df.columns = [c.replace('tr_','') for c in columns.split(',')[:-1]]
    return df

def decode_gbe_strings(df, column):
    '''Turning df into trial-level df based on GBE strings.
    '''
    gbe_data = pd.concat(df.set_index(['participant','baseline_session'])[column].apply(decode_gbe_string).values, keys = df.index)
    gbe_data.index.rename('trial_index',level = 1, inplace = True)
    df = pd.merge(left=df, right=gbe_data.reset_index(level=1), left_index = True, right_index = True).reset_index()
    df['trial_index'] = df.trial_index + 1 # Making the trial index one-based
    return df


#@get_efficiently
def get_rtt_data(df):
    df = decode_gbe_strings(df, "RewardAndHappinessGame")
    # Calculating outcome variables
    df['trial_type'] = np.nan
    df.loc[(df.choiceamount.astype(float) < 0),'trial_type'] = 'loss'
    df.loc[(df.choiceamount.astype(float) > 0),'trial_type'] = 'win'
    df.loc[(df.choiceamount.astype(float) == 0),'trial_type'] = 'mixed'
    df['result'] = df.trialresult.replace({'1':'gain', '2': 'loss', '3':'certain'})
    df['gambled'] = df.result!='certain'
    # Making variable for split-half
    df['trial_number'] = df.groupby(['participant','baseline_session','trial_type']).cumcount()+1

    df['is_even'] = (df.trial_index+1)%2
    # Filtering variables of interest
    rtt_vars = ["timestarted", "timesubmitted", "choiceamount", "decisiontime", "happiness", "happinessstart", "happinesstime" ,"spinnerangle", "spinnerloseamount", "spinnerwinamount", "spintime", "trial_type","trialresult","gambled",'is_even']
    df = df[['mov_index','gbe_index','gbe_baseline_index','initial','trial_index','participant','baseline_session']+rtt_vars]
    return df



def decode_ssrt_string(s):
    '''This function cleans SSRT raw data
    1) We get rid of the left-right distinction
    2) We turn tr_gobaddelay ("the amount of time between the fruit going bad and the center point of the reaction window.
integer, milliseconds") into SSDs ("time at which the fruit turns bad relative to onset of the start of the fall"), by subtracting it from the time it takes for the fruit to reach the center of the response window (650 ms).
    '''
    df = decode_gbe_string(s)
    # Removing left/right distinctions
    df['rt'] = df.lefttime.astype(int) + df.righttime.astype(int)
    df['is_stop'] = (df.stop.astype(int) > 0).astype(float)
    df.loc[df.rt==0,'rt'] = np.nan # Setting 0 RTs to nan
    df['responded'] = (df.rt.isna()==False).astype(float)
    # Calculating SSD
    crw = 650 # ToDo: I'll have to double check this is correct; in Smittenaar it's reported as 500ms, but Ying used 650ms
    df['ssd'] = crw - df.gobaddelay.astype(int)
    df.loc[df.is_stop==False,'ssd'] = np.nan
    # Error analysis
    df['omission'] = ((df.is_stop==0) & ((df.rt.isna()) | (df.rt >= 800))).astype(float)
    df['comission'] = ((df.is_stop==1) & (df.rt.isna()==False)).astype(float)
    df['premature'] = (df.rt <= 500).astype(float)
    # Creating convenience variables and restructuring
    df['accuracy'] = df.success.astype(int)
    df = df[[
        'anticipation',
        'is_stop','ssd',
        'responded',
        'rt',
        'accuracy',
        'omission',
        'comission',
        'premature']]
    return df

def get_ssrt_data(df):
    '''Turning df into trial-level df based on GBE strings.
    '''
    gbe_data = pd.concat(df.set_index(['participant','baseline_session'])['FruitTapGame'].apply(decode_ssrt_string).values, keys = df.index)
    gbe_data.index.rename('trial_index',level = 1, inplace = True)
    df = pd.merge(left=df, right=gbe_data.reset_index(level=1), left_index = True, right_index = True).reset_index()
    df['trial_index'] = df.trial_index + 1 # Making the trial index one-based
    return df

@get_efficiently
def get_initial_ssrt_data():
    '''ToDo: This should be named get_initial_baseline_ssrt_data'''
    df = get_gbe_baseline_data() # ToDo: add sample variable ("initial" vs. "replication")
    df = df[df.initial] # For now, we only look at the initial dataset
    df = df[df['FruitTapGame'].isnull()==False]
    return get_ssrt_data(df)

@get_efficiently
def get_initial_rtt_data():
    df = get_gbe_baseline_data() # ToDo: add sample variable ("initial" vs. "replication")
    df = df[df.initial] # For now, we only look at the initial dataset
    df = df[df['RewardAndHappinessGame'].isnull()==False]
    return get_rtt_data(df)

def get_phone_codebook():
    tables = pd.read_html(open('../data/raw/phone_codebook.html','r').read())
    df = tables[1]
    # Note that str.contains fills NaN values with nan, which can lead to strange results during filtering
    df = df[df.LabelHinweistext.str.contains('Fragebogen:',na=False)==False]
    df = df.set_index('#')
    # Parsing variable name
    df['variable'] = df["Variable / Feldname"].apply(lambda x: x.split(' ')[0])
    # Parsing condition under which variable is displayed
    df['condition'] = df["Variable / Feldname"].apply(lambda x: ' '.join(x.split(' ')[1:]).strip() if len(x.split(' '))>1 else '')
    df['condition'] = df.condition.apply(lambda x: x.replace('Zeige das Feld nur wenn:  ',''))
    # Parsing labels for numerical data
    df['labels'] = np.nan
    labels = tables[2:-1]
    try:
        labels = [dict(zip(l[0],l[1])) for l in labels]
    except:
        display(table)
    searchfor = ["radio","dropdown","yesno","checkbox"]
    with_table = df['Feld Attribute (Feld-Typ, Pr??fung, Auswahlen, Verzweigungslogik, Berechnungen, usw.)'].str.contains('|'.join(searchfor))
    df.loc[with_table,'labels'] = labels
    df = df.astype(str)
    return df

def determine_phone_b07(df):
    # Some initial fixes
    df.loc[df.center=='d','screen_caller'] = df.loc[df.center=='d','screen_caller'].str.lower().str.strip().replace('leo','leonard visser').replace('sebastian m??rcke','sebastian m??ricke').replace('jessica zimmerman','jessica zimmermann').replace('miriam-sophie petasch','miriam petasch').replace('dorothee','dorothee scheuermann')
    # Cleaning screener list
    dd_screeners = df[(df.center=='d')&(df.screen_caller.isna()==False)].screen_caller.unique()
    def clean_screeners(dd_screeners):
        dd_screeners = [y  for x in dd_screeners for y in x.split('+')]
        dd_screeners = [y  for x in dd_screeners for y in x.split(',')]
        dd_screeners = [y  for x in dd_screeners for y in x.split('und')]
        dd_screeners = [y.replace('(15.02.21)','')  for x in dd_screeners for y in x.split('/')]
        dd_screeners = [y.replace(')','').strip().lower()  for x in dd_screeners for y in x.split('(')]
        dd_screeners = sorted(list(set(dd_screeners)))
        return dd_screeners
    dd_screeners = clean_screeners(dd_screeners)
    
    b07_screeners = ['ann-kathrin stock','charlotte blum','josephine kirschgens','klara macht','borchardt','marta ledro','miriam petasch','mona hofmann','theo tester']
    s01_screeners = ['esther preuschhof', 'miriam schmitz', 'sebastian m??ricke', 'jessica zimmermann', 'leonard visser', 'anna-lena l??nert', 'anne d??rfler', 'dominic reichert', 'maike borchardt', 'dorothee scheuermann', 'paula b??hlmann', 'alice']
    known_dd_screeners = list(b07_screeners+s01_screeners)
    dd_screeners = df[(df.center=='d')&(df.screen_caller.isna()==False)].screen_caller.unique()
    # Checking if all Dresden phone screeners are accounted for
    assert df[(df.center=='d')&(df.screen_caller)].screen_caller.str.contains('|'.join(known_dd_screeners)).mean()==1, "Unknown Dresden phone screener: %s"%', '.join(set(clean_screeners(dd_screeners))-set(known_dd_screeners))
    # In general, if a screener from a project was involved, it was screened for that project
    df['screened_for_b07'] = (df.center=='d') & (df.screen_caller.str.contains('|'.join(b07_screeners)))
    df['screened_for_s01'] = (df.center!='d') | (df.screen_caller.str.contains('|'.join(s01_screeners)))
    
    # We also exclude participants screened for C02 in Berlin
    df.loc[(df.screen_purpose == 4) & (df.center=='b'), 'screened_for_s01'] = False
    
    # Additionally, we also set it to true if it was specifically set
    df.loc[df.screen_site_dd == 1, 'screened_for_s01'] = True
    df.loc[df.screen_site_dd == 3, 'screened_for_s01'] = True
    df.loc[df.screen_site_dd == 2, 'screened_for_b07'] = True
    df.loc[df.screen_site_dd == 3, 'screened_for_b07'] = True
    return df

def load_phone_data():
    df = pd.read_csv('../data/raw/phonescreening.csv',
                     na_values = ["A 'MySQL server has gone away' error was detected.  It is possible that there was an actual database issue, but it is more likely that REDCap detected this request as a duplicate and killed it."]
                    )
    remove = ['050571', '307493', '345678', '715736', 'Ihloff', 'test',
       'test002', 'test003', 'test004', 'test005', 'test01', 'test02',
       'test03', 'test0722', 'test1', 'test34', 'test999', 'test2020',
       'test20201', 'test345345', 'testt', 'test_10', 'test_11_26',
       'test_neu', 'xx956']
    df = df[~df.participant_id.astype(str).isin(remove)]
    bad_ids = df[~df.participant_id.apply(check_participant_id)].participant_id.unique()
    assert len(bad_ids)==0, "Bad participant IDs (should be added to remove): %s"%', '.join(["'%s'"%b for b in bad_ids])
    df = set_dtypes(df, get_phone_codebook())
    df['participant_id'] = df.participant_id.astype(int)
    df['center'] = df.screen_site.replace({1:'b',2:'d',3:'m'})
    df['screen_date'] = pd.to_datetime(df['screen_date'], errors = 'coerce')
    #display(df[df.screen_caller.isna()])
    df = determine_phone_b07(df)    
    return df