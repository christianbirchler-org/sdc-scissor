function mutationChildren = permutationMutation(parents,~,GenomeLength,~,state,~,thisPopulation,mutationRate)
state.Generation
nVar = length(thisPopulation(parents(1),:));

if nargin < 8 || isempty(mutationRate)
    mutationRate = 1/nVar; % default mutation rate
end

mutationChildren = zeros(length(parents),GenomeLength);
    for i=1:length(parents)
        child = thisPopulation(parents(i),:);

        for j=1:round(nVar * mutationRate)
            % indexes of the element to permute
            mutationPoint1 = randi(nVar, 1);
            mutationPoint2 = randi(nVar-1, 1);

            prob = rand();
            
            % SWAP mutation
            if prob <= 0.33
                temp = child(mutationPoint1);
                child(mutationPoint1) = child(mutationPoint2);
                child(mutationPoint2) = temp;
            else
                % INVERT mutation
                if prob <= 0.66
                    min_index = min(mutationPoint1, mutationPoint2);
                    max_index = max(mutationPoint1, mutationPoint2); 
                    child(min_index:max_index) = child(max_index:-1:min_index);
                else
                    % INSERT mutation
                    temp = child(mutationPoint1);
                    child(mutationPoint1) = [];
                    child = [child(1:mutationPoint2), temp, child(mutationPoint2+1:nVar-1)];
                end
            end
        end

        % storing the child
        mutationChildren(i,:) = child;
    end
end


