#!/bin/bash

packmol < hexadecane.packmol

vmd -e vmd-lammps.tcl
