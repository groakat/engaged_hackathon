
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








































