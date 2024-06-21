from pandas import read_csv, DataFrame, Series
from pandas.errors import EmptyDataError, ParserError


def main():
    """
    動作確認用
    CoopKobeParser インスタンスを作成し、CSV ファイルを解析します。
    """

    # パーサーのインスタンスを作成
    parser = CoopKobeParser()

    # 解析する CSV ファイルのパス
    csv_path = "demo/demo.csv"

    # CSV ファイルを解析
    parser.parse(csv_path)


class CoopKobeParser:
    def parse(self, csv_path: str):
        """
        CSV ファイルを解析し、データフレームを出力する

        Parameters:
        csv_path (str): 解析する CSV ファイルのパス
        """
        # CSV ファイルを読み込み
        df = self._load_csv(csv_path)

        # 商品一覧と支払情報のデータフレームに分ける
        df_products, df_summary = self._divide_df(df)

        # データフレームを出力
        print(df_products)
        print(df_summary)

    def _load_csv(self, path: str) -> DataFrame:
        """
        CSV ファイルを読み込み、データフレームを返却する

        Parameters:
        path (str): 読み込む CSV ファイルのパス

        Returns:
        DataFrame: CSV ファイルから読み込んだデータフレーム
        """
        try:
            # CSV ファイルを読み込み
            df = read_csv(path, dtype=str)
            return df
        except FileNotFoundError:
            print(f"ファイル {path} が見つかりませんでした。")
        except (EmptyDataError, ParserError):
            print(f"ファイル {path} の読み込み中にエラーが発生しました。")
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
            raise ValueError("品番列がデータフレームに存在しません。")

        # 商品一覧のデータフレームを取得 (品番がNaNでない)
        df_products = df[df["品番"].notna()]

        # 支払情報のデータフレームを取得 (品番がNaN)
        df_summary = df[df["品番"].isna()]

        # 商品一覧と支払情報のデータフレームが空でないことを確認
        if df_products.empty or df_summary.empty:
            raise ValueError("商品一覧または支払情報のデータフレームが空です。")

        return df_products, df_summary
