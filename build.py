# build.py
import bz2
import os
from urllib.request import urlretrieve
from hatchling.builders.hooks.plugin.interface import BuildHookInterface

MODEL_CAPACITIES = ["tiny", "small", "medium", "large", "full"]
BASE_URL = "https://github.com/marl/crepe/raw/models/"


class CustomBuildHook(BuildHookInterface):
    """Download and decompress CREPE model weights during wheel build."""

    def initialize(self, version: str, build_data: dict) -> None:
        for capacity in MODEL_CAPACITIES:
            weight_file = f"model-{capacity}.h5"
            weight_path = os.path.join("crepe", weight_file)

            if os.path.isfile(weight_path):
                continue

            compressed_file = weight_file + ".bz2"
            compressed_path = os.path.join("crepe", compressed_file)

            if not os.path.isfile(compressed_path):
                print(f"Downloading {compressed_file} ...")
                urlretrieve(BASE_URL + compressed_file, compressed_path)

            print(f"Decompressing {compressed_file} ...")
            with bz2.BZ2File(compressed_path, "rb") as source:
                with open(weight_path, "wb") as target:
                    target.write(source.read())
            print(f"Decompressed {weight_file}")

            # clean up compressed file after decompression
            os.remove(compressed_path)
