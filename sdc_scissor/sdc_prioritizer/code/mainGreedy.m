benchmarks = ["../datasets/fullroad/BeamNG_AI/BeamNG_RF_1/BeamNG_RF_1_Complete.csv" "../datasets/fullroad/BeamNG_AI/BeamNG_RF_1_5/BeamNG_RF_1_5_selected.csv" "../datasets/fullroad/Driver_AI/DriverAI_Complete.csv"];

mat = ["benchmark" "config" "APFD" "elapsed_time"];
for benchmark_index = 1 : length(benchmarks)
    tic
    APFD = runGreedy("greedy",benchmarks(benchmark_index))
    elapsed_time=toc    
    [filepath,name,ext] = fileparts(benchmarks(benchmark_index))
    mat = [mat; name "Greedy" APFD elapsed_time]
end

output_dir = strcat("../data/")
writematrix(mat,strcat(output_dir,"greedy_results.csv"))