import string
from mobie import htm

dataset_folder = "./data/example-dataset"
max_jobs = 4


# extract the site name (= Well name and position in well for an image)
# here, the site name comes in the source name after the source prefix, i.e.
# source_name = f"{prefix}_{site_name}"
def to_site_name(source_name, prefix):
    return source_name[(len(prefix) + 1):]


# extract the well name from the site name.
# here, the site name consists of well name and position in the well, i.e.
# source_name = f"{well_name}_{position_in_well}"
def to_well_name(site_name):
    return site_name.split("_")[0]


# map the well name to its position in the 2d grid
# here, the Wells are called C01, C02, etc.
def to_position(well_name):
    r, c = well_name[0], well_name[1:]
    r = string.ascii_uppercase.index(r)
    c = int(c) - 1
    return [c, r]


source_types = ["image", "segmentation"]
source_prefixes = ["nuclei", "segmentation-nuclei"]

# specifiy the settings for all the sources
source_settings = [
    # nucleus channel: color blue
    {"color": "blue", "contrastLimits": [570, 1870], "visible": True},
    {"lut": "glasbey", "visible": False, "showTable": False},
]

# crate the plate grid view
htm.add_plate_grid_view(dataset_folder, view_name="simple-grid",
                        source_prefixes=source_prefixes, source_types=source_types, source_settings=source_settings,
                        source_name_to_site_name=to_site_name, site_name_to_well_name=to_well_name,
                        well_to_position=to_position, site_table="sites", well_table="wells",
                        sites_visible=False, menu_name="bookmark")
