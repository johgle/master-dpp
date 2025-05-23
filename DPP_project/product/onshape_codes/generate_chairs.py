import random
import json
from chair_factory import create_chair_in_onshape


def generate_n_chairs(n):
    chairs = []
    for i in range(16, n + 16):
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

    # Save to JSON
    with open("generated_chairs.json", "w") as f:
        json.dump(chairs, f, indent=2)
    print("Saved all chair info to generated_chairs.json")

if __name__ == "__main__":
    generate_n_chairs(1)
    """
    Note: A larger nummber than 15 will result in an OnPyApiError: Bad response: 429 Too Many Requests
    This is due to the OnPy API rate limit.
    """