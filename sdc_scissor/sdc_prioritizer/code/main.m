
benchmarks = ["../datasets/fullroad/BeamNG_AI/BeamNG_RF_1/BeamNG_RF_1_Complete.csv" "../datasets/fullroad/BeamNG_AI/BeamNG_RF_1_5/BeamNG_RF_1_5_selected.csv" "../datasets/fullroad/Driver_AI/DriverAI_Complete.csv"];
configurations = ["10_feature_GA"]
is_hybrid = [false]
for h_status = 1 : length(is_hybrid)
    for benchmark_index = 1 : length(benchmarks)
        for config_index = 1 : length(configurations)
            parfor i = 1:30
                runSearch(i,configurations(config_index),benchmarks(benchmark_index),h_status)   
            end
        end
    end
end
