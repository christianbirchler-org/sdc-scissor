%% Read the dataset
%T = readtable('../datasets/fullroad/BeamNG_AI/BeamNG_RF_1/BeamNG_RF_1_Complete.csv');
%T = readtable('../datasets/fullroad/BeamNG_AI/BeamNG_RF_1_5/BeamNG_RF_1_5_selected.csv');
T = readtable('../datasets/fullroad/Driver_AI/DriverAI_Complete.csv');
TRaw = T(:,1:16);

mat = TRaw{:,:}

[idx,scores] = fsulaplacian(mat)


%[coeff,score,latent, tsd, variance,mu] = pca(ma)

%cs = cumsum(variance)
%E = score * coeff(1:16,1:6)


%E = score(:,1:6)

