function population = initialPopulation(GenomeLength,FitnessFcn,options)
global Cost H BM;

totalPopulation = sum(options.PopulationSize);
population = zeros(totalPopulation, GenomeLength);

if H
    permutations_dir =  "../data/greedy-permutations/";
    permutation = readmatrix(strcat(permutations_dir,BM,".csv"));
    population(1,:) = permutation;
    for i=2:totalPopulation/2
            child = permutation;
            % indexes of the element to permute
            mutationPoint1 = randi(GenomeLength, 1);
            mutationPoint2 = randi(GenomeLength, 1);
    
            % permutaton
            temp = child(mutationPoint1);
            child(mutationPoint1) = child(mutationPoint2);
            child(mutationPoint2) = temp;
            population(i,:) = child;
    end

    for i=(totalPopulation/2)+1:totalPopulation-1
        population(i,:) = randperm(GenomeLength);
    end
    
else
    for i=1:totalPopulation-1
        population(i,:) = randperm(GenomeLength);
    end
end

[~, indexes] = sort(Cost,  'ascend');
population(totalPopulation,:) = indexes;
end

