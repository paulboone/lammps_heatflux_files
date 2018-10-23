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
lmp_avgs_to_tsv.py ./J1_10K.out | awk 'BEGIN {OFS = "\t"}; {print $1, $2-$9, $3-$2-($10-$9), $5-$2-($12-$9), $7-$4-($14-$11), $8-$15, $3+$5+$7-2*$4-($10+$12+$14-2*$11), $3+$5+$8-$4-($10+$12+$15-$11);}' | tsv_eq_trends.py -c 1 "CV_KEPE" -c 2 "CV_p" -c 3 "CV_b" -c 4 "CV_ao" -c 5 "CV_ai" -c 6 "CV_o" -c 7 "CV_i" -n 500 -s 480 | less -S
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
lmp_avgs_to_tsv.py ./J1_10K.out | awk 'BEGIN {OFS = "\t"}; {print $1, $2-$9, $3-$2-($10-$9), $5-$2-($12-$9), $7-$4-($14-$11), $8-$15, $3+$5+$7-2*$4-($10+$12+$14-2*$11), $3+$5+$8-$4-($10+$12+$15-$11);}' | tsv_eq_trends.py -c 1 "CV_KEPE" -c 2 "CV_p" -c 3 "CV_b" -c 4 "CV_ao" -c 5 "CV_ai" -c 6 "CV_o" -c 7 "CV_i" -n 500 -s 480 | less -S
```

< 2% fluctuations in corrected angle. OK.



### Hexagonal [hexagonal_4x4x400]

make sure temperature profiles are steady [same as triangle].

Looks ok from 3-15M on... but using 5M+ for congruity. R > 0.99.

**IMPORTANT: we are ignoring the data from 15-20M timesteps since the framework buckles.**


calculate per-term averages:

```bash
lmp_avgs_to_tsv.py ./J1_10K.out | awk 'BEGIN {OFS = "\t"}; {print $1, $2-$9, $3-$2-($10-$9), $5-$2-($12-$9), $7-$4-($14-$11), $8-$15, $3+$5+$7-2*$4-($10+$12+$14-2*$11), $3+$5+$8-$4-($10+$12+$15-$11);}' | tsv_eq_trends.py -c 1 "CV_KEPE" -c 2 "CV_p" -c 3 "CV_b" -c 4 "CV_ao" -c 5 "CV_ai" -c 6 "CV_o" -c 7 "CV_i" -n 340 -s 480 | less -S
```

< 10% fluctuations in corrected angle. OK.




## h1-hydrocarbons

### Propane [c3h8]

make sure temperature profiles are steady:
```bash
lmp_chunks_to_tsv.py  ./20M/temps10_10K.out ./49M/temps10_10K.out ./75M/temps10_10K.out | tsv_plot_chunks.py -o temps.png --yl "Temp [K]" --xl "Z [A]" --avg-every 10 --yr 220 320 --xr 0 40 --plot-every 50 -v 0 2 '#c7d9e8' -v 4 16 0.90 -v 18 22 '#f6d5ac' -v 24 36 0.9 -v 38 40 '#c7d9e8' --chunksize 3.23 --fit 12.9 51.7 --fit 77.5 116.3 && open temps.png
```

Temp profiles look ok starting at 5M?

Look at temperature profiles from right before heat sources / sinks are applied:

```bash
lmp_chunks_to_tsv.py  ./20M/temps10_10K.out ./49M/temps10_10K.out ./75M/temps10_10K.out | tsv_plot_chunks.py -o temps-ss.png  -r 400 1000 --yl "Temp [K]" --xl "Z [A]" --avg-every 10 --yr 220 320 --xr 0 40 --plot-every 5 -v 0 2 '#c7d9e8' -v 4 16 0.90 -v 18 22 '#f6d5ac' -v 24 36 0.9 -v 38 40 '#c7d9e8' --chunksize 3.23 --fit 12.9 51.7 --fit 77.5 116.3 && open temps-ss.png
```

...maybe... the first 1M timesteps isn't steady state, but it looks like it is already averaged out when you look at the 5M timestep averages.

```bash
lmp_avgs_to_tsv.py ./20M/J1_10K.out ./49M/J1_10K.out ./75M/J1_10K.out | awk 'BEGIN {OFS = "\t"}; {print $1, $2-$11, $3-$12-($2-$11), $4-$13-($2-$11), $5-$14-($2-$11), $6-$15, $7-$16, $8-$17, $9-$18, $10-$19, $3+$4+$5+$6+$7-2*$2-($12+$13+$14+$15+$16-2*$11), $3+$4+$8+$9+$10-$2-($12+$13+$17+$18+$19-$11);}' | tsv_eq_trends.py -c 1 "CV_KEPE" -c 2 "CV_p" -c 3 "CV_b" -c 4 "CV_a" -c 5 "CV_d" -c 6 "CV_i" -c 7 "CV_ai" -c 8 "CV_di" -c 9 "CV_ii" -c 10 "CV_orig" -c 11 "CV_corr" -n 2150 -s 800 | less -S
```

Note modifications to eliminate out the dihedral and improper terms. Corrected angle looks to be within 2%.


### Octane [c8h18d]

make sure temperature profiles are steady:
```bash
lmp_chunks_to_tsv.py  ./output-45M/temps10_10K.out | tsv_plot_chunks.py -o temps.png -r 300 -1 --yl "Temp [K]" --xl "Z [A]" --avg-every 10 --yr 360 440 --xr 0 40 --plot-every 50 -v 0 2 '#c7d9e8' -v 4 16 0.90 -v 18 22 '#f6d5ac' -v 24 36 0.9 -v 38 40 '#c7d9e8' --chunksize 4.30675 --fit 17.2 68.9 --fit 103.4 155.0 && open temps.png
```

Temp profiles look ok starting at 5M?

Look at temperature profiles from right before heat sources / sinks are applied:

```bash
lmp_chunks_to_tsv.py  ./output-45M/temps10_10K.out | tsv_plot_chunks.py -o temps-ss.png -r 200 800 --yl "Temp [K]" --xl "Z [A]" --avg-every 10 --yr 360 440 --xr 0 40 --plot-every 5 -v 0 2 '#c7d9e8' -v 4 16 0.90 -v 18 22 '#f6d5ac' -v 24 36 0.9 -v 38 40 '#c7d9e8' --chunksize 4.30675 --fit 17.2 68.9 --fit 103.4 155.0 && open temps-ss.png
```

First temperature profile at 5M timesteps looks indistinguishable from the rest.

```bash
 lmp_chunks_to_tsv.py ./output-45M/J1_10K.out ./output-90M/J1_10K.out ./output-135M/J1_10K.out ./output-142M/J1_10K.out |  awk 'BEGIN {OFS = "\t"}; {print $1, $2-$11, $3-$12-($2-$11), $4-$13-($2-$11), $5-$14-($2-$11), $6-$15-($2-$11), $7-$16-($2-$11), $8-$17, $9-$18, $10-$19, $3+$4+$5+$6+$7-4*$2-($12+$13+$14+$15+$16-4*$11), $3+$4+$8+$9+$10-$2-($12+$13+$17+$18+$19-$11);}' | tsv_eq_trends.py -c 1 "CV_KEPE" -c 2 "CV_p" -c 3 "CV_b" -c 4 "CV_a" -c 5 "CV_d" -c 6 "CV_i" -c 7 "CV_ai" -c 8 "CV_di" -c 9 "CV_ii" -c 10 "CV_orig" -c 11 "CV_corr" -n 4400 -s 800 | less -S
