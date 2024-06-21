# coop-kobe-parser

[![PyPI version](https://badge.fury.io/py/coop-kobe-parser.svg)](https://badge.fury.io/py/coop-kobe-parser)
![build](https://github.com/ryohidaka/coop-kobe-parser/workflows/Build/badge.svg)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

コープこうべの宅配の注文書(CSV)をパースする Python パッケージ

## Installation

You can install this library using PyPI:

```shell
pip install coop-kobe-parser
```

## 使用方法

```py
from coop-kobe-parser import CoopKobeParser


# パーサーのインスタンスを作成
parser = CoopKobeParser()

# 解析する CSV ファイルのパス
csv_path = "path/to/file.csv"

# CSV ファイルを解析
data = parser.parse(csv_path)

# 出力
print(json.dumps(data, indent=4, ensure_ascii=False))
```

### 入力例(csv)

```csv
品番,商品名,本体価格,数量,小計
001,ダミー商品A,"1,000",1,"1,080"
002,ダミー商品B,300,2,648
003,ダミー商品C,200,1,216
004,ダミー商品D,150,3,486
005,ダミー商品E,500,1,540
006,ダミー商品F,400,1,432
007,ダミー商品G,250,2,540
008,ダミー商品H,350,1,378
009,ダミー商品I,450,1,486
010,ダミー商品J,300,1,324
,値引き前本体合計金額(8%),,,"4,150"
,値引き額(8%),,,50
,本体合計金額(8%),,,"4,100"
,消費税(8%),,,328
,値引き前本体合計金額(10%),,,0
,値引き額(10%),,,0
,本体合計金額(10%),,,0
,消費税(10%),,,0
,値引き前本体合計金額（非課税）,,,0
,値引き額(非課税),,,0
,本体合計金額(非課税),,,0
,本体合計金額,,,"4,100"
,消費税等,,,328
,ご注文金額(税込),,,"4,428"
,合計点数,,12,
,獲得予定ポイント,,,10

```

### 出力例

```json
{
  "products": [
    {
      "name": "ダミー商品A",
      "price": 1000,
      "amount": 1,
      "subtotal": 1080
    },
    {
      "name": "ダミー商品B",
      "price": 300,
      "amount": 2,
      "subtotal": 648
    },
    {
      "name": "ダミー商品C",
      "price": 200,
      "amount": 1,
      "subtotal": 216
    },
    {
      "name": "ダミー商品D",
      "price": 150,
      "amount": 3,
      "subtotal": 486
    },
    {
      "name": "ダミー商品E",
      "price": 500,
      "amount": 1,
      "subtotal": 540
    },
    {
      "name": "ダミー商品F",
      "price": 400,
      "amount": 1,
      "subtotal": 432
    },
    {
      "name": "ダミー商品G",
      "price": 250,
      "amount": 2,
      "subtotal": 540
    },
    {
      "name": "ダミー商品H",
      "price": 350,
      "amount": 1,
      "subtotal": 378
    },
    {
      "name": "ダミー商品I",
      "price": 450,
      "amount": 1,
      "subtotal": 486
    },
    {
      "name": "ダミー商品J",
      "price": 300,
      "amount": 1,
      "subtotal": 324
    }
  ],
  "summary": {
    "pre_total_8": 4150,
    "discount_8": 50,
    "total_8": 4100,
    "tax_8": 328,
    "pre_total_10": 0,
    "discount_10": 0,
    "total_10": 0,
    "tax_10": 0,
    "pre_total_non_tax": 0,
    "discount_non_tax": 0,
    "total_non_tax": 0,
    "total_amount": 4100,
    "total_tax": 328,
    "order_amount_incl_tax": 4428,
    "expected_points": 10,
    "total_items": 12
  }
}
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
