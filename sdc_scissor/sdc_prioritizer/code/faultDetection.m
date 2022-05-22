function [xValues, yValues] = faultDetection(X, T, Cost)
labels = char(table2array(T(:,20)));

nPoints = length(labels);
faults = zeros(1,nPoints);
for i=1:nPoints
    if (contains(labels(i,:),'unsafe'))
        faults(1,i) = 1;
    end
end

xValues = zeros(1, nPoints);
yValues = zeros(1, nPoints);
totalFaults = 0;
totlalCost = 0;

for i=1:nPoints
    totlalCost = totlalCost + Cost(X(i));
    totalFaults = totalFaults + faults(X(i));
    
    xValues(1,i) = totlalCost;
    yValues(1,i) = totalFaults;
end
end

