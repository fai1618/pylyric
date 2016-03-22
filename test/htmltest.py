# TODO:ファイル名変更 + 本番用に(確認等)
"""
python3.4.3

テスト用だけどmain.pyでも使ってる
Yamada Kouhei
"""
from urllib.request import urlopen
import urllib.parse
import urllib.error
import lxml.html
from lxml import etree


def is_exist_url(url):
    # TODO:名前を適切なものに変更
    """
    HTTPステータス
    exception -> return 0
    200 etc... -> return 1
    others -> return error.code

    :param url : str
    :return : int (0 == False, 1 == True)
    """
    if not url:
        return 0
    try:
        page = urlopen(url)
    except urllib.error.HTTPError as err:
        if err.code:
            return err.code
        else:
            return 0
    return 1


def get_name_list_url_by_artist(artist_name, url):
    # TODO: 文字のURL化(アーティスト名)
    """
    アーティスト名(完全一致)から曲のリストのurlを作成する
    url : getパラメータなし (?もなし)

    :param artist_name : str
    :param url : str
    :retrun : str
    """
    artist_name = urllib.parse.quote_plus(artist_name, encoding="sjis")
    result = url + '?Aselect=1&Keyword=' + artist_name + '&Bselect=4&x=40&y=15'
    if not is_exist_url(result) == 1:
        if is_exist_url(result) == 404:
            print('404 NotFound')
            exit()
        # return None
    return result


def get_id_by_music_name(music_name, url):
    # TODO:動作確認
    # TODO:曲の候補がなかった時の処理追加
    # TODO:その他例外処理
    """
    曲名から曲のidを取得する
    :param music_name : str
    :param url : str
    :return : int
    """
    if not url:
        print('URLが間違っています')
        return None
    root = lxml.html.parse(url).getroot()
    for a in root.xpath('//a'):
        text = a.text
        if text == music_name:
            href = a.get('href')
            id = int(href.split('/')[2])
            return id
    print("曲名が見つかりませんでした (get_id_by_music_name)")
    return None


def get_lyric_by_id(id, url):
    # TODO:例外処理
    """
    idから歌詞を取得する
    :param url : str
    :param id : int
    :return : str or bool(False)
    """
    lyric = ""
    if id is None:
        return False
    id = str(id)
    url += '?ID=' + id + '&WIDTH=560&HEIGHT=882&FONTSIZE=15'

    # xmlが返ってきて、そのtextタグの内容1つずつが歌詞の一行となっている
    # textタグの内容を文字列にする
    # TODO: try文にする
    f = urlopen(url)
    if f.code == 200:
        byte = f.read()
        root = etree.XML(byte)
        # TODO:xpathの表現方法改善
        tags = root.xpath('//*')
        for tag in tags:
            if tag.text:
                lyric += tag.text + '\n'
        # 最後改行抜く
        if lyric[-1] == '\n':
            lyric = lyric[:-1]
        return lyric
    elif f.code == 404:
        raise Exception('404 Not Found (get lyrics)')
    elif f.code == 403:
        raise Exception('403 Forbidden (get lyrics)')
    else:
        raise Exception('get lyrics (get request) Error')


if __name__ == '__main__':
    rURL = 'http://www.uta-net.\
com/user/phplib/svg/showkasi.php'
    print('artist: ',end='')
    artist = input()
    print('name: ',end='')
    name = input()
    print('artist : ' + artist)
    print('name : ' + name)
    url = get_name_list_url_by_artist(artist, 'http://www.uta-net.com/search/')
    print(get_lyric_by_id(get_id_by_music_name(name, url), rURL))