```

On 44M rows averaged, angle is within 20%, dihedral is within 10%.



### Hexadecane [c16h34c]



make sure temperature profiles are steady:
```bash
lmp_chunks_to_tsv.py ./output-45M/temps10_10K.out | tsv_plot_chunks.py -o temps.png -r 300 -1 --yl "Temp [K]" --xl "Z [A]" --avg-every 10 --yr 450 550 --xr 0 40 --plot-every 50 -v 0 2 '#c7d9e8' -v 4 16 0.90 -v 18 22 '#f6d5ac' -v 24 36 0.9 -v 38 40 '#c7d9e8' --chunksize 6.029 --fit 24.1 96.5 --fit 144.7 217.0 && open temps.png
```
Temp profiles look ok starting at 5M?

Look at temperature profiles from right before heat sources / sinks are applied:

```bash
lmp_chunks_to_tsv.py  ./output-45M/temps10_10K.out | tsv_plot_chunks.py -o temps-ss.png -r 200 800 --yl "Temp [K]" --xl "Z [A]" --avg-every 10 --yr 450 550 --xr 0 40 --plot-every 5 -v 0 2 '#c7d9e8' -v 4 16 0.90 -v 18 22 '#f6d5ac' -v 24 36 0.9 -v 38 40 '#c7d9e8' --chunksize 6.029 --fit 24.1 96.5 --fit 144.7 217.0 && open temps-ss.png
```

...maybe... the first 1M timesteps isn't steady state, but it looks like it is already averaged out when you look at the 5M timestep averages.


```bash
lmp_avgs_to_tsv.py ./output-45M/J1_10K.out ./output-90M/J1_10K.out ./output-135M/J1_10K.out ./output-180M/J1_10K.out ./output-200M/J1_10K.out ./output-245M/J1_10K.out  | awk 'BEGIN {OFS = "\t"}; {print $1, $2-$11, $3-$12-($2-$11), $4-$13-($2-$11), $5-$14-($2-$11), $6-$15-($2-$11), $7-$16-($2-$11), $8-$17, $9-$18, $10-$19, $3+$4+$5+$6+$7-4*$2-($12+$13+$14+$15+$16-4*$11), $3+$4+$8+$9+$10-$2-($12+$13+$17+$18+$19-$11);}' | tsv_eq_trends.py -c 1 "CV_KEPE" -c 2 "CV_p" -c 3 "CV_b" -c 4 "CV_a" -c 5 "CV_d" -c 6 "CV_i" -c 7 "CV_ai" -c 8 "CV_di" -c 9 "CV_ii" -c 10 "CV_o" -c 11 "CV_i" -n 7800 -s 800 | less -S
```

Much greater swings here of around 35% for angle and 31% for dihedral indicate we could run this for longer to get better results.


## Green-Kubo analysis

to get pressure for gk analysis:

```bash
for dir in `ls ./`; do
  echo "$dir"
  lmp_log_to_tsv.py $dir/output/log.lammps | tsv_stats.py -r 212 1712 -c 1 timestep -c 3 temp -c 4 pressure -c 5 density
