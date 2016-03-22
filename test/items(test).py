"""
python3.4.3

テスト用 main.pyでは使わない
Yamada Kouhei
"""
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
import lyrics


def has_lyrics(file_name):
    """
    歌詞の存在を調べる関数
    :param file_name : str
    :return : bool
    """
    ext = lyrics.extract_extension(file_name)
    if ext == "mp3":
        file = MP3(filename=file_name)
    elif ext == "m4a" or ext == "m4p":
        file = MP4(filename=file_name)
    else:
        raise Exception("この拡張子のファイルには未対応です: " + ext)

    datas = file.items()
    lyric = ''

    # datasにdataがあるか(emptyじゃないか)
    if len(datas) < 1:
        raise Exception(('dataがありません: {0}'.format(datas)))
    # infoのすべての'0'番目の中身を見る
    for data in datas:
        if ext == "mp3":
            if isinstance(data, list) or isinstance(data, tuple):
                # TODO:USLTだけ確認?
                if len(data) >= 1 and data[0] == 'USLT::eng':
                    # print(data[1].text)
                    # キャリッジリターンで行頭に戻って上書きされるので、空白に置換
                    lyric = data[1].text.replace('\r', '\n')
                    if lyric == '':
                        return False
        elif ext == "m4a" or ext == "m4p":
            if isinstance(data, list) or isinstance(data, tuple):
                # TODO:確認方法が正しいか確認
                if len(data) >= 1 and data[0] == '©lyr':
                    # TODO:strか確認
                    tmp = ""
                    # TODO:例外処理
                    for word in data[1]:
                        tmp += word.replace('\r', '')
                    lyric = tmp
                    if lyric == '':
                        return False
    return True


def get_lyrics(file_name):
    """
    歌詞を返す関数
    歌詞がないときは空白を返す
    :param file_name : str
    :return : str
    """
    if not file_name:
        raise Exception("file_nameが正しくないです: {0}".format(file_name))

    if not lyrics.is_exist_file(file_name):
        raise Exception("file_nameは存在しません: {0}".format(file_name))
    ext = lyrics.extract_extension(file_name)
    if ext == "mp3":
        file = MP3(filename=file_name)
    elif ext == "m4a" or ext == "m4p":
        file = MP4(filename=file_name)
    else:
        raise Exception("この拡張子のファイルには未対応です: " + ext)

    try:
        datas = file.items()
    except Exception as e:
        print("error")
        print(e)

    lyric = ''
    # datasにdataがあるか(emptyじゃないか)
    if len(datas) < 1:
        raise Exception(('dataがありません: {0}'.format(datas)))
    # infoのすべての'0'番目の中身を見る
    for data in datas:
        if ext == "mp3":
            if isinstance(data, list) or isinstance(data, tuple):
                # TODO:USLTだけ確認?
                if len(data) >= 1 and data[0] == 'USLT::eng':
                    # print(data[1].text)
                    # キャリッジリターンで行頭に戻って上書きされるので、空白に置換
                    lyric = data[1].text.replace('\r', '\n')  # for mac?
                    if lyric == '':
                        print("歌詞が空です")
        elif ext == "m4a" or ext == "m4p":
            if isinstance(data, list) or isinstance(data, tuple):
                # TODO:確認方法が正しいか確認
                if len(data) >= 1 and data[0] == '©lyr':
                    # TODO:strか確認
                    tmp = ""
                    # TODO:例外処理
                    for word in data[1]:
                        tmp += word.replace('\r', '')
                    lyric = tmp
                    if lyric == '':
                        print("歌詞が空です")
    return lyric

if __name__ == '__main__':
    # print("歌詞を表示するファイルのパスを入力してください")
    a = '../music/yes/風の憧憬.m4a'
    print(a+'\n')
    print(str(has_lyrics(a)) + '\n')
    print(get_lyrics(a))
