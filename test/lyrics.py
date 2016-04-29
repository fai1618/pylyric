"""
python3.4.3
2016/02/16
音楽ファイルの歌詞情報を登録、取得するための関数群
Yamada Kouhei
"""
import os.path

import mutagen.id3
from mutagen.id3 import ID3, USLT
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4


def extract_extension(file_name):
    """
    拡張子取得
    :type file_name: str
    :rtype str
    """

    if not file_name or not os.path.splitext(file_name)[1] or os.path.splitext(file_name)[1] == '.':
        raise Exception("file_nameが正しくないです :{0}".format(file_name))

    ext = os.path.splitext(file_name)[1]

    # splitextはextに'.'を含むので削除
    # 将来仕様変更で'.'を含まなくなった時のため、先頭が'.'だった時のみ削除
    if ext[0] == '.':
        return os.path.splitext(file_name)[1][1:]
    else:
        return os.path.splitext(file_name)[1]


def is_exist_file(file_path):
    """
    ファイル存在確認
    :param file_path: str
    :return bool
    """
    if not file_path:
        return False
    return os.path.isfile(file_path)


def register_lyric(file_path, lyric):
    """
    歌詞を登録する
    :param file_path: str
    :param lyric: str
    :return: bool
    """
    if not file_path or not lyric:
        raise Exception("ファイル名か歌詞が正しくない: {0}, {1}".format(file_path, lyric))

    if not is_exist_file(file_path):
        raise Exception("file_pathは存在しません: {0}".format(file_path))

    ext = extract_extension(file_path)
    # TODO:拡張子大文字はあり得るかも？
    if ext == "mp3" or ext == "MP3":
        file = MP3(filename=file_path, ID3=ID3)
    elif ext == "m4a" or ext == "m4p" or ext == "m4b":
        # TODO:m4b未確認
        file = MP4(filename=file_path, ID3=ID3)
    else:
        print("この拡張子のファイルは未対応です: {0}".format(ext))
        return False

    # try:
    #     file.add_tags(ID3=ID3)
    # except mutagen.id3.error:
    #     print('mutagen.id3.error')

    # m['USLT'] = USLT(encoding=0,lang='eng', desc='',text='TEST')
    file['USLT'] = USLT(encoding=1,lang='eng', desc='', text=lyric)
    # print("file['USLT'] : ", file['USLT'])
    file.save()
    return True


def parse_music_file(file_name):
    """
    拡張子による使う関数の振り分け
    :param file_name : str
    :return : instance
    """
    ext = extract_extension(file_name)
    if ext == "mp3":
        return MP3(filename=file_name)
    elif ext == "m4a" or ext == "m4p":
        return MP4(filename=file_name)
    else:
        raise Exception("この拡張子のファイルには未対応です: " + ext)


def has_lyrics(file_path):
    """
    歌詞の存在を調べる関数
    :param file_path : str
    :return : bool
    """

    # 引数確認
    if not file_path:
        raise Exception("ファイル名が正しくない: {0}".format(file_path))
    if not is_exist_file(file_path):
        raise Exception("file_pathは存在しません: {0}".format(file_path))

    # 拡張子による使う関数の振り分け
    file = parse_music_file(file_path)

    # 処理準備
    ext = extract_extension(file_path)
    datas = file.items()
    lyric = ''

    # datasにdataがあるか(emptyじゃないか)
    if not datas:
        raise Exception(('dataがありません: {0}'.format(datas)))

    # infoのすべての'0'番目の中身を見る
    has_lyrics_tag = False
    for data in datas:
        if ext == "mp3":
            if isinstance(data, tuple) and data:
                # TODO:USLTだけ確認?
                if data[0] == 'USLT::eng':
                    has_lyrics_tag = True
                    # キャリッジリターンで行頭に戻って上書きされるので、空白に置換
                    lyric = data[1].text.replace('\r', '\n')  # for mac?
                    if lyric == '':
                        return False
            else:
                return False
        elif ext == "m4a" or ext == "m4p":
            if isinstance(data, tuple) and data:
                # TODO:確認方法正しい?
                if data[0] == '©lyr':
                    has_lyrics_tag = True
                    tmp = ""
                    # TODO:例外処理
                    for word in data[1]:
                        tmp += word.replace('\r', '')
                    lyric = tmp
                    if lyric == '':
                        return False
            else:
                return False

    if has_lyrics_tag and not lyric == '':
        return True

    return False


def get_lyric(file_path):
    """
    歌詞を返す関数
    歌詞がない場合、空白を返す

    エラーとして処理:
        file_pathがFalse
        file_pathで与えられたパスのファイルが存在しない
        対応した拡張子ではない
        音楽ファイルにデータがない

    :param file_path : str
    :return : str
    """
    if not file_path:
        raise Exception("file_pathが正しくないです: {0}".format(file_path))

    if not is_exist_file(file_path):
        raise Exception("file_pathは存在しません: {0}".format(file_path))

    ext = extract_extension(file_path)
    # TODO:拡張子大文字はあり得る？
    if ext == 'mp3':
        file = MP3(filename=file_path, ID3=ID3)
    elif ext == 'm4a' or ext == 'm4p' or ext == 'm4b':
        # TODO:m4b未確認
        file = MP4(filename=file_path, ID3=ID3)
    else:
        print("この拡張子のファイルは未対応です: {0}".format(ext))
        return False

    # TODO:例外処理必要か?
    datas = file.items()
    lyric = ''

    # TODO:items()の仕様確認
    if not datas:
        raise Exception(("dataがありません: {0}".format(datas)))

    # TODO:仕様確認
    # dataのすべての0番目の中身がkeyになってるっぽいから、そこで判別
    for data in datas:
        if ext == 'mp3':
            # TODO:listの判定いる？
            if isinstance(data, list) or isinstance(data, tuple):
                # TODO:USLTだけ確認でOK?
                if data and data[0] == 'USLT::eng':
                    # キャリッジリターンで変数の内容が上書きされるので、改行に置換
                    # TODO?:mac以外で確認
                    lyric = data[1].text.replace('\r', '\n')
                    # ここまで到達したうえでlyricが空なのか確認するためのデバッグ用
                    if lyric == '':

                        print("歌詞が空です")

        elif ext == "m4a" or ext == "m4p":
            # TODO:listの判定いる？
            if isinstance(data, list) or isinstance(data, tuple):
                # TODO:確認方法が正しいか確認
                if data and data[0] == '©lyr':
                    tmp = ""
                    # TODO:例外処理
                    # いらないかも
                    for word in data[1]:
                        tmp += word.replace('\r', '')

                    lyric = tmp
                    # ここまで到達したうえでlyricが空なのか確認するためのデバッグ用
                    if lyric == '':
                        print("歌詞が空です")
    return lyric
