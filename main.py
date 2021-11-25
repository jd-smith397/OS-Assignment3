import sys as sys
import csv
import simulator as simu


#Utility function built to output the resulting data to a csv for plotting
def export_results(replacement_alg: str, result_list: list):

    #Each int must be enclosed in its own list for writerows to correctly write list to file
    formatted_list = map(lambda x: [x], result_list)

    with open(f'{replacement_alg}_Page_Replacement.csv', 'w', newline = '') as csvfile:
        my_writer = csv.writer(csvfile, delimiter = ' ')
        my_writer.writerows(formatted_list)

def export_results(result_list: list):
    with open('Page_Replacement.csv', 'w', newline = '') as csvfile:
        my_writer = csv.writer(csvfile)
        my_writer.writerow(['FIFO', 'LRU', 'OPT'])
        my_writer.writerows(result_list)

#Where the block of operating code goes
def main():
    #Case where random seed is given in command line args for one simulation
    if len(sys.argv) == 4:
        num_frames = int(sys.argv[1])
        replacement_alg = int(sys.argv[2])
        seed = int(sys.argv[3])

        sim = simu.Simulator(num_frames, replacement_alg, rand_seed= seed)
        sim.run()
        sim.print_report()
    #Case where default seed is used for one simulation
    elif len(sys.argv) == 3:
        num_frames = int(sys.argv[1])
        replacement_alg = int(sys.argv[2])

        sim = simu.Simulator(num_frames, replacement_alg)
        sim.run()
        sim.print_report()
    #Case where no command line args given, used by me to run multiple simulations
    #And output the data to a .csv file
    #Default random seed used
    elif len(sys.argv) == 1:
        results = []
        for i in range(1, 31):
            temp = []
            for j in range(1, 4):
                sim = simu.Simulator(i, j)
                sim.run()
                temp.append(sim.page_faults)
            results.append(temp)
        export_results(results)    
    else:
        print("Error, not correct number of command line arguments")

#Entry point when not imported as a module
if(__name__ == "__main__"):
    main()

