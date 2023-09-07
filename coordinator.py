from csp2 import get_solutions


import multiprocessing
import time
def main():
    n_processes = 2**5
    
    processes = []

    for index in range(n_processes):
        process = multiprocessing.Process(target=get_solutions, args=(index, n_processes))
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