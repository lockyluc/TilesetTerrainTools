import os
from PIL import Image  
import warnings

def terrain_from_parts(part_file : str, output_file :str = ""):
    
    # open image 
    img = Image.open(part_file)
    w,h = img.size
    if w % 5 != 0 or h % 3 != 0:
        warnings.warn(f"Image '{part_file}' has invalid shape.\nMust match 5W x 3H, got {w}x{h} instead.")

    # get resolution
    W = w // 5; H = h // 3
    print(f"Input part resolution {W}x{H}")

    # read 13 terrain parts ( 3x3 + 2x2 = 13 parts)
    parts = []
    for idx in range(9):
        i = idx%3 ; j = idx // 3
        parts.append( img.crop(( W*i,H*j, W*(i+1),H*(j+1))) )
    for idx in range(4):
        i = idx % 2 ; j = idx // 2
        parts.append( img.crop(( W*(i+3),H*(j+1),  W*(i+4), H*(j+2) )) )

    # output corners and sides terrain (with 3x3 peer bits)
    out = Image.new(img.mode, (2*W*12, 2*H*4)) 
    arrangements = [
        [0,2,3,5],
        [3,5,3,5],
        [3,5,6,8],
        [0,2,6,8],

        [0,1,3,9],
        [3,11,3,9],
        [3,11,6,7],
        [0,1,6,7],

        [1,1,10,9],
        [12,11,10,9],
        [12,11,7,7],
        [1,1,7,7],

        [1,2,10,5],
        [12,5,10,5],
        [12,5,7,8],
        [1,2,7,8],

        [4,11,10,9],
        [3,11,3,4],
        [3,4,3,9],
        [12,11,4,9],

        [1,1,10,4],
        [12,4,4,4],
        [4,4,10,4],
        [12,4,7,7],

        [1,1,4,9],
        [4,11,4,4],
        [4,4,4,9],
        [4,11,7,7],

        [12,4,10,9],
        [12,5,4,5],
        [4,5,10,5],
        [12,11,10,4],

        [0,1,3,4],
        [3,4,3,4],
        [12,4,10,4],
        [3,4,6,7],

        [12,11,4,4],
        [12,4,4,9],
        [4,4,4,4],
        [4,4,7,7],

        [1,1,4,4],
        [9,10,11,12],
        [4,11,10,4],
        [4,4,10,9],
        
        [1,2,4,5],
        [4,11,4,9],
        [4,5,4,5],
        [4,5,7,8]
    ]
    for tile_idx,arrangement in enumerate(arrangements):
        tile_i = tile_idx // 4 ; tile_j = tile_idx % 4
        for part_idx in range(4):
            part_i = part_idx % 2 ; part_j = part_idx // 2
            x = W*(2*tile_i+part_i)
            y = H*(2*tile_j+part_j)
            out.paste(parts[arrangement[part_idx]], (x,y) )

    # save to file
    if output_file == "":
        name, ext = os.path.splitext(part_file)
        output_file = name + ".terrain" + ext 
    print(f"Saving to {output_file}")
    out.save(output_file)

