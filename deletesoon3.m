close all
clear;clc;

load exploratorya

sz = 37;

a = figure;
set(a,'Units','normalized','Position',[0 0 1 1]);
for j = 1:sz
    for k = 1:sz
        if j ~= k
            if diffRmulti(j,k) > 0
                color = 'b';
            else
                color = 'r';
            end
            colorshp = ['.' color];
            eval(['p_' num2str(j) '_' num2str(k) ' = plot3(diffParamRmulti(1,j,k),'...
                'diffParamRmulti(2,j,k),logKd(k)-logKd(j),colorshp);'])
            hold on
        end
    end
end
xlabel('Effective avidity')
ylabel('Order of Magnitude of Kx')

figure('color',[1 1 1],'Units','normalized','Position',[0 0 1 1]);
hold on
for j = 1:sz
    for k = 1:sz
        if j ~= k
            if j < k
                color = 'g';
            else
                color = 'k';
            end
            colorshp = ['.' color];
            eval(['q_' num2str(j) '_' num2str(k) ' = plot3(diffParamRmulti(1,j,k),'...
                'diffParamRmulti(2,j,k),diffRmulti(j,k),colorshp);'])
            hold on
        end
    end
end
view(-37.5,30)

% txt = '';
% for j = 1:sz
%     txt = [txt 'logKd(' num2str(j) ') = ' num2str(logKd(j)) char(10)];
% end
% txt = [txt '...or just input 0 for a random combination.' char(10)...
%     'Be sure your input is a 2-D row vector.' char(10) char(10)];
% shp = '*g';
% test = 1;
% while test
%     clc
%     inp = input(txt);
%     if size(inp) ~= [1 2]
%         clc
%         disp('Error...')
%         pause(3)
%     else
%         test = 0;
%     end
% end
% while 1
%     ttla = 'K_{D,a} = ';
%     ttlb = '; K_{D,b} = ';
%     a = inp(1);
%     b = inp(2);
%     eval('title([ttla num2str(logKd(a)) ttlb num2str(logKd(b))])')
%     eval(['delete(p_' num2str(a) '_' num2str(b) ')'])
%     eval(['p_' num2str(a) '_' num2str(b) ' = plot3(diffParamRmulti(1,a,b),'...
%         'diffParamRmulti(2,a,b),logKd(b)-logKd(a),shp);'])
%     hold on
%     drawnow
%     test = 1;
%     while test
%         clc
%         inp = input(txt);
%         if size(inp) ~= [1 2]
%             clc
%             disp('Error...')
%             pause(3)
%         else
%             test = 0;
%         end
%     end
%     eval(['delete(p_' num2str(a) '_' num2str(b) ')'])
%     if diffRmulti(a,b) > 0
%         color = 'b';
%     else
%         color = 'r';
%     end
%     colorshp = ['.' color];
%     eval(['p_' num2str(a) '_' num2str(b) ' = plot3(diffParamRmulti(1,a,b),'...
%         'diffParamRmulti(2,a,b),logKd(b)-logKd(a),colorshp);'])
% end

figure('color',[1 1 1],'Units','normalized','Position',[0 0 1 1])
hold on
for j = 1:sz
    for k = 1:sz
        if j ~= k
            plot3(logKd(j),logKd(k),diffRmulti(j,k),'.k')
            hold on
        end
    end
end
view(-37.5,30)

fig4 = figure('color',[1 1 1],'Units','normalized','Position',[0 0 1 1]);
hold on
for j = 1:sz
    for k = 1:sz
        if j ~= k
            if diffRmulti(j,k) > 0
                if diffParamRmulti(1,j,k) == 2
                    color = 'b';
                elseif diffParamRmulti(1,j,k) == 30
                    color = 'r';
                else
                    color = 'k';
                end
                colorshp = ['o' color];
                eval(['r_' num2str(j) '_' num2str(k)...
                    ' = plot(diffParamRmulti(1,j,k),10^diffParamRmulti(2,j,k),'...
                    'colorshp);'])
                hold on
            end
        end
    end
end
set(gca,'YScale','log')
xlabel('effective avidity')
ylabel('K_X')
frame = getframe(fig4);
image = frame2im(frame);
[imind,cm] = rgb2ind(image,256);
imwrite(imind,cm,'ModesofICDesign.jpg','JPEG')

figure('color',[1 1 1])
text(0.1,0.5,['\color{blue} Higher-affinity receptor preferred'...
    char(10) char(10) '\color{red} Lower-affinity receptor preferred'...
    char(10) char(10) '\color{black} Small difference in receptor affinities'],...
    'FontSize',16)

figure('color',[1 1 1])
text(0.1,0.5,['RIA' char(10) char(10) 'RIIA-131R' char(10) char(10)...
    'RIIA-131H' char(10) char(10) 'RIIB' char(10) char(10) 'RIIIA-158F' char(10)...
    char(10) 'RIIIA-158V'])