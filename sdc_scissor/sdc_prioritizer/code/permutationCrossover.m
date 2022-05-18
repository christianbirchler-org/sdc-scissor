function xoverKids = permutationCrossover(parents,options,GenomeLength,~,~,thisPopulation)

nKids = length(parents)/2;
% Allocate space for the kids
xoverKids = zeros(nKids,GenomeLength);

% To move through the parents twice as fast as thekids are
% being produced, a separate index for the parents is needed
index = 1;

for i=1:nKids
    % get parents
    parent1 = thisPopulation(parents(index),:);
    index = index + 1;
    parent2 = thisPopulation(parents(index),:);
    index = index + 1;

    % cut point is AFTER this index.
    cutPoint = randi(length(parent1), 1);
    head = parent1(1, 1:cutPoint);
    indexes = not(ismember(parent2, head));
    tail = parent2(1, indexes);    
   
    % make one child
    xoverKids(i,:) = [ head, tail ];
   
end
