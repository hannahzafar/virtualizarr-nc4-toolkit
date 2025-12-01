#!/usr/bin/env python

from pathlib import Path

# from virtualizarr_nc4_toolkit.utils import find_directory_files
from virtualizarr_nc4_toolkit.virtualize import create_vzarr_store

# Path test?
# NOTE: I can't get my find_directory_files to work, because I just want to grab all .nc4 files in a glob directory. Oh well
# micasa_test = Path("micasa-data/daily/2001/").glob("*")
# list = find_directory_files(micasa_test)

# Have to use absolute paths
micasa_path = "/css/gmao/geos_carb/pub/MiCASA/v1/netcdf/"
micasa_test = sorted(list(Path(f"{micasa_path}daily/2001/").glob("*/*.nc4")))
# print(*micasa_test, sep="\n")
# print(len(micasa_test))
create_vzarr_store("micasa_test", micasa_test)
