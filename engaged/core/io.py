
def read_wav(df, meta):
    args = meta['read_wav']
    
    import scipy.io.wavfile
    import pandas as pd
    def merge_two_dicts(x, y):
        z = x.copy()
        z.update(y)
        return z
    
    sr, sound = scipy.io.wavfile.read(args['in_filename'])
    df = pd.DataFrame(sound)


    # updata meta
    new_meta = {'sampling_rate': sr}
    d = merge_two_dicts(meta.to_dict(), new_meta)
    meta = pd.DataFrame(d)


    return df, meta

def save(df, meta):
    args = meta['save']
    folder = args['out_folder']

    ##########

    import hashlib
    import os
    import pandas as pd

    file_hash = hashlib.sha256(str(meta)).hexdigest()

    out_filename = file_hash + '.csv'

    df.to_csv(os.path.join(folder, out_filename))

    ##########

    def merge_two_dicts(x, y):
        z = x.copy()
        z.update(y)
        return z

    new_meta = {'save_out' : {'out_filename': out_filename}}
    d = merge_two_dicts(meta.to_dict(), new_meta)
    meta = pd.DataFrame(d)

    return df, meta

def logger(df, meta):
    args = meta['logger']
    folder = args['out_folder']
    filename = args['filename']
    import ast
    keys = ast.literal_eval(args['keys'])

    ##########

    import hashlib
    import os
    import pandas as pd

    def get_meta_values(meta, keys):
        if len(keys) > 0:
            meta, tmp = get_meta_values(meta[keys[0]], keys[1:])

        return meta, '-'.join(keys)


    path = os.path.join(folder, filename)
    out_data = {}

    for k in keys:
        tmp_meta, key_string = get_meta_values(meta, k)

        out_data[key_string] = tmp_meta

    out_df = pd.DataFrame(out_data, index=[0])

    if os.path.exists(path):
        log_df = pd.read_csv(path, index_col=0)

        out_df = pd.concat((out_df, log_df))


    out_df.to_csv(filename)

    ############

    return df, meta


def import_local_labels(df, meta):
    """ read label of multiple (local) annotations within the file
    """
    args = meta['import_global_labels']
    csv_filename = args['csv_filename']
    wav_filename = args['wav_filename']
    expected_keys = ['Label', 'Spec_NStep', 'Spec_NWin', 
                     'Spec_x1', 'Spec_y1', 'Spec_x2', 'Spec_y2',
                     'LabelStartTime_Seconds', 'LabelEndTime_Seconds',
                     'MinimumFreq_Hz', 'MaximumFreq_Hz']    
    
    
    import pandas as pd
    
    csv_df = pd.DataFrame.from_csv(csv_filename).dropna()
    
    labels = []
    for i, line in csv_df.iterrows():
        d = {}
        for k in expected_keys:
            try:
                d[k] = line[k]
            except KeyError:
                d[k] = None

        labels += [d]
        
    labelDf = pd.DataFrame({'labels': labels})
    meta = pd.concat((meta, labelDf))
    
    return df, meta
    
    
def import_global_label(df, meta):
    """ read global (only) label of single file

    """
    args = meta['import_local_label']
    csv_filename = args['csv_filename']
    wav_filename = args['wav_filename']
    
    
    import pandas as pd
        
    csv_df = pd.read_csv(csv_filename, 
                    names=['start_time', 'label', 'None'], 
                    header=None, index_col=None)
    
       
    
    
    labelDf = pd.DataFrame({'label': csv_df.ix[wav_filename]['label']},
                           index=[0])
    meta = pd.concat((meta, labelDf))
    
    return df, meta







































