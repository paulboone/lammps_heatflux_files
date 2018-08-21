

rsync -r --exclude=".*" * h2p:lammpshf/i1/


## run simulations in dir

```
for simdir in `ls ./`; do
  echo "$simdir"
  cd $simdir
  sbatch < c8h18-octane.slurm
  cd ..
done

```
