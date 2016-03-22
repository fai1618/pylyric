"""
python3.4.3
2016/03/05
設定ファイルをパースする関数のみ
Yamada Kouhei
"""
import os
import json


def settings(setting_file_path=os.environ.get("HOME") + '/.lyrics/settings'):
    """
    JSON形式の設定ファイルを辞書型にパースする
    :param setting_file_path: str
    :return :dict
    """
    with open(setting_file_path, "r") as f:
        settings_dict = json.load(f)
        return settings_dict
