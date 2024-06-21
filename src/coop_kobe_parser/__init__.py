from pandas import read_csv, DataFrame
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

        # データフレームを出力
        if df is not None:
            print(df)

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
