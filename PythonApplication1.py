import nbtlib
import numpy as np
import os

# 設定
SCHEM_FILE = "Floor1.schem"

def block_to_id(block_name):
    if 'air' in block_name: return 0
    if 'spruce_planks' in block_name: return 1        # トウヒの板材
    if 'purple_terracotta' in block_name: return 2    # 紫色のテラコッタ
    if 'crimson_planks' in block_name: return 3       # 真紅の板材
    if 'spruce_stairs' in block_name: return 4        # トウヒの階段
    return 5  # その他

# Schematic読み込み
print(f"読み込み: {SCHEM_FILE}")
schem_file = nbtlib.load(SCHEM_FILE)
schem = schem_file['Schematic']  # ✅ Schematic ネストにアクセス
width, height, length = int(schem['Width']), int(schem['Height']), int(schem['Length'])
print(f"サイズ: {width}x{height}x{length}")

# パレット→IDマップ (Blocks内のPaletteを取得)
palette = schem.get('Blocks', {}).get('Palette', {})
block_id_map = {}
if palette:
    for name, idx in palette.items():
        block_id_map[idx] = block_to_id(name)
    print("ブロックマップ:", block_id_map)
else:
    print("⚠️ Palette が見つかりません")

# Blocks解凍 (✅ Blocks内のDataを取得)
blocks_data = schem.get('Blocks', {}).get('Data')
if blocks_data is None:
    print("❌ エラー: Data が見つかりません")
    exit(1)

blocks = np.array(blocks_data, dtype=np.int32)

# 縦x横x高さ配列生成 (length x width x height)
level_map = np.zeros((length, width, height), dtype=int)

for y in range(height):
    for z in range(length):
        for x in range(width):
            idx = y * (length * width) + z * width + x
            if idx < len(blocks):
                block_idx = blocks[idx]
                # ブロックIDを取得
                block_id = block_id_map.get(block_idx, 5)  # デフォルトは5
                level_map[z][x][y] = block_id

# Cヘッダ出力
with open("levelmap.h", "w", encoding="utf-8") as f:
    f.write("#ifndef LEVELMAP_H\n#define LEVELMAP_H\n\n")
    f.write(f"#define MAP_LENGTH {length}\n")
    f.write(f"#define MAP_WIDTH {width}\n")
    f.write(f"#define MAP_HEIGHT {height}\n\n")
    f.write(f"static int Floor1[MAP_HEIGHT][MAP_LENGTH][MAP_WIDTH] = {{\n")
    
    for y in range(height):
        f.write(f"    {{ // Y={y}\n")
        for z in range(length):
            f.write("        {")
            row = [str(int(level_map[z][x][y])) for x in range(width)]
            f.write(",".join(row))
            f.write(f"}}, // Z={z}\n")
        f.write("    },\n")
    
    f.write("};\n\n")
    f.write("// 使用方法: Floor1[y][z][x]\n#endif\n")

print("✅ levelmap.h 生成完了！")
print("📏 配列サイズ:", level_map.shape)
print("🔢 ブロック分布:", np.bincount(level_map.flatten()))
