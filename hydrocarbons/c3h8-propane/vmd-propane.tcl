package require topotools
package require pbctools

mol new propane_packed.xyz autobonds no waitfor all

set sel_ch3 [atomselect top "type H"]
set sel_ch2 [atomselect top "type He"]

$sel_ch3 set name "CH3"
$sel_ch3 set type "CH3"
$sel_ch3 set mass 15.035
$sel_ch3 set radius 1.3

$sel_ch2 set name "CH2"
$sel_ch2 set type "CH2"
$sel_ch2 set mass 14.027
$sel_ch2 set radius 1.3

mol bondsrecalc top
topo guessangles
topo guessdihedrals
mol reanalyze top

pbc set {19.38 19.38 129.22 90.0 90.0 90.0}
topo writelammpsdata propane.data full

exit 0