done | grep 8555000
```

to create input files for thermal_conductivity_via_acf.py script (the tail just eliminates the header)
from the file):

```bash
mkdir -p acf_outputs
mkdir -p acf_outputs/original

for filename in `ls c8h18-octane-emd-gk-*/output/J0Jt_*.dat`; do
  echo "$filename => ${filename//\//-}"
  tail -n 100000 $filename > ./acf_outputs-17/original/${filename//\//-}
done

mkdir -p acf_outputs/corrected
for filename in `ls c8h18-octane-emd-gk-*/output/J0Jti_*.dat`; do
  echo "$filename => ${filename//\//-}"
  tail -n 100000 $filename > ./acf_outputs-17/corrected/${filename//\//-}
done
```
to verify that the top and bottom are both chosen correctly
```bash
for filename in `ls */output/J0Jt_*.dat`; do
  echo "$filename => ${filename//\//-}"
  tail -n 100000 $filename | head -n 3
  tail -n 100000 $filename | tail -n 3
done
```

then run thermal_conductivity_via_acf.py

## Octane NEMD at 345K for thermal conductivity

```bash
lmp_chunks_to_tsv.py  ./output/temps10_10K.out | tsv_plot_chunks.py -o temps.png -r 1000 -1 --yl "Temp [K]" --xl "Z [A]" --avg-every 50 --yr 300 400 --xr 0 40 --plot-every 70 -v 0 2 '#c7d9e8' -v 4 16 0.90 -v 18 22 '#f6d5ac' -v 24 36 0.9 -v 38 40 '#c7d9e8' --chunksize 4.30675 --fit 17.2 68.9 --fit 103.4 155.0 && open temps.png
```

```bash
 lmp_avgs_to_tsv.py ./output/J1_10K.out | awk 'BEGIN {OFS = "\t"}; {print $1, $2-$11, $3-$12-($2-$11), $4-$13-($2-$11), $5-$14-($2-$11), $6-$15-($2-$11), $7-$16-($2-$11), $8-$17, $9-$18, $10-$19, $3+$4+$5+$6+$7-4*$2-($12+$13+$14+$15+$16-4*$11), $3+$4+$8+$9+$10-$2-($12+$13+$17+$18+$19-$11);}' | tsv_eq_trends.py -c 1 "CV_KEPE" -c 2 "CV_p" -c 3 "CV_b" -c 4 "CV_a" -c 5 "CV_d" -c 6 "CV_i" -c 7 "CV_ai" -c 8 "CV_di" -c 9 "CV_ii" -c 10 "CV_orig" -c 11 "CV_corr" -n 500 -s 800 | less -S
```


## Octane NEMD at 345K for thermal conductivity–small gradient

```bash
lmp_chunks_to_tsv.py ./output-45M/temps10_10K.out ./output-90M/temps10_10K.out | tsv_plot_chunks.py -o temps.png -r 1000 -1 --yl "Temp [K]" --xl "Z [A]" --avg-every 100 --yr 325 365 --xr 0 40 --plot-every 80 -v 0 2 '#c7d9e8' -v 4 16 0.90 -v 18 22 '#f6d5ac' -v 24 36 0.9 -v 38 40 '#c7d9e8' --chunksize 4.30675 --fit 17.2 68.9 --fit 103.4 155.0 && open temps.png
```

## Octane NEMD at 345K for thermal conductivity–small-100 gradient

```bash
lmp_chunks_to_tsv.py ./output/temps10_10K.out | tsv_plot_chunks.py -o temps.png -r 1000 -1 --yl "Temp [K]" --xl "Z [A]" --avg-every 100 --yr 340 345 --xr 0 40 --plot-every 70 -v 0 2 '#c7d9e8' -v 4 16 0.90 -v 18 22 '#f6d5ac' -v 24 36 0.9 -v 38 40 '#c7d9e8' --chunksize 4.30675 --fit 17.2 68.9 --fit 103.4 155.0 && open temps.png
```
