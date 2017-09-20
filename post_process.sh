#!/bin/bash

# templates for modification

########## p8
lmp_avgs_to_tsv.py ./J1_10K.out | awk 'BEGIN {OFS = "\t"}; {print $1, $3+$5+$7-2*$4-($10+$12+$14-2*$11), $3+$5+$8-$4-($10+$12+$15-$11), $7-$4-($14-$11), $8-$15;}' | tsv_eq_trends.py -c 1 "CV_o" -c 2 "CV_i" -c 3 "CV_ao" -c 4 "CV_ai" -n 500 -s 500




lmp_avgs_to_tsv.py J1_10K.out | awk 'BEGIN {OFS = "\t"}; {print $1, ($10-$9)-($3-$2), ($12-$9)-($5-$2), ($14-$9)-($7-$2), $15-$8, $9-$2;}' |  tsv_plot_stacked_bar.py -r 100 4300 --avg-every 1000 --title "Heat Flux Breakdown (improved angle)" -c 1 Pair -c 2 Bond -c 4 Angle -c 5 "KE + PE" && open tempoutcols.png

#angle importance 1
lmp_avgs_to_tsv.py pe10K.out | tsv_eq_trends.py -c 2 AnglePE -c 1 AllPE --nrows 500 -s 500
#angle importance 2
lmp_avgs_to_tsv.py pe1.out | tsv_stats.py -r 3000000 43000000



#### EQUILIBRATION AVERAGES ####
lmp_avgs_to_tsv.py ./J1_10K.out | awk 'BEGIN {OFS = "\t"}; {print $1, $3+$5+$7-2*$4, $3+$5+$8-$4, $10+$12+$14-2*$11, $10+$12+$15-$11, $3+$5+$7-2*$4-($10+$12+$14-2*$11), $3+$5+$8-$4-($10+$12+$15-$11);}' | tsv_eq_trends.py -c 5 "CV_o" -c 6 "CV_i" -c 1 "CVL_o" -c 2 "CVL_i" -c 3 "CVR_o" -c 4 "CVR_i" -n 500 -s 0

lmp_avgs_to_tsv.py ../output-0-23M/J1_10K.out ./J1_10K.out | awk 'BEGIN {OFS = "\t"}; {print $1, $3+$5+$7-2*$4, $3+$5+$8-$4, $10+$12+$14-2*$11, $10+$12+$15-$11, $3+$5+$7-2*$4-($10+$12+$14-2*$11), $3+$5+$8-$4-($10+$12+$15-$11);}' | tsv_eq_trends.py -c 5 "CV_o" -c 6 "CV_i" -c 1 "CVL_o" -c 2 "CVL_i" -c 3 "CVR_o" -c 4 "CVR_i" -n 500 -s 200 > ../../heat_flux_averages.txt

#### TEMP PROFILE ####

# 0-23M
lmp_chunks_to_tsv.py ../output-0-23M/temps10_10K.out | tsv_plot_chunks.py  --yl "Temp [K]" --xl "Z [A]" --avg-every 10 --yr 200 300 --xr 0 40 --plot-every 10 -v 0 2 '#c7d9e8' -v 4 16 0.90 -v 18 22 '#f6d5ac' -v 24 36 0.9 -v 38 40 '#c7d9e8' --chunksize 3.5 && open tempout.chunks.png

# for 23-63M
lmp_chunks_to_tsv.py ./temps10_10K.out | tsv_plot_chunks.py  --yl "Temp [K]" --xl "Z [A]" --avg-every 50 --yr 200 300 --xr 0 40 --plot-every 10 -v 0 2 '#c7d9e8' -v 4 16 0.90 -v 18 22 '#f6d5ac' -v 24 36 0.9 -v 38 40 '#c7d9e8' --chunksize 3.5 && open tempout.chunks.png


####  DENSITY PROFILE ####
lmp_chunks_to_tsv.py density100_10K.out | tsv_plot_chunks.py  --yl "Density" --xl "Chunk" --avg-every 10 --plot-every 20


#### HEAT FLUX BREAKDOWN ####

# both sides -- change r
lmp_avgs_to_tsv.py J1_10K.out | awk 'BEGIN {OFS = "\t"}; {print $1, ($10-$9)-($3-$2), ($12-$9)-($5-$2), ($14-$9)-($7-$2), $15-$8, $9-$2;}' |  tsv_plot_stacked_bar.py -r 100 4300 --avg-every 1000 --title "Heat Flux Breakdown (improved angle)" -c 1 Pair -c 2 Bond -c 4 Angle -c 5 "KE + PE" && open tempoutcols.png


# cvl
lmp_avgs_to_tsv.py J1_10K.out | awk 'BEGIN {OFS = "\t"}; {print $1, $3-$2, $5-$2, $7-$2, $8, $2;}' |  tsv_plot_stacked_bar.py -r 200 2300 --avg-every 600 -c 1 P -c 2 B -c 4 A_i -c 5 E
# cvr
lmp_avgs_to_tsv.py J1_10K.out | awk 'BEGIN {OFS = "\t"}; {print $1, $10-$9, $12-$9, $14-$9, $15, $9;}' |  tsv_plot_stacked_bar.py -r 200 2300 --avg-every 600 -c 1 P -c 2 B -c 4 A_i -c 5 E

# both sides – two files
lmp_avgs_to_tsv.py ../../p7-propane/output/J1_10K.out J1_10K.out | awk 'BEGIN {OFS = "\t"}; {print $1, ($10-$9)-($3-$2), ($12-$9)-($5-$2), ($14-$9)-($7-$2), $15-$8, $9-$2;}' |  tsv_plot_stacked_bar.py -r 100 6300 --avg-every 1000 --title "Heat Flux Breakdown (improved angle)" -c 1 Pair -c 2 Bond -c 4 Angle -c 5 "KE + PE" && open tempoutcols.png

#### TEMPERATURE GRADIENT ###

# take CVL rows only and linear fit
lmp_chunks_to_tsv.py ../../p7-propane/output/temps10_10K.out temps10_10K.out | cut -f 1,6-17 | tsv_plot_chunks.py --avg-every 10 --show-fit --yl "Temp [K]" --xl "CVL Chunk" --yr 200 300 --rows 3300 6300 --chunksize 3.5 --xlabel "CVL Position (Angstroms)" && open tempout.chunks.png

# take CVR rows only and linear fit
lmp_chunks_to_tsv.py ../../p7-propane/output/temps10_10K.out temps10_10K.out | cut -f 1,26-37 | tsv_plot_chunks.py --avg-every 10 --show-fit --yl "Temp [K]" --xl "CVR Chunk" --yr 200 300 --rows 3300 6300 --chunksize 3.5 --xlabel "CVR Position (Angstroms)" && open tempout.chunks.png
