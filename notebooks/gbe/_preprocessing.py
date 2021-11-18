import wp1.data_provider as dp
import random
import numpy as np

    
@dp.get_efficiently
def get_initial_filtered_wm_data():
    '''This function preprocesses the working memory data.
    Note that this function already filters out participants that failed level 2 on any condition and participants that completed the wrong game.
    '''
    df = dp.get_gbe_baseline_data() # ToDo: add sample variable ("initial" vs. "replication")
    df = df[df.initial] # For now, we only look at the initial dataset
    df = df[df['WorkingMemoryGame'].isnull()==False]
    df = dp.decode_gbe_strings(df, "WorkingMemoryGame")
    df['success'] = df.success.astype(int)
    specs = get_wm_trial_specifications()
    df = df.merge(specs,on='trialid',validate='many_to_one').sort_values(by=['participant','baseline_session','trial_index']).reset_index(drop = True)
    df['trial_number'] = df.groupby(['participant','baseline_session','type']).cumcount()+1
    df['is_even'] = (df.trial_number+1)%2
    ## Filtering variables of interest
    wm_vars = ["timestarted", "timesubmitted", "success", "timetaken", "trialid","trial_number", "trialrot","is_even","pattern","level","type","boards"]
    df = df[['mov_index','gbe_index','gbe_baseline_index','initial','trial_index','participant','baseline_session']+wm_vars]
    # Filtering out participants that used an old version of the GBE
    is_sequential = (df.set_index('participant')['type']=='sequential').reset_index().groupby('participant').max()
    wrong_game_pps = list(is_sequential[is_sequential.type].index)
    print("%d participants used the wrong version of the game."%len(wrong_game_pps))
    df = df[df.participant.isin(wrong_game_pps)==False]
    # Filtering out participants that failed level two
    failed_level_two = df.query("(level==2) and (success==0)").gbe_baseline_index.unique()
    print("%d sessions are excluded because participants failed on a level two trial of any condition."%len(failed_level_two))
    df = df[df.gbe_baseline_index.isin(failed_level_two)==False]
    # Fixing the duplicated no distractor condition
    df['type'] = df.type.replace({"no_distractor_1":"no_distractor","no_distractor_2":"no_distractor"})
    type_repetitions = df[df.type.str.contains('no')].groupby(['participant','baseline_session']).apply(fix_game)
    type_repetitions.index.name = ""
    df['type_repetition'] = type_repetitions['type_repetition']
    df.type_repetition.fillna("",inplace = True)
    df['type'] = df.type + df.type_repetition
    df.drop(columns = 'type_repetition', inplace = True)
    return df



def fix_game_attempt(df):
    '''This function splits the duplicated no_distractor condition into two subconditions.
    In case a trial fits in either condition, it allocates one of them randomely.
    '''
    repetitions = ["_1","_2"]
    random.shuffle(repetitions)
    df['type_repetition'] = np.nan
    level_1 = 3
    errors_1 = 0
    level_2 = 3
    errors_2 = 0
    count_1 = 0
    count_2 = 0
    for index, row in df.iterrows():
        level_1_possible, level_2_possible = True, True
        
        if (level_1 != row.level) or (errors_1 >= 2) or (count_1 == 8):
            level_1_possible = False
        if (level_2 != row.level) or (errors_2 >= 2) or (count_2 == 8):
            level_2_possible = False
            
        if (level_1_possible) and (level_2_possible):
            level_1_possible = bool(random.getrandbits(1)) # If both are possible decide randomely
            
        if level_1_possible:
            df.loc[index,'type_repetition'] = repetitions[0]
            count_1 += 1
            if row.success == 1:
                level_1 += 1
                errors_1 = 0
            else:
                errors_1 += 1
                if row.level == 3:
                    level_1 -= 1
        elif level_2_possible:
            df.loc[index,'type_repetition'] = repetitions[1]
            count_2 += 1
            if row.success == 1:
                level_2 += 1
                
            else:
                errors_2 += 1
                errors_2 = 0
                if row.level == 3:
                    level_2 -= 1
    return df



def fix_game(df):
    '''This function splits the duplicated no_distractor condition into separate conditions.
    '''
    def check_length(df):
        length_ok = (len(df.success)==8) or (df.success.iloc[-2:].sum()==0)
        return length_ok
    attempts = 0
    max_attempts = 100
    searching = True
    while searching:
        attempts += 1
        df = fix_game_attempt(df)
        length_ok = check_length(df.query('type_repetition=="_1"')) and check_length(df.query('type_repetition=="_2"'))
        types_ok = df.type_repetition.isnull().mean() == 0
        if (length_ok and types_ok) or (attempts > max_attempts):
            searching = False
    if (length_ok and types_ok):
        return df
    else:
        print('Failed to reach solution.')
        
        
@dp.get_efficiently
def get_wm_trial_specifications():
    '''This function parses WM trial types from the GBE app resources.
    '''
    types = open(os.path.join(dp.get_external(), "types.xml","r")).read()
    soup = BeautifulSoup(types, "xml")
    trials = soup.find_all('trial')
    trials_data = []
    for trial in trials:
        trial_dict = {}
        # Getting trial IDs
        trial_dict['trialid'] = str(int(trial['id']))
        # Getting board sequence
        boards = [b for b in trial.find_all('board') if b.text]
        trial_dict['boards'] = len(boards)
        # Turning board sequence into pattern (this could be useful to run crossed-random effects analyses with random trial factors)
        board_dfs = [pd.DataFrame([[c for c in r] for r in b.text.split('\n')[1:-1]]).replace('.',np.nan) for b in boards]
        pattern = board_dfs[0]
        for p in board_dfs:
            pattern = pattern.fillna(p)
        pattern.fillna('', inplace = True)
        trial_dict['pattern'] = ''.join(pattern.stack().values)
        # Determining trial level as the number of targets
        trial_dict['level'] = (pattern=='T').sum().sum()
        # Determining trial types
        distractors = (pattern=='D').sum().sum()
        delayed = len(boards)>1
        if not delayed:
            if distractors:
                trial_dict['type'] = "encoding_distractor"
            else:
                trial_dict['type'] = "no_distractor"
        else:
            if distractors:
                trial_dict['type'] = "delayed_distractor"
            else:
                trial_dict['type'] = "sequential"
        trials_data.append(trial_dict)

    df = pd.DataFrame(trials_data)
    df['level'] = df.level.astype(int)
    return df