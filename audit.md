# Experiment post-processing snippets

## i1-idealized mofs

### Cubic [cubic_6x6x40]

make sure temperature profiles are steady:
```
lmp_chunks_to_tsv.py  ./temps10_10K.out | tsv_plot_chunks.py -o temps.png --yl "Temp [K]" --xl "Z [A]" --avg-every 10 --yr 280 320 --xr 0 40 --plot-every 25 -v 0 2 '#c7d9e8' -v 4 16 0.90 -v 18 22 '#f6d5ac' -v 24 36 0.9 -v 38 40 '#c7d9e8' --chunksize 10 --fit 40 160 --fit 240 360 && open temps.png
```

Looks ok from 5M on... R > 0.98

calculate per-term averages:

```bash
lmp_avgs_to_tsv.py ./J1_10K.out | awk 'BEGIN {OFS = "\t"}; {print $1, $2-$9, $3-$2-($10-$9), $5-$2-($12-$9), $7-$4-($14-$11), $8-$15, $3+$5+$7-2*$4-($10+$12+$14-2*$11), $3+$5+$8-$4-($10+$12+$15-$11);}' | tsv_eq_trends.py -c 1 "CV_KEPE" -c 2 "CV_p" -c 3 "CV_b" -c 4 "CV_ao" -c 5 "CV_ai" -c 6 "CV_o" -c 7 "CV_i" -n 500 -s 500 | less -S
```

< 10% fluctuations in corrected angle. OK.

### Triangular [triangular_4x4x400]

make sure temperature profiles are steady:
```
lmp_chunks_to_tsv.py  ./temps10_10K.out | tsv_plot_chunks.py -o temps.png --yl "Temp [K]" --xl "Z [A]" --avg-every 10 --yr 220 380 --xr 0 40 --plot-every 25 -v 0 2 '#c7d9e8' -v 4 16 0.90 -v 18 22 '#f6d5ac' -v 24 36 0.9 -v 38 40 '#c7d9e8' --chunksize 10 --fit 40 160 --fit 240 360 && open temps.png
```

Looks ok from 3M on... but using 5M+ for congruity. R > 0.99

calculate per-term averages:

```bash
lmp_avgs_to_tsv.py ./J1_10K.out | awk 'BEGIN {OFS = "\t"}; {print $1, $2-$9, $3-$2-($10-$9), $5-$2-($12-$9), $7-$4-($14-$11), $8-$15, $3+$5+$7-2*$4-($10+$12+$14-2*$11), $3+$5+$8-$4-($10+$12+$15-$11);}' | tsv_eq_trends.py -c 1 "CV_KEPE" -c 2 "CV_p" -c 3 "CV_b" -c 4 "CV_ao" -c 5 "CV_ai" -c 6 "CV_o" -c 7 "CV_i" -n 500 -s 500 | less -S
```

< 2% fluctuations in corrected angle. OK.



### Hexagonal [hexagonal_4x4x400]

make sure temperature profiles are steady [same as triangle].

Looks ok from 3-15M on... R > 0.99

calculate per-term averages:

```bash
lmp_avgs_to_tsv.py ./J1_10K.out | awk 'BEGIN {OFS = "\t"}; {print $1, $2-$9, $3-$2-($10-$9), $5-$2-($12-$9), $7-$4-($14-$11), $8-$15, $3+$5+$7-2*$4-($10+$12+$14-2*$11), $3+$5+$8-$4-($10+$12+$15-$11);}' | tsv_eq_trends.py -c 1 "CV_KEPE" -c 2 "CV_p" -c 3 "CV_b" -c 4 "CV_ao" -c 5 "CV_ai" -c 6 "CV_o" -c 7 "CV_i" -n 400 -s 300 | less -S
```

< 10% fluctuations in corrected angle. OK.




## h1-hydrocarbons





## Green-Kubo analysis

to get pressure for gk analysis:

```bash
for dir in `ls ./`; do
  echo "$dir"
  lmp_log_to_tsv.py $dir/output/log.lammps | tsv_stats.py -r 209 510 -c 1 timestep -c 3 temp -c 4 pressure -c 5 density
done
```

to create input files for thermal_conductivity_via_acf.py script:

```bash
mkdir -p acf_outputs
mkdir -p acf_outputs/original

for filename in `ls */output/J0Jt_*.dat`; do
  echo "$filename => ${filename//\//-}"
  tail -n 20000 $filename > ./acf_outputs/original/${filename//\//-}
done

mkdir -p acf_outputs/corrected
for filename in `ls */output/J0Jti_*.dat`; do
  echo "$filename => ${filename//\//-}"
  tail -n 20000 $filename > ./acf_outputs/corrected/${filename//\//-}
done
```

then run thermal_conductivity_via_acf.py
