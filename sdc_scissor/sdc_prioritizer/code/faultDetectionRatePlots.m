input_csv_dir = "r-script/medians_APFDc.csv"
cases = readtable(input_csv_dir);
cases_size = height(cases);
data_dir = "../data/";
output_dir = strcat(data_dir,"figures/samples/");
greedy_permutations_dir = strcat(data_dir,"greedy-permutations/")

% tiledlayout(1,3)

benchmarks = ["../datasets/fullroad/BeamNG_AI/BeamNG_RF_1/BeamNG_RF_1_Complete.csv" "../datasets/fullroad/BeamNG_AI/BeamNG_RF_1_5/BeamNG_RF_1_5_selected.csv" "../datasets/fullroad/Driver_AI/DriverAI_Complete.csv"];

for row_index = 1:cases_size
%     nexttile
    
    benchmark = cases{row_index,"benchmark"}{1,1};
    execution_id_so = cases{row_index,"execution_id_so"};
    execution_id_mo = cases{row_index,"execution_id_mo"};
    solution_id_mo = cases{row_index,"solution_id_mo"};
    
    
    if benchmark == "BeamNG.AI.AF1"
        benchmark_data_dir=strcat(data_dir,"BeamNG_RF_1_Complete/");
        csv_file = benchmarks(1)
    elseif benchmark == "BeamNG.AI.AF1.5"
          benchmark_data_dir=strcat(data_dir,"BeamNG_RF_1_5_selected/");  
          csv_file = benchmarks(2)
    else
        benchmark_data_dir=strcat(data_dir,"DriverAI_Complete/");
        csv_file = benchmarks(3)
    end

    T = readtable(csv_file);
    Cost = table2array(T(:,19));
    Features = table2array(T(:,1:16)); 
    [coeff,scores,latent, tsd, variance,mu] = pca(Features);
    Features = scores(:,1:10);
    [m, n] = size(Features);


    
    permutation_dir_so = strcat(benchmark_data_dir,"10_feature_GA/",int2str(execution_id_so),"/best-permutation.csv");
    permutation_dir_mo = strcat(benchmark_data_dir,"mo-10_feature_GA/",int2str(execution_id_mo),"/best-permutation.csv");

    permutation_so = readmatrix(permutation_dir_so);

    permutations_mo = readmatrix(permutation_dir_mo);
    permutation_mo = permutations_mo(solution_id_mo,:);
    
    
    [a,b] = faultDetection(permutation_so, T, Cost); 
    
    
    APFD_c = trapz(a, b) / max(a) / max(b)
    zoomIndex = (max(a)*0.2)
    
    pl = plot(a, b, 'm','LineWidth',3.0);
    for ind = 1 : length(a)
        if a(ind) > zoomIndex
            line([0,zoomIndex], [b(ind),b(ind)],'Color','m','LineStyle','--')
            text(zoomIndex+700,b(ind),strcat(num2str(b(ind))," faults"),"FontSize",12,"FontWeight","bold")
            break
        end
    end
    
    hold on



    [a,b] = faultDetection(permutation_mo, T, Cost); 
    
    
    APFD_c = trapz(a, b) / max(a) / max(b)
    zoomIndex = (max(a)*0.2)
    
    pl = plot(a, b, 'r','LineWidth',3.0);
    for ind = 1 : length(a)
        if a(ind) > zoomIndex
            line([0,zoomIndex], [b(ind),b(ind)],'Color','r','LineStyle','--')
            text(zoomIndex+700,b(ind),strcat(num2str(b(ind))," faults"),"FontSize",12,"FontWeight","bold")
            break
        end
    end
    
%     datatip(pl,zoomIndex,0.5);
    
    
    %% Random permutations (baseline)
    max_APFD = 0;
    for i=1:500
        [a,b] = faultDetection(randperm(m), T, Cost); 
