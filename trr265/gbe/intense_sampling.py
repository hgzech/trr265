# AUTOGENERATED! DO NOT EDIT! File to edit: notebooks/24_gbe.rtt.intense_sampling.ipynb (unless otherwise specified).

__all__ = ['get_intense_drinking_data']

# Cell
from .sst.data_provider import SSTDataProvider
import pandas as pd
import numpy as np
from scipy import stats
import biuR.wrapper

# Cell
def get_intense_drinking_data():

    change_dict = {'AnzahlKleinesBier': 'kleinesBier',
 'AnzahlMittlereBier': 'mittleresBier',
 'AnzahlGrosseBier': 'grossesBier',
 'AnzahlKleinerWeisswein': 'kleinerWeisswein',
 'AnzahlMittlererWeisswein': 'mittlererWeisswein',
 'AnzahlFlascheWeisswein': 'FlascheWeisswein',
 'AnzahlKleinerRotwein': 'kleinerRotwein',
 'AnzahlMittlererRotwein': 'mittlereRotwein',
 'AnzahlFlaschenRotwein': 'FlascheRotwein',
 'AnzahlSekt': 'Sekt',
 'AnzahlFlaschenSekt': 'FlascheSekt',
 'AnzahlLikoerWein': 'Likoer-Wein',
 'AnzahlKleineLikoer': 'kleinerLikoer',
 'AnzahlGrosseLikoer': 'grosserLikoer',
 'AnzahlLikoerSuess': 'LikoerSuess',
 'AnzahlKleineSpirituosen': 'kleineSpirituosen',
 'AnzahlGrosseSpirituosen': 'grosseSpirituosen',
 'AnzahlSpirituosen100ml': 'Spirituose',
 'AnzahlSpirituosenStark': 'SpirituoseStark'}

    alc_dict = {"Anzahl"+k:v for k,v in dp.get_alcohol_per_drink().set_index('drink')['ml_alc_per_drink'].to_dict().items()}
    alc_dict_1 = dict(("INT_"+change_dict[key], value) for (key, value) in alc_dict.items())
    alc_dict_1['INT_Weinbrand'] = 7.2

    alc_dict_2 = dict(("INT_Morgenabfr_"+change_dict[key]+'_gesternAbend', value) for (key, value) in alc_dict.items())
    alc_dict_2['INT_Morgenabfr_Weinbrand_gesternAbend'] = 7.2
    alc_dict = {**alc_dict_1, **alc_dict_2}

    change_dict2 = {
'INT_Morgenabfr_kleinerLikoer_gesternAbend':'INT_Morgenabfr_Likoerklein_gesternAbend',
 'INT_Morgenabfr_kleineSpirituosen_gesternAbend':'INT_Morgenabfr_kleineSpirituose_gesternAbend',
 'INT_Morgenabfr_grosseSpirituosen_gesternAbend':'INT_Morgenabfr_grosseSpirituose_gesternAbend',
 'INT_Morgenabfr_Likoer-Wein_gesternAbend':'INT_Morgenabfr_LikoerWein_gesternAbend',
 'INT_Morgenabfr_LikoerSuess_gesternAbend':'INT_Morgenabfr_Likoersuess_gesternAbend',
 'INT_Morgenabfr_SpirituoseStark_gesternAbend':'INT_Morgenabfr_kleineSpirituoseStark_gesternAbend',
 'INT_Morgenabfr_mittlereRotwein_gesternAbend':'INT_Morgenabfr_mittlererRotwein_gesternAbend',
 'INT_Morgenabfr_grosserLikoer_gesternAbend':'INT_Morgenabfr_Likoergross_gesternAbend'}

    alc_dict = dict((change_dict2[key] if key in change_dict2 else key, value) for (key, value) in alc_dict.items())

    mov_data = dp.get_mov_data().reset_index()
    drinking_columns = list(alc_dict.keys())#[c for c in mov_data.columns if c.startswith("INT_")]
    two_day_columns = ['mov_index','starting_date','end_date','sampling_day'] + drinking_columns
    # 1) Turning df into one line per date
    two_day_forms = ["Intense_Morgenabfrage","Intense_Tagesabfrage"]
    df = mov_data.sort_values(by=['participant','trigger_date','Form','Trigger_counter'])
    df = df[df.Form.isin(two_day_forms)].groupby(["participant","date"])[two_day_columns].first().dropna(how='all').reset_index()
    # 2) Turning drinking answers into dictionaries
    df[drinking_columns].fillna(0,inplace = True)
    df['drinks_heute'] = df[[c for c in drinking_columns if "gestern" not in c]].fillna(0).agg(lambda x: x.to_dict(), axis=1)
    df['drinks_gestern'] = df[[c for c in drinking_columns if "gestern" in c]].fillna(0).agg(lambda x: x.to_dict(), axis=1)
    # Adding missing values

    # TODO
    #def add_missing_data(df):
    #    dates = pd.date_range(df.starting_date.iloc[0]-pd.DateOffset(days = 2), df.end_date.iloc[0])
    #    df = df.reindex(dates)
    #    df.index.names = ['date']
    #    df[['starting_date','sampling_day']] = df[['starting_date','sampling_day']].bfill().ffill()
    #    return df
    #df = df.set_index('date').groupby('participant').apply(add_missing_data).drop(columns='participant').reset_index()

    # 3) Shifting back retrospective answers
    df['drinks_1'] = df['drinks_heute']
    df['drinks_2'] = df['drinks_gestern'].shift(-1) # Drinks yesterday shift back one days
    def combine_dicts(drinks_1, drinks_2):
        if type(drinks_2)!=dict:
            return drinks_1
        else:
            d = {**drinks_1, **drinks_2}


        return d
    df['drinks'] = df.apply(lambda x: combine_dicts(x.drinks_1, x.drinks_2), axis=1)

    # 4) Calculating daily alcohol consumption in grams
    #alc_dict = {"Anzahl"+k:v for k,v in self.get_alcohol_per_drink().set_index('drink')['ml_alc_per_drink'].to_dict().items()}
    def calculate_g_alc(x):
        if x != x:
            ml_alc = np.nan
        else:
            ml_alc = 0
            for k,v in x.items():
                if v > 0:
                    ml_alc += alc_dict[k]*v#.split('_')[0]] * v
        return ml_alc * .8
    df['g_alc']  = df.drinks.apply(calculate_g_alc)
    # Returning relevant columns only
    df = df.reset_index()
    df['sampling_day'] = df.groupby('participant').starting_date.cumcount() + 1
    df.index.rename('intense_index',inplace = True)
    return df[['mov_index','participant','starting_date','date','sampling_day','g_alc']]
_df = get_intense_drinking_data()