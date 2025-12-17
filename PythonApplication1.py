import nbtlib
import numpy as np
import os
from datetime import datetime

# 設定
SCHEM_FILE = "Floor1.schem"

def block_to_id(block_name, block_properties=None):

    # 階段チェック
    if 'spruce_stairs' in block_name:
        if block_properties is not None:
            facing = block_properties.get('facing')
            half = block_properties.get('half')
            
            # half=bottom (下付き) : 東西南北
            if half == 'bottom':
                if facing == 'east': return 5
                elif facing == 'west': return 6
                elif facing == 'south': return 7
                elif facing == 'north': return 8
            # half=top (上付き) : 東西南北
            elif half == 'top':
                if facing == 'east': return 9
                elif facing == 'west': return 10
                elif facing == 'south': return 11
                elif facing == 'north': return 12
        return 5  # デフォルト
    
    if 'spruce_planks' in block_name: return 1
    if 'dark_oak_log' in block_name: return 2
    if 'dark_oak_planks' in block_name: return 3
    if 'birch_planks' in block_name: return 4

    if 'dark_oak_door' in block_name: return 13
    if 'dark_oak_fence' in block_name: return 14
    if 'air' in block_name: return 0
    
    return 99

# Schematic読み込み
print(f"読み込み: {SCHEM_FILE}")
schem_file = nbtlib.load(SCHEM_FILE)
schem = schem_file['Schematic']
width, height, length = int(schem['Width']), int(schem['Height']), int(schem['Length'])
print(f"サイズ: {width}x{height}x{length}\n")

# パレット→IDマップ
palette = schem.get('Blocks', {}).get('Palette', {})
block_id_map = {}

if palette:
    for name, idx in palette.items():
        props = {}
        if '[' in name and ']' in name:
            props_str = name[name.find('[')+1:name.find(']')]
            for prop in props_str.split(','):
                if '=' in prop:
                    key, value = prop.split('=')
                    props[key] = value
        
        block_id = block_to_id(name, props)
        idx_int = int(idx)
        block_id_map[idx_int] = block_id
        
        # spruce_stairsはログ出力
        if 'spruce_stairs' in name:
            half = props.get('half', 'unknown')
            facing = props.get('facing', 'unknown')
            print(f"📍 {name}")
            print(f"   half={half}, facing={facing} → ID: {block_id}")
    
    print(f"\nブロックマップ生成完了")
else:
    print("⚠️ Palette が見つかりません")

# Blocks解凍
blocks_data = schem.get('Blocks', {}).get('Data')
if blocks_data is None:
    print("❌ エラー: Data が見つかりません")
    exit(1)

blocks = np.array(blocks_data, dtype=np.int32)

# 縦x横x高さ配列生成
level_map = np.zeros((length, width, height), dtype=int)

for y in range(height):
    for z in range(length):
        for x in range(width):
            idx = y * (length * width) + z * width + x
            if idx < len(blocks):
                block_idx = int(blocks[idx])
                block_id = block_id_map.get(block_idx, 99)
                level_map[z][x][y] = block_id

# ファイル名から配列名を生成
base_name = os.path.splitext(os.path.basename(SCHEM_FILE))[0].lower()

# タイムスタンプを取得
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Cヘッダ出力
with open("levelmap.h", "w", encoding="utf-8") as f:
    f.write("#pragma once\n\n")
    f.write(f"// Generated: {timestamp}\n")
    f.write(f"// Source: {SCHEM_FILE}\n")
    f.write(f"// Block IDs:\n")
    f.write(f"//   0: air\n")
    f.write(f"//   1: spruce_planks\n")
    f.write(f"//   2: dark_oak_log\n")
    f.write(f"//   3: dark_oak_planks\n")
    f.write(f"//   4: birch_planks\n")
    f.write(f"//   5-8: spruce_stairs[half=bottom] (east/west/south/north)\n")
    f.write(f"//   9-12: spruce_stairs[half=top] (east/west/south/north)\n")
    f.write(f"//   13: dark_oak_door\n")
    f.write(f"//   14: dark_oak_fence\n")
    f.write(f"//   99: unknown\n\n")
    f.write(f"#define MAP_LENGTH {length}\n")
    f.write(f"#define MAP_WIDTH {width}\n")
    f.write(f"#define MAP_HEIGHT {height}\n\n")
    f.write(f"static int {base_name}[MAP_HEIGHT][MAP_LENGTH][MAP_WIDTH] = {{\n")
    
    for y in range(height):
        f.write(f"    {{ // Y={y}\n")
        for z in range(length):
            f.write("        {")
            row = [f"{int(level_map[z][x][y]):2d}" for x in range(width)]
            f.write(",".join(row))
            f.write(f"}}, // Z={z}\n")
        f.write("    },\n")
    
    f.write("};\n\n")
    f.write(f"// 使用方法: {base_name}[y][z][x]\n")

print("\n✅ levelmap.h 生成完了！")
print("📏 配列サイズ:", level_map.shape)
print("🔢 ブロック分布:", np.bincount(level_map.flatten()))
