from csp2 import get_solutions


import multiprocessing
import time
def main():
    find_all_solutions = False
    n_processes = 2**2#same as number of shards
    threads_per_shard=2
    #WARNING: FIND_ALL_SOLUTIONS IS INCOMPATIBLE WITH THREADS_PER_SHARD>1
    #IF WANT ALL SOLUTIONS, USE SHARDING WITH MULTIPLE PROCESSES
    #IF WANT ONE SOLUTION, USE 1 SHARD WITH MULTIPLE THREADS
    
    processes = []

    for shard_index in range(n_processes):
        process = multiprocessing.Process(target=get_solutions, args=(shard_index, n_processes,threads_per_shard,find_all_solutions))
        processes.append(process)
        process.start()
        
    
    for process in processes:
        process.join()
        

if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()

    print("DONE")
    print(f"Function took {end_time - start_time:.2f} seconds to run.")


    #======SHUFFLING========
    #Function took 119.93 seconds to run.