%         plot(a, b, 'b');
        rand_APFD = trapz(a, b) / max(a) / max(b);
        if (max_APFD < rand_APFD)
            max_APFD = rand_APFD;
            max_A = a;
            max_B = b;
        end
    end
    
    pl = plot(max_A, max_B, 'b','LineWidth',3.0);
    
    a = max_A;
    b =  max_B;
    for ind = 1 : length(a)
        if a(ind) > zoomIndex
            line([0,zoomIndex], [b(ind),b(ind)],'Color','b','LineStyle','--')
            text(zoomIndex-6000,b(ind)+10,strcat(num2str(b(ind))," faults"),"FontSize",11,"FontWeight","bold")
            break
        end
    end
%     datatip(pl,zoomIndex,0.5);

    %% Greedy permutation

    if benchmark == "BeamNG.AI.AF1"
        greedy_permutation_csv_dir=strcat(greedy_permutations_dir,"BeamNG_RF_1_Complete.csv");
    elseif benchmark == "BeamNG.AI.AF1.5"
          greedy_permutation_csv_dir=strcat(greedy_permutations_dir,"BeamNG_RF_1_5_selected.csv");  
    else
        greedy_permutation_csv_dir=strcat(greedy_permutations_dir,"DriverAI_Complete.csv");
    end

    permutation_greedy = readmatrix(greedy_permutation_csv_dir);


    [a,b] = faultDetection(permutation_greedy, T, Cost); 
    
    
    APFD_c = trapz(a, b) / max(a) / max(b)
    zoomIndex = (max(a)*0.2)
    
    pl = plot(a, b, 'k','LineWidth',3.0);
    for ind = 1 : length(a)
        if a(ind) > zoomIndex
            line([0,zoomIndex], [b(ind),b(ind)],'Color','k','LineStyle','--')
            text(zoomIndex+700,b(ind),strcat(num2str(b(ind))," faults"),"FontSize",12,"FontWeight","bold")
            break
        end
    end


%     Differences = pdist(Features,"seuclidean");
%     Differences = squareform(Differences);
%     
%     maximum = max(max(Differences));
%     [x,y] = find(Differences==maximum);
%     
%     
%     firstTest=x(1);
%     secondTest=x(2);
%     permutation_size = size(Features,1);
%     greedy_permutation = [firstTest,secondTest];
%     
%     for index = 3:permutation_size
%         max_avg=0;
%         max_index=0;
%         for c = 1:permutation_size
%             if ~ismember(c, greedy_permutation)
%                 dists=0;
%                 for already_selected_test_index = 1:(index-1)
%                     dists= dists + Differences(c,greedy_permutation(already_selected_test_index));
%                 end
%                 avg = dists/(index-1);
%                 if avg > max_avg
%                     max_avg = avg;
%                     max_index = c;
%                 end
%             end
%         end
%         % Now, we add the detected max
%         greedy_permutation(index) = max_index;
%     end
%      
%     [a,b] = faultDetection(greedy_permutation, T, Cost); 
%     APFD_g = trapz(a, b) / max(a) / max(b)
%     plot(a, b, 'k','LineWidth',3.0);
%     
%     for ind = 1 : length(a)
%         if a(ind) > zoomIndex
%             line([0,zoomIndex], [b(ind),b(ind)],'Color','b','LineStyle','--')
%             text(zoomIndex+700,b(ind),strcat(num2str(b(ind))," faults"),"FontSize",12,"FontWeight","bold")
%             break
%         end
%     end
    
    xline(zoomIndex,'--');
     hold off
     legend({'SO-SDC-Prioritizer','','MO-SDC-Prioritizer','','random','','greedy'},'Location','southeast','Orientation','vertical','FontSize',14,"FontWeight","bold")
     xlabel('Test Execution Cost (Seconds)',"FontWeight","bold","FontSize",12) 
     ylabel('Number of Detected Faults',"FontWeight","bold","FontSize",12)
     
     exportgraphics(gcf,strcat(output_dir,benchmark,".png"))
    
end