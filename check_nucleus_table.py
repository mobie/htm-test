import os

import mobie
import napari
import numpy as np
import pandas as pd
import zarr

DATA_ROOT = "../../data/mobie/mobie_htm_project/data/example-dataset/images/ome-zarr"
TABLE_ROOT = "./data/example-dataset/tables"


def check_table(seg_name):
    data_path = os.path.join(DATA_ROOT, f"{seg_name}.ome.zarr")
    table_path = os.path.join(TABLE_ROOT, f"{seg_name}/default.tsv")

    with zarr.open(data_path, "r") as f:
        mscales = f.attrs["multiscales"][0]
        resolution = mscales["datasets"][0]["coordinateTransformations"][0]["scale"]

        ds = f["s0"]
        shape = ds.shape

        data = ds[:]

    print(shape)
    print(resolution)

    table = pd.read_csv(table_path, sep="\t")
    anchor_x = table["anchor_x"].values
    anchor_y = table["anchor_y"].values
    print(anchor_x.min(), anchor_x.max())
    print(anchor_y.min(), anchor_y.max())

    points = np.array([
        [py, px] for py, px in zip(anchor_y, anchor_x)
    ])

    v = napari.Viewer()
    v.add_labels(data, scale=resolution)
    v.add_points(points)
    napari.run()


def rescale_table(table_path, resolution):
    table = pd.read_csv(table_path, sep="\t")
    for col in ["anchor_y", "bb_min_y", "bb_max_y"]:
        table[col] *= resolution[0]
        table[col] *= resolution[0]
    for col in ["anchor_x", "bb_min_x", "bb_max_x"]:
        table[col] *= resolution[1]
        table[col] *= resolution[1]
    table.to_csv(table_path, sep="\t", index=False, na_rep="nan")


def rescale_tables():
    sources = mobie.metadata.read_dataset_metadata("./data/example-dataset")["sources"]
    for name, source in sources.items():
        if next(iter(source)) != "segmentation":
            continue
        table_path = os.path.join(TABLE_ROOT, name, "default.tsv")
        data_path = os.path.join(DATA_ROOT, f"{name}.ome.zarr")
        with zarr.open(data_path, "r") as f:
            mscales = f.attrs["multiscales"][0]
            resolution = mscales["datasets"][0]["coordinateTransformations"][0]["scale"]

        rescale_table(table_path, resolution)


def main():
    # rescale_tables()
    check_table("segmentation-nuclei-C01_0")


if __name__ == "__main__":
    main()
