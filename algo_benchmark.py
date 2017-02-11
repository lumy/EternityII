import argparse

DEFAULT_NB_PARALLEL_EXECUTIONS = 1
DEFAULT_NB_EXECUTIONS_PER_GRID_SIZE = 4

def parse_arguments():
    parser = argparse.ArgumentParser(description='Eternity II algortihm benchmarking')
    parser.add_argument('--nb-parallel-executions', type=int,
                        default=DEFAULT_NB_PARALLEL_EXECUTIONS,
                        help='Number of parallel executions at the same time')
    parser.add_argument('--nb-executions-per-grid-size', type=int,
                        default=DEFAULT_NB_EXECUTIONS_PER_GRID_SIZE,
                        help='Number of algorithm executions per grid size')
    return parser.parse_args()

def main():
    args = parse_arguments()
    print "nb_parallel_executions", args.nb_parallel_executions
    print "nb_executions_per_grid_size", args.nb_executions_per_grid_size

if __name__ == '__main__':
    main()
