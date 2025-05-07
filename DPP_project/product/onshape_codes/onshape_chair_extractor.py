# file: onshape_chair_extractor.py
"""
Light-weight helper for turning a handful of raw Onshape API responses
(requests.get(...).json()) into an easy-to-use Python object.

Author: <you>
"""

from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Any, Tuple, Optional


@dataclass
class MassVolume:
    mass: float        # kg   (Onshape returns an array – we take the first entry)
    volume: float      # m³   (same)
    density: Optional[float] = None  # kg/m³ – filled in if Onshape supplies it


@dataclass
class BoundingBox:
    min_corner: Tuple[float, float, float]  # (x, y, z)
    max_corner: Tuple[float, float, float]

    @property
    def size(self) -> Tuple[float, float, float]:
        """Overall (x-size, y-size, z-size)."""
        return tuple(h - l for l, h in zip(self.min_corner, self.max_corner))


class OnshapeChair:
    """
    Parse a minimal set of Onshape endpoints:

    *  /partstudios/.../massproperties?               -> partstudio_mass_json
    *  /parts/.../massproperties?                     -> part_mass_json
    *  /parts                                         -> parts_json   (for material & name)
    *  /partstudios/.../boundingboxes                 -> studio_bbox_json
    *  /partstudios/.../bodydetails                   -> body_details_json
    """

    # ------------- construction helpers -------------------------------------------------

    def __init__(
        self,
        *,
        partstudio_mass_json: Dict[str, Any],
        part_mass_json: Dict[str, Any],
        parts_json: List[Dict[str, Any]],
        studio_bbox_json: Dict[str, Any],
        body_details_json: Dict[str, Any],
    ):
        self._studio_mass_json = partstudio_mass_json
        self._part_mass_json = part_mass_json
        self._parts_json = parts_json
        self._studio_bbox_json = studio_bbox_json
        self._body_details_json = body_details_json

        # Build quick look-ups
        self._material_by_partid = {
            p["partId"]: p["material"]["displayName"] if p.get("material") else None
            for p in self._parts_json
        }
        self._name_by_partid = {p["partId"]: p["name"] for p in self._parts_json}

        # ---- pre-compute everything we need once ---------
        self.overall_massvol = self._parse_studio_mass()
        self.overall_bbox = self._parse_studio_bbox()
        self.part_massvol = self._parse_part_mass()
        self.part_bbox = self._parse_body_bboxes()

    # ------------- public API -----------------------------------------------------------

    # ----- 1. overall chair -------------------------------------------------------------
    def total_mass(self) -> float:
        return self.overall_massvol.mass

    def total_volume(self) -> float:
        return self.overall_massvol.volume

    def total_size(self) -> Tuple[float, float, float]:
        return self.overall_bbox.size

    def centroid(self) -> Tuple[float, float, float]:
        # extra convenience (not requested) – the nominal centroid
        return tuple(self._studio_mass_json["bodies"]["-all-"]["centroid"][:3])

    # ----- 2. per part / body -----------------------------------------------------------
    def part_ids(self) -> List[str]:
        return sorted(self.part_massvol.keys())

    def part_name(self, part_id: str) -> str:
        return self._name_by_partid.get(part_id, part_id)

    def part_material(self, part_id: str) -> Optional[str]:
        return self._material_by_partid.get(part_id)

    def part_mass(self, part_id: str) -> Optional[float]:
        mv = self.part_massvol.get(part_id)
        return mv.mass if mv else None

    def part_volume(self, part_id: str) -> Optional[float]:
        mv = self.part_massvol.get(part_id)
        return mv.volume if mv else None

    def part_size(self, part_id: str) -> Optional[Tuple[float, float, float]]:
        bbox = self.part_bbox.get(part_id)
        return bbox.size if bbox else None

    # ----- 3. one-stop summary ----------------------------------------------------------
    def summary(self) -> Dict[str, Any]:
        result = {
            "chair": {
                "mass_kg": self.total_mass(),
                "volume_m3": self.total_volume(),
                "size_m": self.total_size(),
            },
            "parts": {},
        }
        for pid in self.part_ids():
            result["parts"][pid] = {
                "name": self.part_name(pid),
                "material": self.part_material(pid),
                "mass_kg": self.part_mass(pid),
                "volume_m3": self.part_volume(pid),
                "size_m": self.part_size(pid),
            }
        return result

    # ------------- implementation details ----------------------------------------------

    def _parse_studio_mass(self) -> MassVolume:
        all_body = self._studio_mass_json["bodies"]["-all-"]
        # Onshape returns [nominal, min, max] – we take the first (nominal) entry
        return MassVolume(mass=all_body["mass"][0], volume=all_body["volume"][0])

    def _parse_studio_bbox(self) -> BoundingBox:
        j = self._studio_bbox_json
        return BoundingBox(
            min_corner=(j["lowX"], j["lowY"], j["lowZ"]),
            max_corner=(j["highX"], j["highY"], j["highZ"]),
        )

    def _parse_part_mass(self) -> Dict[str, MassVolume]:
        mv = {}
        for pid, body in self._part_mass_json["bodies"].items():
            mv[pid] = MassVolume(mass=body["mass"][0], volume=body["volume"][0])
        return mv

    def _parse_body_bboxes(self) -> Dict[str, BoundingBox]:
        # Build a bbox per body by unioning the face boxes
        per_body = defaultdict(
            lambda: {
                "min": [float("inf")] * 3,
                "max": [-float("inf")] * 3,
            }
        )
        for body in self._body_details_json["bodies"]:
            bid = body["id"]
            for face in body["faces"]:
                mn = face["box"]["minCorner"]
                mx = face["box"]["maxCorner"]
                for i in range(3):
                    per_body[bid]["min"][i] = min(per_body[bid]["min"][i], mn[i])
                    per_body[bid]["max"][i] = max(per_body[bid]["max"][i], mx[i])

        # Convert to nice objects
        return {
            bid: BoundingBox(tuple(v["min"]), tuple(v["max"])) for bid, v in per_body.items()
        }


# ------------------- example usage -----------------------------------------------------
if __name__ == "__main__":
    import json, pathlib

    # Folder where all the sample JSON files live
    data_dir = pathlib.Path(__file__).parent  # <- same folder as this script
    # If your files are elsewhere, point data_dir to that folder instead:
    # data_dir = pathlib.Path(r"C:\Users\Johanne\onshape_codes")

    files = {
        "partstudio_mass_json": json.load(
            open(data_dir / "CHAIR_onshape_data_url_partstudios_massproperties.json")
        ),
        "part_mass_json": json.load(
            open(data_dir / "CHAIR_onshape_data_url_part_massproperties.json")
        ),
        "parts_json": json.load(
            open(data_dir / "CHAIR_onshape_data_url_parts.json")
        ),
        "studio_bbox_json": json.load(
            open(data_dir / "CHAIR_onshape_data_url_partstudios_boundingboxes.json")
        ),
        "body_details_json": json.load(
            open(data_dir / "CHAIR_onshape_data_url_partstudios_bodydetails.json")
        ),
    }

    chair = OnshapeChair(**files)

    # Quick peek
    print("Overall chair:")
    print("  mass   :", chair.total_mass(), "kg")
    print("  volume :", chair.total_volume(), "m³")
    print("  size   :", chair.total_size(), "m")

    print("\nParts:")
    for pid in chair.part_ids():
        print(
            f"  {pid:>4} | {chair.part_name(pid):<12} "
            f"| {str(chair.part_material(pid)):<10} "
            f"| {chair.part_mass(pid):>7.3f} kg "
            f"| {chair.part_size(pid)} m"
        )