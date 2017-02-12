from multiprocessing import Process
import argparse
import datetime
import time

import config
import main as algorithm
import eval

DEFAULT_NB_PARALLEL_EXECUTIONS = 1
DEFAULT_NB_EXECUTIONS_PER_GRID_SIZE = 4

processes_pool = []
running_processes_pool = []
resolution_time_records = []

def parse_arguments():
    parser = argparse.ArgumentParser(description='Eternity II algortihm benchmarking')
    parser.add_argument('--nb-parallel-executions', type=int,
                        default=DEFAULT_NB_PARALLEL_EXECUTIONS,
                        help='Number of parallel executions at the same time')
    parser.add_argument('--nb-executions-per-grid-size', type=int,
                        default=DEFAULT_NB_EXECUTIONS_PER_GRID_SIZE,
                        help='Number of algorithm executions per grid size')
    return parser.parse_args()

def prepare_grid_benchmark(input_grid, nb_executions):
    for i in range(nb_executions):
        process = Process(target=algorithm.main, args=(False,))
        processes_pool.append((process, input_grid))

def record_process_start():
    resolution_time_records.append(datetime.datetime.now())

def record_process_end(process_index):
    current_time = datetime.datetime.now()
    start_time = resolution_time_records[process_index]
    resolution_time = current_time - start_time
    resolution_time_records[process_index] = resolution_time
    print process_index, "\t|", processes_pool[process_index][1], "\t| resolution time:", resolution_time_records[process_index]

def find_ended_processes(nb_current_executions):
    for process_index in running_processes_pool:
        if not processes_pool[process_index][0].is_alive():
            record_process_end(process_index)
            nb_current_executions -= 1
            running_processes_pool.remove(process_index)
    return nb_current_executions

def launch_benchmark(nb_executions):
    nb_current_executions = 0
    for i, process_data in enumerate(processes_pool):
        process = process_data[0]
        process_config = process_data[1]
        while nb_current_executions == nb_executions:
            nb_current_executions = find_ended_processes(nb_current_executions)
            time.sleep(0.01)

        config.population_file_base = process_config
        config.init()
        eval.init_virgin_scores_list()

        running_processes_pool.append(i)
        process.start()
        record_process_start()
        nb_current_executions += 1

    while nb_current_executions != 0:
        nb_current_executions = find_ended_processes(nb_current_executions)
        time.sleep(0.01)

def main(args):
    print "nb_parallel_executions", args.nb_parallel_executions
    print "nb_executions_per_grid_size", args.nb_executions_per_grid_size
    prepare_grid_benchmark("test_4pieces.txt", args.nb_executions_per_grid_size)
    # our algorithm currently does not solve 3x3 puzzle
    # prepare_grid_benchmark("test_9pieces.txt", args.nb_executions_per_grid_size)
    launch_benchmark(args.nb_parallel_executions)

if __name__ == '__main__':
    args = parse_arguments()
    main(args)
