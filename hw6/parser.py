import sys
from pathlib import Path

JPEG_IMG = []
JPG_IMG = []
PNG_IMG = []
SVG_IMG = []
#'MP3', 'OGG', 'WAV', 'AMR'
MP3_AUDIO = []
OGG_AUDIO = []
WAV_AUDIO = []
AMR_AUDIO = []
#'AVI', 'MP4', 'MOV', 'MKV'
MP4_VIDEO = []
AVI_VIDEO = []
MOV_VIDEO = []
MKV_VIDEO = []
#'DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX, PY
DOC_DOC = []
DOCX_DOC = []
TXT_DOC = []
PDF_DOC = []
XLSX_DOC = []
PPTX_DOC = []
PY_DOC = []
#'ZIP', 'GZ', 'TAR'
ZIP_ARCH = []
GZ_ARCH = []
TAR_ARCH = []
NOT_DEFINED = []

REGISTER_EXTENSION = {
    'JPEG': JPEG_IMG,
    'JPG': JPG_IMG,
    'PNG': PNG_IMG,
    'SVG': SVG_IMG,
    'OGG': OGG_AUDIO,
    'WAV': WAV_AUDIO,
    'AMR': AMR_AUDIO,            
    'MP3': MP3_AUDIO,
    'MP4': MP4_VIDEO,
    'AVI': AVI_VIDEO,
    'MOV': MOV_VIDEO,
    'MKV': MKV_VIDEO,
    'DOC': DOC_DOC,
    'DOCX': DOCX_DOC,
    'TXT': TXT_DOC,
    'PDF': PDF_DOC,
    'XLSX': XLSX_DOC,
    'PPTX': PPTX_DOC,
    'PY': PY_DOC,
    'ZIP': ZIP_ARCH,
    'GZ': GZ_ARCH,
    'TAR': TAR_ARCH
}

FOLDERS = []
EXTENSIONS = set()
UNKNOWN = set()

def get_extension(name: str) -> str:
    return Path(name).suffix[1:].upper()  
#folder
def scan(folder: Path):
    for item in folder.iterdir():
        if item.is_dir(): 
            if item.name not in ('archives', 'video', 'audio', 'documents', 'images', 'not_defined'):
                FOLDERS.append(item)
                scan(item)
            continue
        extension = get_extension(item.name)  # беремо розширення файлу
        full_name = folder / item.name  # беремо повний шлях до файлу
        if not extension:
            NOT_DEFINED.append(full_name)
        else:
            try:
                REGISTER_EXTENSION[extension].append(full_name)
                EXTENSIONS.add(extension)
            except KeyError:
                UNKNOWN.add(extension) 
                NOT_DEFINED.append(full_name)

if __name__ == '__main__':
    folder = sys.argv[1]
    scan(Path(folder))
    print(f'Images jpeg: {JPEG_IMG}')
    print(f'Images jpg: {JPG_IMG}')
    print(f'Images png: {PNG_IMG}')
    print(f'AUDIO mp3: {MP3_AUDIO}')
    print(f'Archives zip: {ZIP_ARCH}')
    print(f'EXTENSIONS: {EXTENSIONS}')
    print(f'UNKNOWN: {UNKNOWN}')
    print(f'folders: {FOLDERS}')


