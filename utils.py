import config


# Convert blocks to units
def btu(block):
    return block * config.UNITS_PER_BLOCK
