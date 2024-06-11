# hacky parent directory import 
import os, sys
os.chdir(os.path.dirname(__file__))
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

# run example
from placement import terrain_from_parts 
terrain_from_parts("13tiles.png", "48tiles.png")

