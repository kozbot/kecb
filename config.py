

UNITS_PER_BLOCK = UPB = 20.0  # Drawing in a 20x20 grid
BLOCK_SIZE = 1.0 / 8.0  # Imperial - 1/8"
UNIT_SCALE = BLOCK_SIZE / UPB


# Disable text when generating images
# It messes with the extents during autogeneration
DISABLE_TEXT = False

STANDARD_LINETYPES = [
    ('DOT',
        'DOTTED 1.0 .  .  .  .  .  .  .  .  .',
        [UNIT_SCALE * 2, 0.0, -UNIT_SCALE * 2]),
    ('DOTX2',
        'DOTTED 2.0 .     .     .     .     .',
        [UNIT_SCALE * 4, 0.0, -UNIT_SCALE * 4]),
    ('DOT2 ',
        'DOTTED 1/2 . . . . . . . . . . . . .',
        [UNIT_SCALE * 1, 0.0, -UNIT_SCALE * 1]),
]
