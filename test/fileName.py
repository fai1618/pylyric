"""
python3.4.3
2016/08/07
ファイル名をitunesから取得する時、
濁点・半濁点が含まれるファイル名のものは文字コード？が違うので、それを変換する
Yamada Kouhei
"""
def convert_file_name(bytes_file_name):
    bytes_file_name_list = list(bytes_file_name)

    for i, element in enumerate(bytes_file_name_list):
    if i is len(bytes_file_name_list) - 2:
        break
    if hex(element) == '0xe3' and hex(bytes_file_name_list[i+1]) == '0x82' and hex(bytes_file_name_list[i+2]) == '0x99':
        bytes_file_name_list[i-1] = bytes_file_name_list[i-1] + 1
        del bytes_file_name_list[i:i+3]
    elif hex(element) == '0xe3' and hex(bytes_file_name_list[i+1]) == '0x82' and hex(bytes_file_name_list[i+2]) == '0x9a':
        bytes_file_name_list[i-1] = bytes_file_name_list[i-1] + 2
        del bytes_file_name_list[i:i+3]

    file_name = ''
    for e in bytes_file_name_list:
        file_name += '\\' + str(hex(e))[1:]
    return file_name


if __name__ == '__main__':
    a = '叫べ'.encode()
    b = b'\xe5\x8f\xab\xe3\x81\xb8\xe3\x82\x99'
    file_name = convert_bytes_file_name(b)
    print(file_name)

    correct_codes = str(a)[2:-1]
    asd = list(file_name)

    for i, e in enumerate(list(correct_codes)):
        if not e == asd[i]:
            raise('false!!!')