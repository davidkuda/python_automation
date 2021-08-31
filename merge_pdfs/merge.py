from datetime import datetime
from typing import List
import os
import glob

from PyPDF2 import PdfFileMerger


def get_timestamp() -> str:
	return '{:%Y-%m-%d__%H-%M-%S}'.format(datetime.now())


def get_pdf_file_paths(path: str = '.', filename: str = '*.pdf') -> str:
    for dirpath, dirnames, filenames in os.walk(path):
        file_paths = glob.glob(os.path.join(dirpath, filename))
        for file_path in file_paths:
            yield os.path.abspath(file_path)


def merge_pdfs(pdf_file_paths: List[str]) -> None:
	merger = PdfFileMerger()

	for pdf in pdf_file_paths:

		try:
			merger.append(pdf)

		except:
			print(f'Corrupt file: {pdf}')

	file_name = get_timestamp() + '.pdf'

	merger.write(file_name)
	merger.close()

if __name__ == '__main__':
	print('let\'s get ready to rumble!' )
