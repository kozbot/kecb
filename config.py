

UNITS_PER_BLOCK = UPB = 20.0  # Drawing in a 20x20 grid
BLOCK_SIZE = 1.0 / 8.0  # Imperial - 1/8"
UNIT_SCALE = BLOCK_SIZE / UPB
POLE_OFFSET = -2 * UPB


# Disable text when generating images
# It messes with the extents during autogeneration
DISABLE_TEXT = False
