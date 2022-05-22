function [AUC] = fitness(X)
global A Cost

[~,n] = size(X);
AUC = 0;
for i=1:n
    % average distance between the the i-th test and the previous ones
    %averageDistance = mean(A(X(1:i), X(i)));
    if (i == 1)
        distance =  A(X(i+1), X(i));
    else
        distance = A(X(i-1), X(i));
    end
    
    AUC = AUC + distance / Cost(X(i)) / i ; 
end

AUC = -AUC; %% we want to maximize
end
