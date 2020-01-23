import sys

import runner.runner as run


#parameters in the config:
# enter: year False
# year is the year of the sim; needs to be 2017 when running it locally
#2nd parameter is to disable the socket data logging ie set the boolean as False
# 2017 False
if __name__ == '__main__':
    year = int(sys.argv[1])
    try:
        withSocket = eval(sys.argv[2])
    except:
        withSocket = True

    program = run.Runner(year, withSocket)
    program.run()
