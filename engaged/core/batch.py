import glob

def loop(folder, pattern, meta, func_key, func_list):
    """
    folder (string):
        folder with input files
    pattern (string):
        glob pattern
    meta (dict):
        meta data to initialize AzurePipeline
    func_key (string):
        name of function with 'in_filename' that is changed dynamically
        by looping over the files in `folder`
    func_list (list(func_ptr)):
        functions to be applied to the AzurePipeline
    
    """
    files = glob.glob(folder + '/' + pattern)
    
    for f in files:
        tmp_meta = meta
        tmp_meta[func_key]['in_filename'] = f
        
        ap = AP.AzurePipeline(tmp_meta)
        
        print tmp_meta
        
        for func in func_list:
            ap.apply(func)
        