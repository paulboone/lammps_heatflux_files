#!/bin/bash

packmol < octane.packmol

vmd -e vmd-octane.tcl
