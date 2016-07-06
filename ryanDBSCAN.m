%Ryan's modification of S. Mostapha Kalami Heris's algorithm:
%
%[IDX, isnoise]=ryanDBSCAN(points,epsilon,MinPts)
%
%Points must be row vectors in a matrix. epsilon is the maximum Euclidean 
%distance between two points for those points to be density-reachable,
%granted both points are within distance epsilon of at lease MinPts points,
%including themselves in that count (please read Wikipedia's article on
%DBSCAN)
%--------------------------------------------------------------------------
%
% Copyright (c) 2015, Yarpiz (www.yarpiz.com)
% All rights reserved. Please read the "license.txt" for license terms.
%
% Project Code: YPML110
% Project Title: Implementation of DBSCAN Clustering in MATLAB
% Publisher: Yarpiz (www.yarpiz.com)
% 
% Developer: S. Mostapha Kalami Heris (Member of Yarpiz Team)
% 
% Contact Info: sm.kalami@gmail.com, info@yarpiz.com
%

function [IDX, isnoise]=ryanDBSCAN(points,epsilon,MinPts)
    %Number of points
    n = size(points,1);
    %Euclidean distance between each combination of point
    distances = pdist(points,points);
    %The first column vector states whether each point is a core point, a reachable
    %non-core point, or a noise point (2,1, or 0, respectively). The second
    %vector hold a number for each vector which states to what cluster it
    %belongs.
    identity = zeros(n,1);
    %A clustered array which will contain each cluster in entirety, each
    %cluster being represented by a vector of indices
    clusters = {};
    
    for j = 1:n
        test = 0;
        %sameCluster is a vector of logicals stating whether the point at
        %each index is in the same cluster as the main point assuming the
        %main point is a core point
        sameCluster = zeros(n,1);
        for k = 1:n
            testDist = (epsilon >= distances(j,k));
            test = test + testDist;
            if testDist
                if identity(k) == 0
                    identity(k) = 1;
                    sameCluster(k) = 1;
                end
            end
        end
        if test >= MinPts
            identity(j) = 2;
            
        end
    end
end
%-------------------------------------------------------------------------
function 