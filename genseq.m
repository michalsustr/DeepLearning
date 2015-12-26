exMax = 100;
fmMax = 80;
Nseqtogen = 1;


for i=1:Nseqtogen
   fprintf('Generating seq %d/%d\n', i, Nseqtogen);
    
   Nfm = randi([10, 50], 1);
   Nex = randi([10, 50], 1);
   X=[];
   y=[];
   while(Nfm > 0 || Nex > 0)
       exorfm = randi([0,1], 1);
       len = randi([10, 30],1);
       if(exorfm)
          Nex = Nex-1;
          peak = exMax;
          y = [y; zeros(len*2-5,1); ones(5,1)];
       else
          Nfm = Nfm-1;
          peak = randi([10, fmMax], 1);
          y = [y; zeros(len*2,1)];
       end
       
       
       X = [X; linspace(1,peak,len)'; linspace(peak-1,1,len)'];
   end
   
   dlmwrite(['data/generated/' num2str(i) '.csv'], [X,y]);
end