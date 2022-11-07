import mobie


ds_folder = "./data/example-dataset"


sources = [
    [f"nuclei-C01_{i}", f"segmentation-nuclei-C01_{i}"] for i in range(9)
]
display_groups = {
    f"nuclei-C01_{i}": "nuclei" for i in range(9)
}
display_groups.update({
    f"segmentation-nuclei-C01_{i}": "segmentation-nuclei" for i in range(9)
})

display_group_settings = {
    "nuclei": {
        "color": "blue",
        "contrastLimits": [
          567.7193774414062,
          1821.85587890625
        ],
        "opacity": 1.0,
        "visible": True
    },
    "segmentation-nuclei": {
        "lut": "glasbey",
        "opacity": 0.5,
        "showTable": False,
        "visible": False
    },
}


mobie.create_grid_view(
    dataset_folder=ds_folder, view_name="single_well", sources=sources,
    display_groups=display_groups, use_transformed_grid=False,
    display_group_settings=display_group_settings,
    overwrite=True,
)
