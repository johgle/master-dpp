"""
Python script to create a chair in Onshape using the Python-API OnPy.
More about OnPy: https://github.com/kyle-tennison/onpy/blob/main/guide.md

The script creates a simple chair, made up of 4 legs, a seat and a back.

Author: Johanne Glende
Date: Spring 2025
Master thesis DPP, NTNU
"""

import onpy

# Params - the unit is by default [inch] so we must use inch/2.54 to convert to cm.
origo = (0,0)
width_leg = 7/2.54  # 7 inch / 2.54 inch/cm = 2.76 inch
total_width_chair = 52/2.54

height_legs = 46/2.54
height_back = 48/2.54
height_seat = 5/2.54
thickness_back = 5/2.54
height_back_rods = 10/2.54
height_back_plate = 6/2.54

# Get document and partstudio to work in
document = onpy.get_document(name = "chair001")
partstudio = document.get_partstudio()
partstudio.wipe()

# -- LEGS --
# create a new sketch for legs, select which plane it is based in
base_sketch = partstudio.add_sketch(
    plane = partstudio.features.top_plane, name="Base Bottom Sketch")

# Then, we'll add 4 squares to it.
# The sketch will be made up by the four squares.
base_sketch.add_corner_rectangle(corner_1 = (0,0), corner_2=(width_leg,width_leg))
base_sketch.add_corner_rectangle(corner_1 = (0,total_width_chair-width_leg), corner_2=(width_leg,total_width_chair))
base_sketch.add_corner_rectangle(corner_1 = (total_width_chair-width_leg,0), corner_2=(total_width_chair,width_leg))
base_sketch.add_corner_rectangle(corner_1 = (total_width_chair-width_leg, total_width_chair-width_leg), corner_2=(total_width_chair,total_width_chair))

# We'll create a new extrude feature, raising the box
extrude = partstudio.add_extrude(
    faces=base_sketch,  # we'll extrude the entire sketch we created
    distance=height_legs,  # then, we'll extrude this by the given height
    name = "Legs"
)

# -- SEAT --
# create a new plane for where the seating will be
seating_plane = partstudio.add_offset_plane(
    target=partstudio.features.top_plane, distance=height_legs,
    name="Seating Plane"
)

# create a new sketch for seating, select which plane it is based in, here: seating_plane
seating_sketch = partstudio.add_sketch(
    plane = seating_plane, name="Seating Sketch")

seating_sketch.add_corner_rectangle(corner_1 = (0,0), corner_2=(total_width_chair, total_width_chair))

# extrude the seating plate
extrude = partstudio.add_extrude(
    faces = seating_sketch,
    distance = height_seat,
    name = "Seating"
)

# -- BACK --

# create a new sketch for the back.
# We need a new sketch because it is the "whole sketch" we are extruding.

back_plane = partstudio.add_offset_plane(
    target = partstudio.features.front_plane, distance = -total_width_chair,
    name = "Back Plane"
)

# create a sketch where we will draw the back
back_sketch = partstudio.add_sketch(
    plane = back_plane, name = "Back Sketch"
)

#draw the back of the chair
back_sketch.add_corner_rectangle(corner_1 = (0, height_legs+height_seat), corner_2 = (total_width_chair, height_legs+height_seat+height_back))

# extrude the back of the chair
extrude_back = partstudio.add_extrude(
    faces = back_sketch,
    distance = thickness_back,
    name = "Back"
)

# # create a new sketch for the two rods extruding the back.
# back_rods_plane = partstudio.add_offset_plane(
#     target = partstudio.features.top_plane, distance = height_legs + height_seat,
#     name = "Back_rods Plane"
# )

# # create a sketch where we will draw the back
# back_rods_sketch = partstudio.add_sketch(
#     plane = back_rods_plane, name = "Back rods Sketch"
# )

# #draw the back of the chair
# back_rods_sketch.add_corner_rectangle(corner_1 = (2,10), corner_2=(3,11))
# back_rods_sketch.add_corner_rectangle(corner_1 = (9,10), corner_2=(10,11))

# # extrude the back of the chair
# extrude_back = partstudio.add_extrude(
#     faces = back_rods_sketch,
#     distance = height_back_rods,
#     name = "Back_rods"
# )

# # create backplate, first the plane
# back_plate_plane = partstudio.add_offset_plane(
#     target = back_rods_plane, distance = height_back_rods - height_back_plate + 2,
#     name = "Back plate Plane"
# )

# back_plate_sketch = partstudio.add_sketch(
#     plane = back_plate_plane, name = "Back Plate Plane"
# )

# # draw the back plates rectangle.
# back_plate_sketch.add_corner_rectangle(corner_1 = (0.5,9.5), corner_2=(11.5,11.5))

# # extrude the backplate
# extrude_back = partstudio.add_extrude(
#     faces = back_plate_sketch,
#     distance = height_back_plate,
#     name = "Back_plate"
# )

# ###OLD BACK:
# # create a new sketch for the back.
# # We need a new sketch because it is the "whole sketch" we are extruding.

# back_plane = partstudio.add_offset_plane(
#     target = partstudio.features.front_plane, distance = -12,
#     name = "Back Plane"
# )

# # create a sketch where we will draw the back
# back_sketch = partstudio.add_sketch(
#     plane = back_plane, name = "Back Sketch"
# )

# #draw the back of the chair
# back_sketch.add_corner_rectangle(corner_1 = (0, height_legs+height_seat), corner_2 = (12, height_legs+height_seat+height_back))

# # extrude the back of the chair
# extrude_back = partstudio.add_extrude(
#     faces = back_sketch,
#     distance = thickness_back,
#     name = "Back"
# )