# Where are the symbols?

They are generated in the ./dxf folder when the script is run.  See 'img' folder for examples.

# Design:

Symbols are drawn by default where 1 block = 20 units x 20 units = 1/8" x 1/8"

# Purpose:

This program is itended to bootstrap an electrical CAD symbol library by generating common symbols in .dxf format. The symbols are all aligned to a common 2D grid and have a consistent style.  Since they are generated using common building blocks a change to how a Normally Open contact is drawn will require (if kept to the same block dimensions) no changes to the rest of the library and it can easily be proliferated throughout.
