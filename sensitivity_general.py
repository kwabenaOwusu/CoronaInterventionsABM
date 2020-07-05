#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
simulations for sensitivity to results
Author: Kwabena Afriyie Owusu
Date: May, 2020
"""

import csv
import time as mytime

############################################ENVIRONMENT###################################################################################

exec(open('./environment.py').read()) # execute the environment script


####################################################### STANDARD (MARKET)#############################################################################

numsim = 4 # number of years of simulations
start_time=mytime.time() # set time for starting

risk_life = 0.5 #  risk level by moving outside
social_radius = 2 # social radius within which interaction is possible
eff_quarantined = 0.25 # efficiency of contact tracing symptomatic for treatments at hospitals
hospital_capacity = 0.5 # the capacity of the hospitals (in reference to the general population)
essentials_move = 8 # move out only for essentials

exec(open('./market_modules.py').read()) # execute the main script
    
outfname = 'sim_standard_market.csv'
with open(outfname,'w') as outfile:
    allsimdat=csv.writer(outfile)
    for rep in range(numsim):
        exec(open('./loop_modules.py').read())
        with open('./simulation_data.csv', 'r') as csvfile:
            onesimdat = csv.reader(csvfile, delimiter=',')
            header = next(onesimdat)
            header.append('NoSim')
            if rep==0:
                allsimdat.writerow(header)
            for row in onesimdat:
                row.append(str(rep))
                allsimdat.writerow(row)
        print('Done, simulation %i, with standard paramaters, ended at %.4f hours '%(rep+1,(mytime.time()-start_time)/3600. ))
        #os.rename('sim_movie.mp4', 'movie_standard_market_rep_%i.mp4' %(rep+1) ) 
             

####################################################### STANDARD (MARKET) WITH MASK #############################################################################

numsim = 4 # number of years of simulations
start_time=mytime.time() # set time for starting

risk_life = 0.5 #  risk level by moving outside
social_radius = 2 # social radius within which interaction is possible
eff_quarantined = 0.25 # efficiency of contact tracing symptomatic for treatments at hospitals
hospital_capacity = 0.5 # the capacity of the hospitals (in reference to the general population)
essentials_move = 8 # move out only for essentials
wearing_mask = 0.5 # prob of wearing mask 

exec(open('./market_mask_modules.py').read()) # execute the main script
    
outfname = 'sim_standard_market.csv'
with open(outfname,'w') as outfile:
    allsimdat=csv.writer(outfile)
    for rep in range(numsim):
        exec(open('./loop_modules.py').read())
        with open('./simulation_data.csv', 'r') as csvfile:
            onesimdat = csv.reader(csvfile, delimiter=',')
            header = next(onesimdat)
            header.append('NoSim')
            if rep==0:
                allsimdat.writerow(header)
            for row in onesimdat:
                row.append(str(rep))
                allsimdat.writerow(row)
        print('Done, simulation %i, with standard paramaters, ended at %.4f hours '%(rep+1,(mytime.time()-start_time)/3600. ))
        #os.rename('sim_movie.mp4', 'movie_standard_market_rep_%i.mp4' %(rep+1) ) 
             



