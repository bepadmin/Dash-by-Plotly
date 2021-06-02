# -*- coding: utf-8 -*-
"""
Created on Thu May 27 13:04:40 2021

@author: wlim
"""

import pathlib
import os 
# get relative data folder
project = "ucdavis"
#PATH = pathlib.Path(__file__).stem
PATH = pathlib.Path(__file__).parent
#DATA_PATH = PATH.joinpath("../webids/ucdavis").resolve()
print(DATA_PATH)
file_name = os.path.basename(__file__)
webids = pd.read_csv(DATA_PATH.joinpath("webid.csv"),header = 0)


from pilibrary import pi_client
pi = pi_client(config='pi_config.ini')

LiftID = "UC Davis CHCPC Plant BCH-1 Lift"
percentLoadID = "UC Davis CHCPC Plant BCH-1 %Tons"
kWperTonID = "UC Davis CHCPC Plant BCH-1 kW/Ton"
ChillerStatusID = "UC Davis CHCPC Plant BCH-1 Lift"



LiftID = pi.generate_webid_from_name(LiftID)
percentLoadID = pi.generate_webid_from_name(LiftID)
kWperTonID = pi.generate_webid_from_name(LiftID)
ChillerStatusID = pi.generate_webid_from_name(LiftID)
