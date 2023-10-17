import re
CYRILLIC_SYMBOLS = 'абвгдеєжзіийклмнопрстуфхцчшщьюяєїґ'
TRANSLATION = ("a", "b", "v", "h", "d", "e", "ie", "j", "z", "i", "y", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "kh", "ts", "ch", "sh", "shch", "", "iy", "ia", "e", "yi", "h")
ACCORD = dict()
for cyril, latin in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    ACCORD[ord(cyril)] = latin
    ACCORD[ord(cyril.upper())] = latin.capitalize()

def normalize(name: str) -> str:
    translate_name = re.sub(r'[\`,\!,\|,\@,\#,\$,\%,\^,\&,\*,\(,\),\-,\+,\=,\<,\>,\?,\/,\',\,,\:,\;,\"]', '_', name.translate(ACCORD))
    return translate_name

#print(normalize('Якась_назва_файлу.txt'))