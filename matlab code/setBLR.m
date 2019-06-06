function setBLR(scope)
%####################SETUP 
fprintf(scope,'DATA:WIDTH 1');
fprintf(scope,'DATA:ENC RIB');
fprintf(scope,'ACQUIRE:STATE STOP');
fprintf(scope,'ACQUIRE:MODE SAMPLE');
%fprintf(scope,'ACQUIRE:MODE AVERAGE');
fprintf(scope,'ACQUIRE:SAMPLINGMODE rt');
%fprintf(scope,'ACQUIRE:NUMAVG? rt');
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%TURN ON
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%AVERAGING
%fprintf(scope,'ACQUIRE:NUMAVG %g',Num_Averages);
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%HERE 
fprintf(scope,'ACQUIRE:STOPAFTER SEQuence');
%fprintf(scope,'ACQUIRE:STOPAFTER RUNstop');
fprintf(scope,'ACQUIRE:STATE RUN');
end