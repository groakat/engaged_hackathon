import os
import inspect 

def getAccountKey():
    try:

        filename = os.path.join(os.path.dirname(
                                inspect.getfile(inspect.currentframe())),
                                'azure_key.azkey')
        with open(filename, 'r') as f:
            key = f.readlines()
            
        return key[0]
    except OSError:
        raise OSError("You do not have a azure_key file in your repository. For security reasons, \n" +
                      "this file is not included in the git repository. You can request it from \n" +
                      "Alison or Peter. The file has to be in 'engaged/core/'")
        