## generating random numbers for lammps velocities.

Sometimes too high numbers fail; so far this seems to work though:
```python
int(random.random()*66752864)
```

rsync -r --exclude=".*" * h2p:lammpshf/i1/


## run simulations in dir

```bash
for simdir in `ls ./`; do
  echo "$simdir"
  cd $simdir
  sbatch < c8h18-octane.slurm
  cd ..
done

for simdir in `ls | grep c8h18-octane-emd-gk-..`; do
  echo "$simdir"
  cd $simdir
  sbatch < c8h18-octane.slurm
  cd ..
done
```

## rsync selected directories

```bash
for simdir in `ls | grep c8h18-octane-emd-gk-..`; do
  rsync -av $simdir h2p:lammpshf/c8h18-octane-emd-gk-72C-40A-5t/
done

for simdir in `echo "c8h18-octane-emd-gk-10 c8h18-octane-emd-gk-11 c8h18-octane-emd-gk-12 c8h18-octane-emd-gk-13 c8h18-octane-emd-gk-14 c8h18-octane-emd-gk-15 c8h18-octane-emd-gk-16 c8h18-octane-emd-gk-17" | xargs`; do
  rsync -av h2p:lammpshf/c8h18-octane-emd-gk-72C-40A-5t/$simdir ./
done
```
