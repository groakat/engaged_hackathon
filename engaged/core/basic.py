def merge_two_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z

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

    new_meta = {'out_filename': out_filename}
    d = merge_two_dicts(meta.to_dict(), new_meta)
    meta = pd.DataFrame(d)

    return df, meta
