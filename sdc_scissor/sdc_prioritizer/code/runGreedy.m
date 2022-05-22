function [APFD_g] = runGreedy(configuration,csv_file)

csv_file
T = readtable(csv_file);
Cost = table2array(T(:,19));  
Features = table2array(T(:,1:16));
Differences = pdist(Features,"seuclidean");
Differences = squareform(Differences);



maximum = max(max(Differences));
[x,y] = find(Differences==maximum);

firstTest=x(1);
secondTest=x(2);
permutation_size = size(Features,1);

permutation = [firstTest,secondTest];


for index = 3:permutation_size
    max_avg=0;
    max_index=0;
    for c = 1:permutation_size
       if ~ismember(c, permutation)
           dists=0;
           for already_selected_test_index = 1:(index-1)
              dists= dists + Differences(c,permutation(already_selected_test_index));
           end
           avg =  dists / Cost(c) ;
           if avg > max_avg
               max_avg = avg;
               max_index = c;
           end
       end
    end
    % Now, we add the detected max
    permutation(index) = max_index;
end




[a,b] = faultDetection(permutation, T, Cost); 
APFD_g = trapz(a, b) / max(a) / max(b);



