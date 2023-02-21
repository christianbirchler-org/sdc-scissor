import os

# dirs
codes_directory = os.path.dirname(os.path.abspath(__file__))
root_directory = os.path.join(codes_directory, "..", "..")
data_directory = os.path.join(root_directory, "data")

# benchmarks, configs, and number of execution repeats used in this experiment
benchmarks = ["BeamNG_RF_1_Complete", "BeamNG_RF_1_5_selected", "DriverAI_Complete"]
configurations = ["default-GA", "10_feature_GA", "6_feature_GA"]
number_of_runs = 30

# Open the output csv
out_csv_address = os.path.join(data_directory, "results.csv")
out_csv = open(out_csv_address, "w")
out_csv.write("benchmark,config,execution_id,best_fitness_value,APFD,elapsed_time,avg_rand_APFD,std_rand_APFD")
out_csv.write("\n")
out_csv.close()

out_csv = open(out_csv_address, "a")
for benchmark in benchmarks:
    for config in configurations:
        for run in range(1, number_of_runs + 1):
            current_data_directory = os.path.join(data_directory, benchmark, config, str(run))
            current_results_csv = os.path.join(current_data_directory, "results.csv")

            f = open(current_results_csv)
            lines = f.readlines()
            # pop the title line
            lines.pop(0)

            for interesting_line in lines:
                prepared_line_to_save = benchmark + "," + interesting_line
                out_csv.write(prepared_line_to_save)

out_csv.close()
