"""
Python script to create n chairs in Onshape using the Python-API OnPy.
More about OnPy: https://github.com/kyle-tennison/onpy/blob/main/guide.md

The script creates chairs, made up of 4 legs, a seat and a back.

Author: Johanne Glende
Date: Spring 2025
Master thesis DPP, NTNU
"""

import random
import json
from chair_factory import create_chair_in_onshape


def generate_n_chairs(n):
    chairs = []
    for i in range(1, n + 1):
        document_name = f"generated_chair_{i}"
        # Generate random but reasonable sizes for variety
        height_legs = random.uniform(40, 70) / 2.54  # cm to inch
        width_leg = random.uniform(5, 10) / 2.54
        height_back = random.uniform(30, 60) / 2.54

        info = create_chair_in_onshape(document_name, height_legs, width_leg, height_back)
        info["height_legs"] = height_legs
        info["width_leg"] = width_leg
        info["height_back"] = height_back
        chairs.append(info)
        print(f"Created {document_name}: {info}")

if __name__ == "__main__":
    n = 1 # number of chairs to generate
    generate_n_chairs(n)
    """
    Note: A larger nummber than 15 will result in an OnPyApiError: Bad response: 429 Too Many Requests
    This is due to the OnPy API rate limit.
    """