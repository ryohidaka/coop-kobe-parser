import json
from pandas import read_csv, DataFrame, Series
from pandas.errors import EmptyDataError, ParserError

from coop_kobe_parser.logger import init_logger
from coop_kobe_parser.parsers import ProductParser, SummaryParser


def main():
    """
    動作確認用
    CoopKobeParser インスタンスを作成し、CSV ファイルを解析します。
    """

    # パーサーのインスタンスを作成
    parser = CoopKobeParser()

    # 解析する CSV ファイルのパス
    csv_path = "demo/demo.csv"
    parser.logger.info(f"解析を開始します: {csv_path}")

    # CSV ファイルを解析
    data = parser.parse(csv_path)
    print(json.dumps(data, indent=4, ensure_ascii=False))


class CoopKobeParser:
    def __init__(self):
        """
        CoopKobeParser クラスの初期化。
        """
        self.logger = init_logger()
        self.logger.info("CoopKobeParser クラスを初期化しました。")

    def parse(self, csv_path: str) -> dict:
        """
        CSV ファイルを解析し、種別ごとに分離した上で取得する

        Parameters:
        csv_path (str): 解析する CSV ファイルのパス

        Returns:
        dict: パース結果
        """
        self.logger.info(f"CSV ファイルの解析を開始します: {csv_path}")

        # CSV ファイルを読み込み
        df = self._load_csv(csv_path)
        if df is None:
            self.logger.error("CSV ファイルの読み込みに失敗しました。")
            return {}

        # 商品一覧と支払情報のデータフレームに分ける
        df_products, df_summary = self._divide_df(df)
        self.logger.info("データフレームの分割が完了しました。")

        # 商品一覧をパースして配列化する
        products = ProductParser(df_products).parse()
        self.logger.info("商品一覧のパースが完了しました。")

        # 支払情報をパースする
        summary = SummaryParser(df_summary).parse()
        self.logger.info("支払情報のパースが完了しました。")

        return {"products": products, "summary": summary}

    def _load_csv(self, path: str) -> DataFrame:
        """
        CSV ファイルを読み込み、データフレームを返却する

        Parameters:
        path (str): 読み込む CSV ファイルのパス

        Returns:
        DataFrame: CSV ファイルから読み込んだデータフレーム
        """
        try:
            self.logger.info(f"CSV ファイルを読み込みます: {path}")
            # CSV ファイルを読み込み
            df = read_csv(path, dtype=str)
            self.logger.info("CSV ファイルの読み込みが成功しました。")
            return df
        except FileNotFoundError:
            self.logger.error(f"ファイル {path} が見つかりませんでした。")
        except (EmptyDataError, ParserError):
            self.logger.error(f"ファイル {path} の読み込み中にエラーが発生しました。")
            return None

    def _divide_df(self, df: DataFrame) -> tuple[Series, Series]:
        """
        商品一覧と支払情報のデータフレームに分ける

        Parameters:
        df (DataFrame): CSV ファイルから読み込んだデータフレーム

        Returns:
        tuple[DataFrame, DataFrame]: 商品一覧のデータフレームと支払情報のデータフレームのタプル
        """

        # 品番が存在するかどうかを確認
        if "品番" not in df.columns:
            self.logger.error("品番列がデータフレームに存在しません。")
            raise ValueError("品番列がデータフレームに存在しません。")

        self.logger.info("品番列の確認が完了しました。")

        # 商品一覧のデータフレームを取得 (品番がNaNでない)
        df_products = df[df["品番"].notna()]

        # 支払情報のデータフレームを取得 (品番がNaN)
        df_summary = df[df["品番"].isna()]

        # 商品一覧と支払情報のデータフレームが空でないことを確認
        if df_products.empty or df_summary.empty:
            self.logger.error("商品一覧または支払情報のデータフレームが空です。")
            raise ValueError("商品一覧または支払情報のデータフレームが空です。")

        self.logger.info("データフレームの分割に成功しました。")
        return df_products, df_summary
