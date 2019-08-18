import sys

import runner.runner as run

if __name__ == '__main__':
    year = int(sys.argv[1])
    program = run.Runner(year)
    program.run()
