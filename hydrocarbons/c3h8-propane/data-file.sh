#!/bin/bash

packmol < propane.packmol

vmd -e vmd-propane.tcl
