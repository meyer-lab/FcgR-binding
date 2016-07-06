function [Zpcanfacts,nfacts4] = VelicersMAP(X,m)
    Zpca = myPCA(X,m);
    %Using matrices and scalars as labelled in Velicer 1976 (Psychometrika
    %Vol. 41)
    C = cov([X' Zpca']);
    r = corrcov(C);
% Velicer's MAP test

% Harman's data (1967, p 80) 
% r = [
%  1.000  .846  .805  .859  .473  .398  .301  .382,
%   .846 1.000  .881  .826  .376  .326  .277  .415,
%   .805  .881 1.000  .801  .380  .319  .237  .345,
%   .859  .826  .801 1.000  .436  .329  .327  .365,
%   .473  .376  .380  .436 1.000  .762  .730  .629,
%   .398  .326  .319  .329  .762 1.000  .583  .577,
%   .301  .277  .237  .327  .730  .583 1.000  .539,
%   .382  .415  .345  .365  .629  .577  .539 1.000  ];


    nvars = size(r,1);
    [eigvect,eigval] = eig(r);
    eigval = diag(eigval);
    [eigval,k] = sort(eigval,'descend'); % sort the eigenvalues & get the indicies
    eigvect = eigvect(:,k); % sort the eigenvectors based on the indicies

    loadings = eigvect * sqrt(diag(eigval,0));

    fm = [(1:nvars); (1:nvars)]';
    fm(1,2) = (sum(sum(r.^2))-nvars)/(nvars*(nvars-1));
    fm4 = fm;
    fm4(1,2) = (sum(sum(r.^4))-nvars)/(nvars*(nvars-1));
    for m = 1:nvars - 1;
        biga = loadings(:,1:m);
        partcov = r - (biga * biga');
        d = diag (  (1 ./ sqrt(diag(partcov)))   , 0);
        pr = d * partcov * d;
        fm(m+1,2)  = (sum(sum(pr.^2))-nvars)/(nvars*(nvars-1));
        fm4(m+1,2) = (sum(sum(pr.^4))-nvars)/(nvars*(nvars-1));
    end;

    % identifying the smallest fm value & its location
    minfm = fm(1,2);
    nfacts = 0;
    minfm4 = fm4(1,2);
    nfacts4 = 0;
    for s = 1:nvars;
        fm(s,1)  = s - 1;
        fm4(s,1) = s - 1;
        if fm(s,2)  < minfm  ; 
            minfm  = fm(s,2);  
            nfacts  = s - 1;
        end; 
        if fm4(s,2) < minfm4 ; 
            minfm4 = fm4(s,2); 
            nfacts4 = s - 1;
        end; 
    end;
    
    %%%My edit
    Zpcanfacts = Zpca(1:nfacts4,:);

%     disp([' ']);disp([' ']);disp(['Velicer"s Minimum Average Partial (MAP) Test:']);disp([' ']);
%     %disp(['   Eigenvalues ']);
%     %disp([eigval]);
%     disp(['             Average    Average']);
%     disp(['             part r sq  part r 4rth']);
%     disp([fm fm4(:,2)]);
%     disp(['The smallest average squared partial correlation is      ' num2str(minfm)]); disp([' '])
%     disp(['The smallest average 4rth power partial correlation is   ' num2str(minfm4)]); disp([' '])
%     disp(['The Number of Components According to the Original (1976) MAP Test is = ' num2str(nfacts)]); disp([' '])
%     disp(['The Number of Components According to the Revised  (2000) MAP Test is = ' num2str(nfacts4)]); disp([' '])

    %--------------------------------------------------------------------------
    % References

    % the original MAP test:
    % Velicer, W. F. (1976). Determining the number of components 
    % from the matrix of partial correlations. Psychometrika, 41, 321-327.

    % the revised (2000) MAP test i.e., with the partial correlations
    % raised to the 4rth power (rather than squared):
    % Velicer, W. F., Eaton, C. A., and Fava, J. L. (2000). Construct
    % explication through factor or component analysis: A review and 
    % evaluation of alternative procedures for determining the number 
    % of factors or components. Pp. 41-71 in R. D. Goffin and 
    % E. Helmes, eds., Problems and solutions in human assessment. 
    % Boston: Kluwer.

    % the present programs:
    % O'Connor, B. P. (2000). SPSS and SAS programs for determining 
    % the number of components using parallel analysis and Velicer's 
    % MAP test. Behavior Research Methods, Instrumentation, and
    % Computers, 32, 396-402.
end