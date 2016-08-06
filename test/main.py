#!/Users/kohei/.pyenv/shims/python
"""
python3.4.3
2016/02/29
ここから起動する
yamada Kouhei
"""
import os
import subprocess
import unicodedata
import fnmatch
from lyrics import get_lyric, has_lyrics, register_lyric, extract_extension
from htmltest import get_name_list_url_by_artist,\
                     get_lyric_by_id, get_id_by_music_name
from settings import settings


def impl(cmd):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout_data, stderr_data = p.communicate()
    return stdout_data, stderr_data, p.returncode


def itunes_command(arg):
    command = """
        #!/bin/bash
        if [ -f ~/.bash/itunes.scpt ]; then
            echo `osascript ~/.bash/itunes.scpt {0}`
        else
            echo `osascript ~/.bash/itunes.scpt list`
        fi
    """.format(arg)
    return impl(command)


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
               '{', '}', ';', '*', '?', '<', '>', '`', ' ', '-', '/']
    symbols2 = [r'\"', r'\$', r'\@', r'\&', r"\'", r'\(', r'\)',
                r'\^', r'\|', r'\[', r'\]', r'\{', r'\}', r'\;',
                r'\*', r'\?', r'\<', r'\>', r'\`', '\ ', '\-', '\/']
    for symbol, symbol2 in zip(symbols, symbols2):
        replaced_word = replaced_word.replace(symbol, symbol2)
    return replaced_word


class IMPLException(Exception):
    def __init__ (self, message):
        """
        引数はraise文から受け取る
        :param message : str
        """
        self._message = message

    def __str__ (self):
        return self._message


class PurseMusicInfoException(Exception):
    def __init__ (self, info_pattern, info_value):
        """
        引数はraise文から受け取る
        :param info_pattern : str
            artist,album,nameなどの情報の種類
        :param info_value : any
            artist,album,nameなどの情報の中身
        """
        self._ptn, self._val = (info_pattern, info_value)

    def __str__ (self):  # エラーメッセージ
        return '"{0}" is not valid ({1})'.format (self._ptn, self._val)


def isPurseMusicInfoException(info_pattern, info_value):
    """
    PurseMusicInfoException判定と例外呼び出し
    :param info_pattern : str
    :param info_value : any
    :return : Bool
    引数はPurseMusicInfoExceptionの引数と同じ
    """
    if not info_value or info_value == '\n':
        raise(PurseMusicInfoException(info_pattern, info_value))
    else:
        return False


def check_add_lyrics_y_or_n(file_path, is_overwrite=False):  # TODO:関数名変更
    if is_overwrite:
        str = "overwrite lyrics?"
    else:
        str = "register lyrics?"

    print(str + '(y/n): ', end='')
    is_register = input()
    while is_register is not 'y' and is_register is not 'n':
        print('please input y or n')
        print(str + '(y/n): ', end='')
        is_register = input()
    if is_register == 'y':
        register_lyric(file_path, lyric)
        exit()
    elif is_register == 'n':
        exit()


def remove_last_newline(str):
    if str[-1] == '\n':
        str = str[:-1]
    return str

if __name__ == '__main__':
    artist = itunes_command('artist')[0].decode()
    isPurseMusicInfoException("artist", artist)
    artist = remove_last_newline(str(artist))

    # 曲再生中でないとき
    if artist == 'Music is not played' or artist == 'iTunes is not Active':
        print(artist)

    # 曲再生中の時
    else:
        setting = settings()
        album = itunes_command('album')[0].decode()
        if album == '\n':
            album = ''
        else:
            album = remove_last_newline(str(album))

        name = itunes_command('name')[0].decode()
        isPurseMusicInfoException("name", name)
        name = remove_last_newline(str(name))

        if len(setting["search_lyrics_sites"]) > 1:
            print("you can only use www.uta-net.com")
        #歌詞検索のサイトを設定から読み込む
        if "http://uta-net.com" in setting["search_lyrics_sites"]:
            rURL = 'http://www.uta-net.com/user/phplib/svg/showkasi.php'
        else:
            print("you can only use www.uta-net.com")
            exit()

        MUSIC_FILE_ROOT_PATH = os.environ.get("HOME") + '/' + setting["file_search_target_directory"]
        album_path = MUSIC_FILE_ROOT_PATH + '/' + artist + '/' + album
        # shell環境用
        album_path_for_shell = replace_symbol_for_shell(album_path)
        name_for_shell = replace_symbol_for_shell(name)

        print('artist     : ' + artist)
        print('album      : ' + album)
        print('name       : ' + name)

        # iTunesに登録された曲名の曲のファイル名検索    かならずしも(曲名 == ファイル名)でないため
        files = os.listdir(album_path)
        for file in files:
            ext = extract_extension(file)
            print(name.encode())
            print(file.encode())
            nameE = name.encode()
            name2 = nameE.decode()
            print(name2.encode())
            if fnmatch.fnmatch(file, '*{0}.'.format(name) + ext):
                print('match!!!')
                file_name = file
                break
            else:
                print('no match!!!')

        print('file name  : ' + file_name)

        hasLyrics = has_lyrics(album_path + '/' + file_name)
        print('has lyrics : ' + str(hasLyrics))

        url = get_name_list_url_by_artist(artist, 'http://www.uta-net.com/search/')
        music_id_or_None = get_id_by_music_name(name, url)
        if music_id_or_None is None:
            exit()
        lyric_or_False = get_lyric_by_id(music_id_or_None, rURL)
        print(lyric_or_False)

        if not lyric_or_False:
            #TODO?:raise False!!!
            print('lyric is False')
            exit()
        else:
            file_path = album_path+ '/' +file_name
            lyric = lyric_or_False

            if hasLyrics:
                if setting["overwrite_lyrics"]:
                    check_add_lyrics_y_or_n(file_path ,is_overwrite=True)
                exit()
            else:
                if setting["auto_register_lyrics"]:
                    register_lyric(file_path, lyric)
                    exit()
                else:
                    check_add_lyrics_y_or_n(file_path)
