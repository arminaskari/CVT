#!/usr/bin/env python

#@file runner.py

import os
import sys
import optparse
import subprocess
import random
import pdb
import matplotlib.pyplot as plt
import math
import numpy, scipy.io
from run_init import run_setup


daq_step = 1 #time at which to record data
sim_time = 60*60 #seconds


flow_array = [[0 for i in range(4)] for j in range(int(round(sim_time/daq_step)))] #initialize 4xn array of zeros

# import python modules from $SUMO_HOME/tools directory
try:
	sys.path.append(os.path.join(os.path.dirname(os.path.realpath(
	   __file__)), '..', "tools"))
	sys.path.append(os.path.join(os.environ.get("SUMO_HOME", os.path.join(
		os.path.dirname(os.path.realpath(
	   __file__)), "..")), "tools"))
	from sumolib import checkBinary
except ImportError:
	sys.exit("please declare environment variable 'SUMO_HOME' as the root directory of your sumo installation (it should contain folders 'bin', 'tools' and 'docs')")

import traci
PORT = 8873 # the port used for communicating with your sumo instance

# designates the phases, one for each direction and turn type, this is for intersection 13
NSGREEN = "GGGgrrrrGGGrrrr"
NSYELLOW = "yyygrrrryyyrrrr"
TURN1 = "rrrGrrrrrrrrrrr"
CLEAR1 = "rrryrrrrrrrrrrr"
WEGREEN = "rrrrGGGgrrrGGGg"
WEYELLOW = "rrrryyygrrryyyg"
TURN2 = "rrrrrrrGrrrrrrG"
CLEAR2 = "rrrrrrryrrrrrry"

# An example of a potential program, total length of 18, 3 seconds each
# NS pass goes during i=0-9 and WE pass goes during i=16-33
PROGRAM = [NSGREEN, NSGREEN, NSGREEN, NSGREEN, NSGREEN, NSGREEN, NSGREEN, NSGREEN, NSGREEN, NSGREEN,
	NSYELLOW, TURN1, TURN1, TURN1, TURN1, CLEAR1, 
	WEGREEN, WEGREEN, WEGREEN, WEGREEN, WEGREEN, WEGREEN, WEGREEN, WEGREEN, WEGREEN, WEGREEN, 
	WEGREEN, WEGREEN, WEGREEN, WEGREEN, WEGREEN, WEGREEN, WEGREEN, WEGREEN, 
	WEYELLOW, TURN2, TURN2, TURN2, CLEAR2]

# Runs the simulation, and allows you to change traffic phase


def get_options():
	optParser = optparse.OptionParser()
	optParser.add_option("--nogui", action="store_true",
						 default=False, help="run the commandline version of sumo")
	options, args = optParser.parse_args()
	return options


# this is the main entry point of this script
if __name__ == "__main__":
	options = get_options()

	# this script has been called from the command line. It will start sumo as a
	# server, then connect and run
	if options.nogui:
		sumoBinary = checkBinary('sumo')
	else:
		sumoBinary = checkBinary('sumo-gui')

	# this is the normal way of using traci. sumo is started as a
	# subprocess and then the python script connects and runs
	sumoProcess = subprocess.Popen([sumoBinary, "-c", "huntcol_network/huntcol.sumocfg", "--step-length", "1.0", "--tripinfo-output",
									"tripinfo.xml", "--remote-port", str(PORT)], stdout=sys.stdout, stderr=sys.stderr)
	run()
	sumoProcess.wait()

	'''
	plt.plot(flow_array)
	plt.xlabel('Time mod ' + str(daq_step))
	plt.show()
	'''
	scipy.io.savemat('100percent.mat',mdict={'flow_array':flow_array})
	#pdb.set_trace()
