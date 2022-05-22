function [objs] = objectives(X)
global A Cost

[~,n] = size(X);
obj1 = 0;
obj2 = 0;
for i=1:n-1
   obj1 = obj1 + Cost(X(i)) / i;
   obj2 = obj2 + A(X(i), X(i+1)) / i;
end
objs = [obj1; -obj2]; %% we want to maximize
end

