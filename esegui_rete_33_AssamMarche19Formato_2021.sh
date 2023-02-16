#!/bin/bash
##########################################INIZIALIZZAZIONI#########################################################

rete=33_AssamMarche19Formato

#rm -r INPUT
#mkdir INPUT
#rm -r REPPIERO
#mkdir REPPIERO
rm -r NORMALIZED
mkdir NORMALIZED
rm -r NEWSTATIONS
mkdir NEWSTATIONS
rm -r INDICATORIDAY
mkdir INDICATORIDAY



#mkdir INPUT/${rete}
mkdir NORMALIZED/${rete}
mkdir NEWSTATIONS/${rete}
mkdir INDICATORIDAY/${rete}

for year in {2021..2021}
do 
	echo $year
	#mkdir INPUT/${rete}_${year}
	mkdir NORMALIZED/${rete}_${year}
	mkdir NEWSTATIONS/${rete}_${year}
	mkdir INDICATORIDAY/${rete}_${year}
done


########################################## 01 DOWNLOAD RETE 33 ASSAM MARCHE#########################################################
############################################ESEGUITO MANUALMENTE

######################################### 02 CONTROLLO FILE E CARTELLE ETEROGENEI CONTENENTI MISURE CLIMATICHE#########################################################
#NOTA IN INPUT OUT REPPIERO ESEGUE SOLO CONTROLLI E GENERA UN REPORT
for year in {2021..2021}
do 
	./ve/bin/make_reports -r REPPIERO/report_02_CONTROLLO_CARTELLA_${rete}_${year}.txt INPUT/${rete}_${year}
	toilet -f term -F border --gay '02 CONTROLLO FILE E CARTELLE ETEROGENEI CONTENENTI MISURE CLIMATICHE ESEGUITO '${rete}${year}
done

######################################### 03 ESPORTAZIONE DI DATI CLIMATICI IN FORMATO OMOGENEO  #########################################################
#NOTA IN INPUT OUT NORMALIZED REP REPPIERO GENERA FILES IN FORMATO NORMALIZZATO
for year in {2021..2021}
do 
	./ve/bin/make_reports -r REPPIERO/report_03_ESPORTAZIONE_FORMATO_OMOGENEO_${rete}_${year}.txt INPUT/${rete}_${year} -d NORMALIZED/${rete}_${year}
	toilet -f term -F border --gay '03 ESPORTAZIONE DI DATI CLIMATICI IN FORMATO OMOGENEO ESEGUITO '${rete}${year}

done

########################################## 04 RICERCA NUOVE STAZIONI DAI DATI ESTRATTI IN FORMATO OMOGENEO IN SUBDIRECTORY #########################################################
#A QUESTO PUNTO OPZIONALE SERVE SOLO PER VERIFICHE
for year in {2021..2021}
do 
	./ve/bin/find_new_stations NORMALIZED/${rete}_${year} -s NEWSTATIONS/${rete}_${year}/new_stations.csv -r REPPIERO/report_04_NUOVE_STAZIONI_${rete}_${year}.txt 
	toilet -f term -F border --gay '04 RICERCA NUOVE STAZIONI DAI DATI ESTRATTI IN FORMATO OMOGENEO ESEGUITO '${year}
done

########################################## 05 INSERIMENTO DELLE NUOVE STAZIONI NEL DATABASE  #########################################################

toilet -f term -F border --gay '05 INSERIMENTO DELLE NUOVE STAZIONI NEL DATABASE ESEGUITO TRAMITE NAVICAT SALTO  '

########################################## 06 CALCOLO DEGLI INDICATORI GIORNALIERI  #########################################################
#ESEGUE IL CALCOLO DEGLI INDICATORI GIORNALIERI PER IL SUCCESSIVO CARICAMENTO 
for year in {2021..2021}
do 
	./ve/bin/compute_daily_indicators NORMALIZED/${rete}_${year} INDICATORIDAY/${rete}_${year} -r REPPIERO/report_06_INDICATORIDAY_${rete}_${year}.txt
	toilet -f term -F border --gay '06 CALCOLO DEGLI INDICATORI GIORNALIERI ESEGUITO '${year}

done


########################################## 07 INSERIMENTO DEGLI INDICATORI GIORNALIERI NEL DATABASE  #########################################################
#INSERIMENTO INDICATORI DAILY NEL DATABASE 
for year in {2021..2021}
do 
	./ve/bin/insert_daily_indicators -r REPPIERO/report_07_INSERIMENTO_INDICATORIDAY_${rete}_${year}.txt -p upsert -s dailypdbanpacarica INDICATORIDAY/${rete}_${year}
	toilet -f term -F border --gay '07 INSERIMENTO DEGLI INDICATORI GIORNALIERI NEL DATABASE  ESEGUITO   '${year}
done





