"""
Create a virtualized dataset reference parquet from a list of Path filepaths at the current working directory
"""

from obstore.store import LocalStore
from virtualizarr import open_virtual_mfdataset
from virtualizarr.parsers import HDFParser
from virtualizarr.registry import ObjectStoreRegistry
from pathlib import Path
# import pandas as pd

# Ignore warnings that do not apply to our use case
import warnings

warnings.filterwarnings(
    "ignore",
    message="Numcodecs codecs are not in the Zarr version 3 specification*",
    category=UserWarning,
)


# NOTE: I'm getting rid of this for now
# # Function for debugging compression info mismatch
# def get_codec_info(path):
#     """Extract compression info from the first dataset in a NetCDF file.
#     Args:
#         path (Path object): Path to .nc4 file
#
#     Returns:
#         info (dict): filename, compression, and shuffle information
#
#     """
#     info = {"file": str(path), "compression": None, "shuffle": None}
#     try:
#         with h5py.File(path, "r") as f:
#             for name, dset in f.items():
#                 if isinstance(dset, h5py.Dataset):
#                     info["variable_checked"] = name
#                     info["compression"] = dset.compression
#                     info["shuffle"] = dset.shuffle
#                     break
#     except Exception:
#         # TODO: Check for valid .nc4 (or just HDF5?) AND WITH data variables (returns empty if no vars but still valid file)
#         raise
#     return info


def create_vzarr_store(store_name, filepaths):
    """create virtual Zarr stores for lists of .nc4 filepaths.
    # (Only one) Creates 1 store if all uniform compression types or a store for each compression type.

    Args:
        store_name (str): name of store to be created
        filepaths (list): list of filepath Path objects returned in find_directory_files

    Returns:
        Path to virtual store

    """
    # Create a path for the vzarr store
    vstore_path = Path.cwd() / f"{store_name}"
    # vstore_path.mkdir(exist_ok=True)
    vstore_path.mkdir()

    # Build registry dict over all unique parent dirs in filepaths
    registry_map = {}
    for file in filepaths:
        dir_path = file.parent
        prefix = dir_path.as_uri() + "/"
        if prefix not in registry_map:
            registry_map[prefix] = LocalStore(prefix=dir_path)

    # This differs from VZarr2 documentation in that the filepath and the store are in separate directories: registers source dir as a file:// prefix and creates a LocalStore for that source directory
    registry = ObjectStoreRegistry(registry_map)

    file_urls = [file.as_uri() for file in filepaths]

    # Debugging for compression mismatch
    try:
        vds = open_virtual_mfdataset(
            urls=file_urls,
            parser=HDFParser(),
            registry=registry,
            # loadable_variables=['time'],
            # decode_times=True,
        )
        vds.vz.to_kerchunk(f"{vstore_path.name}/vstore.parquet", format="parquet")

        # NOTE: Returns the path to the virtualized dataset
        print(f"Created virtual Zarr store at {vstore_path}")

        return f"{vstore_path.name}/vstore.parquet"

    # Handle compression mismatch
    # except NotImplementedError as e:
    #     if (
    #         "ManifestArray class cannot concatenate arrays which were stored using different codecs"
    #         in str(e)
    #     ):
    #         print(f"{e}")
    #
    #         print("\nChecking compression info for each file...")
    #         codecs = [get_codec_info(file) for file in filepaths]
    #         codec_df = pd.DataFrame(codecs)  # Make a df of codec info
    #         codec_df = codec_df.fillna(
    #             {"compression": "None", "shuffle": False}
    #         )  # Fill Nonetype values
    #         print(codec_df[["compression", "shuffle"]].value_counts())
    #
    #         # Split into group of filses by compression
    #         groups = codec_df.groupby(["compression", "shuffle"])["file"].apply(list)
    #         vstore_list = []
    #         i = 1
    #         for multi_idx, filepaths in groups.items():
    #             # print(f"MultiIndex: {multi_idx}")
    #             file_urls = [Path(file).as_uri() for file in filepaths]
    #             vds = open_virtual_mfdataset(
    #                 urls=file_urls,
    #                 parser=HDFParser(),
    #                 registry=registry,
    #                 # loadable_variables=['time'],
    #                 # decode_times=True,
    #             )
    #             vstore_name = f"vstore{i}.parquet"
    #             vstore_list.append(vstore_name)
    #             vds.vz.to_kerchunk(
    #                 f"{vstore_path.name}/{vstore_name}", format="parquet"
    #             )
    #             i += 1
    #
    #         print(
    #             f"Created {len(vstore_list)} separate virtual Zarr stores per compression type at {vstore_path}"
    #         )
    #         return [f"{vstore_path.name}/{vstore}" for vstore in vstore_list]
    #
    #     else:
    #         raise
    #
    except Exception:
        raise
