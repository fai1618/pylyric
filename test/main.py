#!/Users/kohei/.pyenv/shims/python
"""
python3.4.3
2016/02/29
ここから起動する
yamada Kouhei
"""
import os
import subprocess
from lyrics import get_lyric, has_lyrics, register_lyric
from htmltest import get_name_list_url_by_artist,\
                     get_lyric_by_id, get_id_by_music_name
from settings import settings


def impl(cmd):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout_data, stderr_data = p.communicate()
    return stdout_data, stderr_data, p.returncode


def replace_symbol_for_shell(word):
    """
    \"  $  @  &  '  (  )  ^  |  [  ]  {  }  ;  *  ?  <  >  `  \\ -
    の前にバックスラッシュをつけて、shellに引数として与えた時に文字列として認識させる
    (バックスラッシュは曲名に使われないので省く) + (空白も前にバックスラッシュをつける)

    :param word : str
    :return : str
    """
    replaced_word = word
    symbols = ['"', '$', '@', '&', '\'', '(', ')', '^', '|', '[', ']',
               '{', '}', ';', '*', '?', '<', '>', '`', ' ', '-']
    symbols2 = [r'\"', r'\$', r'\@', r'\&', r"\'", r'\(', r'\)',
                r'\^', r'\|', r'\[', r'\]', r'\{', r'\}', r'\;',
                r'\*', r'\?', r'\<', r'\>', r'\`', '\ ', '\-']
    for symbol, symbol2 in zip(symbols, symbols2):
        replaced_word = replaced_word.replace(symbol, symbol2)
    return replaced_word


if __name__ == '__main__':
    # TODO:itunesコマンドを内包化
    artist = impl('/usr/local/bin/itunes artist')[0]
    artist = artist.decode()
    if str(artist[-1]) == '\n':
        artist = artist[:-1]

    # 曲再生中でないとき
    if artist == 'Music is not played' or artist == 'iTunes is not Active':
        print(artist)

    # 曲再生中の時
    else:
        setting = settings()
        album = impl('/usr/local/bin/itunes album')[0]
        album = album.decode()
        if album[-1] == '\n':
            album = album[:-1]

        name = impl('/usr/local/bin/itunes name')[0]
        name = name.decode()
        if name[-1] == '\n':
            name = name[:-1]

        rURL = 'http://www.uta-net.com/user/phplib/svg/showkasi.php'

        MUSIC_FILE_ROOT_PATH = os.environ.get("HOME") + \
            '/Music/iTunes/iTunes Media/Music'

        print('artist     : ' + artist)
        print('album      : ' + album)
        print('name       : ' + name)

        album_path = MUSIC_FILE_ROOT_PATH + '/' + artist + '/' + album

        # shell環境用
        album_path_for_shell = replace_symbol_for_shell(album_path)
        name_for_shell = replace_symbol_for_shell(name)

        # iTunesに登録された曲名の曲のファイル名検索    かならずしも(曲名 == ファイル名)でないため
        # TODO:ファイル名検索方法変更(シェル使わなくていいように)
        file_name = impl('cd ' + album_path_for_shell + ' && ls ./*' + name_for_shell + '*')[0].decode()[2:-1]  # './'削除 + 改行削除
        if not file_name:
            print('IMPL ERROR')
            print('cd ' + album_path_for_shell + ' && ls *' + name_for_shell + '*')
            raise print(impl('cd ' + album_path_for_shell + ' && ls *' + name_for_shell + '*'))

        print('file name  : ' + file_name)

        hasLyrics = has_lyrics(album_path + '/' + file_name)  # 正しくない  register_lyricからの登録時のみ？
        print('has lyrics : ' + str(hasLyrics))

        url = get_name_list_url_by_artist(artist, 'http://www.uta-net.com/search/')
        # TODO:変数名変更
        lyric_or_False = get_lyric_by_id(get_id_by_music_name(name, url), rURL)
        print(lyric_or_False)

        # test
        if not lyric_or_False or hasLyrics:
            exit()
        else:
            lyric = lyric_or_False
            print('register lyrics?(y/n): ', end='')
            is_register = input()
            while is_register is not 'y' and is_register is not 'n':
                print('please input y or n')
                print('register lyrics?(y/n): ', end='')
                is_register = input()
            if is_register == 'y':
                register_lyric(album_path+ '/' +file_name, lyric)
            elif is_register == 'n':
                exit()
