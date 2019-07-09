if __name__ == "__main__":
    
    ### NATHANS RUN ###
    RUN_NAME = "run1"
    
    import os
    import yaml
    import numpy as np
    import pandas as pd
    import sqlite3 as sql
    import warnings

    import sys
    sys.path.append("../..")

    from atm.models import STM, FRM, NEATM
    from atm.obs import WISE
    from atm import modifyErrors
    from atm import multiFit
    
    # Instantiate observatory and NEATM class for simulating data
    obs = WISE()
    model = NEATM(verbose=False)
    
    # Grab observations
    con = sql.connect("/gscratch/astro/moeyensj/atm/atm/data/sample.db")
    observations = pd.read_sql("""SELECT * FROM observations""", con)
    additional = pd.read_sql("""SELECT * FROM additional""", con)
    
    # Only keep clipped observations
    observations = observations[observations["keep"] == 1]
    additional = additional[additional["obs_id"].isin(observations["obs_id"].values)]
    
    # Modify errors
    observations = modifyErrors(observations, obs, sigma=0.15)
    
    # Remove missing H value, G value objects... 
    observations = observations[~observations["designation"].isin([
       '2010 AJ104', '2010 BM69', '2010 DZ64', '2010 EL27', '2010 EW144',
       '2010 FE82', '2010 FJ48', '2010 HK10', '2010 LE80'])]
    
    # Convert phase angle to radians
    observations["alpha_rad"] = np.radians(observations["alpha_deg"])
    
    # Create data dictionary
    dataDict = {}
    dataDict[RUN_NAME] = observations.copy()
    dataDict[RUN_NAME]["eps_W3W4"] = np.ones(len(observations)) * 0.9 
    
    # Create fit dictionary
    fitDict = {}
    fitDict[RUN_NAME] = {
        "fitParameters" : ["logT1", "logD", "eps_W1W2"],
        "emissivitySpecification" : {
                    "eps_W1W2" : ["W1","W2"],
                    "eps_W3W4" : ["W3","W4"]},
        "albedoSpecification": "auto",
        "fitFilters" : "all",
        "columnMapping" : {
                    "obs_id" : "obs_id",
                    "designation" : "designation",
                    "exp_mjd" : "mjd",
                    "r_au" : "r_au",
                    "delta_au" : "delta_au",
                    "alpha_rad" : "alpha_rad",
                    "eps" : ["eps_W3W4"],
                    "p" : None,
                    "G" : "G",
                    "logT1" : None,
                    "logD" : None,
                    "flux_si" : ["flux_W1_si", "flux_W2_si", "flux_W3_si", "flux_W4_si"],
                    "fluxErr_si" : ["fluxErr_W1_si", "fluxErr_W2_si", "fluxErr_W3_si", "fluxErr_W4_si"],
                    "mag" : ["mag_W1", "mag_W2", "mag_W3", "mag_W4"],
                    "magErr" : ["magErr_W1", "magErr_W2", "magErr_W3", "magErr_W4"]
        }
    }
    
    # Load fit configuration
    with open("config.yml", 'r') as stream:
        fitConfig = yaml.load(stream, Loader=yaml.FullLoader)
    runDir = fitConfig["runDir"]
    fitConfig.pop("runDir")

    summary, model_observations = multiFit(model, obs, dataDict, fitDict, fitConfig,
                                           saveDir=os.path.join(runDir, "{}".format(RUN_NAME))
                                           )