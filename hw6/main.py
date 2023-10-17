from pathlib import Path
import shutil
import sys
import parser
from normalize import normalize

def handle_media(file_name: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    file_name.replace(target_folder / normalize(file_name.name))

def handle_archive(file_name: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    folder_for_file = target_folder / normalize(file_name.name.replace(file_name.suffix, ''))
    folder_for_file.mkdir(exist_ok=True, parents=True)
    try:
        shutil.unpack_archive(str(file_name.absolute()), str(folder_for_file.absolute()))
    except shutil.ReadError:
        folder_for_file.rmdir()
        return
    file_name.unlink()


def main(folder: Path):
    parser.scan(folder)
    for file in parser.JPEG_IMG:
        handle_media(file, folder / 'images' / 'JPEG')
    for file in parser.JPG_IMG:
        handle_media(file, folder / 'images' / 'JPG')
    for file in parser.PNG_IMG:
        handle_media(file, folder / 'images' / 'PNG')
    for file in parser.SVG_IMG:
        handle_media(file, folder / 'images' / 'SVG')

    for file in parser.MP3_AUDIO:
        handle_media(file, folder / 'audio' / 'MP3')
    for file in parser.OGG_AUDIO:
        handle_media(file, folder / 'audio' / 'OGG')
    for file in parser.WAV_AUDIO:
        handle_media(file, folder / 'audio' / 'WAV')  
    for file in parser.AMR_AUDIO:
        handle_media(file, folder / 'audio' / 'AMR')  

    for file in parser.AVI_VIDEO:
        handle_media(file, folder / 'video' / 'AVI')
    for file in parser.MP4_VIDEO:
        handle_media(file, folder / 'video' / 'MP4')
    for file in parser.MOV_VIDEO:
        handle_media(file, folder / 'video' / 'MOV')                                    
    for file in parser.MKV_VIDEO:
        handle_media(file, folder / 'video' / 'MKV')

    for file in parser.DOC_DOC:
        handle_media(file, folder / 'documents' / 'DOC')
    for file in parser.DOCX_DOC:
        handle_media(file, folder / 'documents' / 'DOCX')        
    for file in parser.TXT_DOC:
        handle_media(file, folder / 'documents' / 'TXT')        
    for file in parser.PDF_DOC:
        handle_media(file, folder / 'documents' / 'PDF')        
    for file in parser.XLSX_DOC:
        handle_media(file, folder / 'documents' / 'XLSX') 
    for file in parser.PPTX_DOC:
        handle_media(file, folder / 'documents' / 'PPTX')               
    for file in parser.PY_DOC:
        handle_media(file, folder / 'documents' / 'PY')        

    for file in parser.NOT_DEFINED:
        handle_media(file, folder / 'not_defined')

    for file in parser.ZIP_ARCH:
        handle_archive(file, folder / 'archives' / 'ZIP')
    for file in parser.GZ_ARCH:
        handle_archive(file, folder / 'archives' / 'GZ') 
    for file in parser.TAR_ARCH:
        handle_archive(file, folder / 'archives' / 'TAR')               

    for folder in parser.FOLDERS[::-1]: #delete empty folders
        try:
            folder.rmdir()
        except OSError:
            print(f'Error during remove folder {folder}')


if __name__ == "__main__":
    folder_process = Path(sys.argv[1])
    main(folder_process.resolve())