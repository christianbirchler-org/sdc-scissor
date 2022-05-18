function [value] = plotResults(X, color)
global A Cost

[m,n] = size(X);

xValues = zeros(1, m);
yValues = zeros(1, m);

xValues(1,1) = 0;
yValues(1,1) = 0;

value = 0;
for i=2:n
    xValues(1,i) = xValues(1,i-1) + Cost(X(i));
    yValues(1,i) = A(X(i-1), X(i));
end
plot(xValues, yValues, color);
end

