from csp import get_solutions


import multiprocessing

def main():
    n_processes = 8
    
    # Creating a shared list to store the result
    result = multiprocessing.Array('i', n_processes)
    
    processes = []

    for index in range(n_processes):
        process = multiprocessing.Process(target=get_solutions, args=(index, n_processes))
        processes.append(process)
        process.start()
    
    for process in processes:
        process.join()
        

if __name__ == "__main__":
    main()
    print("DONE")