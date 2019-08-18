# main

import runner.runner as run
import sys

if __name__ == '__main__':
    year = int(sys.argv[1])
    #year =2018
    program = run.Runner(year)
    program.run()


