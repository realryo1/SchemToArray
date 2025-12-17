# SchemToArray

Minecraft の `.schem` ファイルを C 言語用の 3D 配列に変換するツールです。

## 概要

- 📦 **Minecraft Schematic ファイル対応**: `.schem` ファイルを読み込み
- 🔢 **C 言語配列生成**: 3 次元配列として `.h` ファイルを出力
- 🎮 **ブロック定義カスタマイズ**: JSON で自由にブロック ID をマッピング
- 📊 **ブロック分布表示**: 使用ブロックの統計情報を表示
- 🔧 **自動ライブラリインストール**: 必要なライブラリを自動でインストール

## 必要環境

- **Python 3.9 以上**
- **pip** (Python パッケージマネージャー)

## インストール

このリポジトリをクローン：
```bash
git clone https://github.com/realryo1/SchemToArray.git
cd SchemToArray
```

必要なライブラリは自動でインストールされます。

## 使い方

### ①パス指定で実行

```bash
python PythonApplication1.py <schemファイルのパス> [ブロック定義JSONのパス]
```

例：
```bash
python PythonApplication1.py ./Floor1.schem ./block_definitions.json
```

### ②対話的に実行

```bash
python PythonApplication1.py
```

実行時にファイルパスを入力するよう促されます。

## 入力ファイル形式

### 1. `.schem` ファイル

Minecraft Schematic ファイルです。FAWE (FastAsyncWorldEdit) で保存できます。

#### FAWE での .schem ファイル取得方法

1. 木の斧を持ちながら始点（左クリック）と終点（右クリック）を設定
2. コマンド「`//copy`」を実行
3. コマンド「`download schem`」を実行
4. 出てきたリンクをクリック
5. サイトの「Click here if your download doesn't start automatically」をクリックしてダウンロード
6. ファイル名を適当に変更
   - ⚠️ **注意**: ファイル名がヘッダーガード名と変数名になります

### 2. ブロック定義 JSON ファイル (`block_definitions.json`)

ブロック名を ID にマッピングする定義ファイルです。

#### 基本構造

```json
{
  "blocks": [
    {
      "name": "spruce_planks",
      "names_ja": "トウヒの板材",
      "default_id": 1
    },
    {
      "name": "spruce_stairs",
      "names_ja": "トウヒの階段",
      "default_id": 5,
      "conditions": [
        {
          "properties": {
            "half": "bottom",
            "facing": "east"
          },
          "id": 5,
          "names_ja": "トウヒの階段[下付き・東向き]"
        }
      ]
    }
  ],
  "default_id": 99,
  "default_names_ja": "不明"
}
```

#### 各フィールドの説明

| フィールド | 説明 |
|-----------|------|
| `name` | Minecraft のブロック ID 名 |
| `names_ja` | 日本語名（表示用） |
| `default_id` | デフォルトの割り当て ID |
| `conditions` | (オプション) ブロックプロパティによる条件分岐 |
| `properties` | ブロックの条件（例: `half`, `facing`） |
| `id` | 条件が合致した時の割り当て ID |
| `names_ja` | 条件時の日本語名 |

## 出力ファイル

`.h` ファイルが `.schem` ファイルと同じディレクトリに生成されます。

### 出力例（`Floor1.h`）

```c
#pragma once

// Generated: 2025-12-17 22:49:19
// Source: C:\path\to\Floor1.schem
// Block IDs:
//   0: 空気
//   1: トウヒの板材
//   5: トウヒの階段[下付き・東向き]

#define MAP_LENGTH 31
#define MAP_WIDTH 53
#define MAP_HEIGHT 7

static int floor1[MAP_HEIGHT][MAP_LENGTH][MAP_WIDTH] = {
    { // Y=0
        { 1, 1, 1, ... }, // Z=0
        { 1, 1, 1, ... }, // Z=1
    },
};

// 使用方法: floor1[y][z][x]
```

## 配列の使い方

```c
// Y: 高さ, Z: 深さ, X: 幅
int block_id = floor1[y][z][x];
```

## 機能詳細

### 🔍 ブロックマッピング

1. Schematic のパレットからブロック情報を取得
2. ブロック定義 JSON に基づいて ID に変換
3. 複数のプロパティがある場合は条件マッチングを実行

### 📈 統計表示

実行完了時にブロック分布を表示：

```
==================================================
📊 ブロック分布詳細
==================================================
ID   0: 空気              ×  1500個
ID   1: トウヒの板材      ×   800個
ID   5: トウヒの階段[下付き・東向き] ×   150個
==================================================
```

### 🔤 エンコーディング自動検出

ブロック定義 JSON は以下のエンコーディングに対応：
- Shift-JIS
- UTF-8
- CP1252

## トラブルシューティング

### ライブラリのインストール失敗

```bash
pip install --upgrade pip
pip install nbtlib numpy
```

### ファイルが見つからない

- ファイルパスが正しいか確認してください
- 相対パスの場合、スクリプトを実行するディレクトリから見たパスを指定してください

### エンコーディングエラー

ブロック定義 JSON を UTF-8 で保存してください。

## ライセンス

MIT License

## 貢献

バグ報告や機能リクエストは GitHub Issues からお願いします。
