import onpy

def create_chair_in_onshape(document_name, height_legs, width_leg, height_back):
    # Default values for other parameters
    total_width_chair = 52/2.54
    height_seat = 5/2.54
    thickness_back = 5/2.54

    # Create new document
    document = onpy.create_document(document_name)
    partstudio = document.get_partstudio()

    # -- LEGS --
    base_sketch = partstudio.add_sketch(
        plane=partstudio.features.top_plane, name="Base Bottom Sketch")
    base_sketch.add_corner_rectangle(corner_1=(0,0), corner_2=(width_leg,width_leg))
    base_sketch.add_corner_rectangle(corner_1=(0,total_width_chair-width_leg), corner_2=(width_leg,total_width_chair))
    base_sketch.add_corner_rectangle(corner_1=(total_width_chair-width_leg,0), corner_2=(total_width_chair,width_leg))
    base_sketch.add_corner_rectangle(corner_1=(total_width_chair-width_leg, total_width_chair-width_leg), corner_2=(total_width_chair,total_width_chair))
    partstudio.add_extrude(faces=base_sketch, distance=height_legs, name="Legs")

    # -- SEAT --
    seating_plane = partstudio.add_offset_plane(
        target=partstudio.features.top_plane, distance=height_legs, name="Seating Plane")
    seating_sketch = partstudio.add_sketch(
        plane=seating_plane, name="Seating Sketch")
    seating_sketch.add_corner_rectangle(corner_1=(0,0), corner_2=(total_width_chair, total_width_chair))
    partstudio.add_extrude(faces=seating_sketch, distance=height_seat, name="Seating")

    # -- BACK --
    back_plane = partstudio.add_offset_plane(
        target=partstudio.features.front_plane, distance=-total_width_chair, name="Back Plane")
    back_sketch = partstudio.add_sketch(
        plane=back_plane, name="Back Sketch")
    back_sketch.add_corner_rectangle(
        corner_1=(0, height_legs+height_seat),
        corner_2=(total_width_chair, height_legs+height_seat+height_back))
    partstudio.add_extrude(faces=back_sketch, distance=thickness_back, name="Back")

    return {
        "document_name": document_name,
    }
