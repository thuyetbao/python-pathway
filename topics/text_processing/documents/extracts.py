# Global
import sys
import os
import argparse
import logging
import fnmatch
import random
from datetime import date

# Path Append
sys.path.append(os.path.abspath(os.curdir))

# Externals
import pandas as pd

# Internals
from src.documents import Document

# Internals
from topics.text_processing.documents.configs import (
    TEMP_DIR, SOURCES_DIR, OUTPUTS_DIR,
    SUPPORTED_FILE_TYPES, TRUNCATED_LENGTH
)

RANDOM_SEARCH_POOL=[
    "Việt Nam", 
    "thủy điện",
    "kỹ thuật",
    "Góc nhìn"
]

# Log
LOG = logging.getLogger(__name__)
logging.basicConfig(
    filename=os.path.join(TEMP_DIR, f"document_extract_{date.today().strftime('%Y%m%d')}.log"),
    encoding='UTF-8',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S |',
    format='%(asctime)s - %(levelname)s - Thread: %(thread)d - Message: %(message)s'
)

if __name__ == "__main__":

    # CLI binding
    parser = argparse.ArgumentParser(description="""
        Process document into files and metadata Atributes through CLI

        Synponis:
        py topics/text_processing/extract_documents.py --source SOURCE --destination DESTINATION
        
        Where
            SOURCE: sources contain multiple document in various files types (Default is 'data/sources')
            DESTINATION: destination of output generated by document extract process (Default is 'temp/document')

        Return:
            1. File contain metadata of documents. `F_DOCUMENT_METADATA.xlsx`
            2. File contain attributes of documents, such as paragraph with document-id `F_DOCUMENT_ATTRIBUTES.xlsx`
            3. Files both in excel, parquet file type

        Note:
            1. This default destination is ignore by git to not affected source code, please used with caution
            2. All logs will captured daily within suffix 'temp/extracts_YYYYMMDD.log'

        Examples:
        
        ```bash
        py --source data/sources/ --destination temp/document/
        ```
    """)
    parser.add_argument(
        "--source",
        dest='source',
        default=SOURCES_DIR, type=str,
        help="The sources of documents need to analyze"
    )
    parser.add_argument(
        "--destination",
        default=OUTPUTS_DIR, type=str,
        help="The destination of output parse"
    )
    args = parser.parse_args()

    # Log
    LOG.info("{:=^60}".format('Document Extraction'))
    LOG.info(f"Sources is: '{args.source}'")
    LOG.info(f"Destination is: '{args.destination}'")

    # List Files
    FILES=[]
    for root, dirs, files in os.walk(args.source):
        for f in files:
            if any([fnmatch.fnmatch(f, pat) for pat in SUPPORTED_FILE_TYPES]):
                FILES.append(os.path.join(root, f))

    # Log
    LOG.info(f"There are total of {len(FILES)} files that satisfied supported files type {','.join(SUPPORTED_FILE_TYPES)}")

    # Declare
    METADATA = pd.DataFrame([])
    ATTRIBUTE = pd.DataFrame([])

    # Interate
    for f in FILES:
        
        # Binding
        _doc = Document(path=f)
        _id = _doc.get_id()

        # Get Information
        _meta = _doc.get_metadata()
        _meta_df = pd.DataFrame.from_dict({x: [y] for x, y in _meta.items()})
        METADATA = pd.concat([METADATA, _meta_df])

        _attr = _doc.to_dataframe()
        ATTRIBUTE = pd.concat([ATTRIBUTE, _attr])

        # Snapshot 
        _document = _doc.get_document()
        _truncated_document = _document[:TRUNCATED_LENGTH] + '...' if len(_document) > TRUNCATED_LENGTH else _document
        _stat = _doc.statistics()
        LOG.info(f"""
            Document: {_id}
            Path: {_meta.get('path')}
            Meta: {_meta.get('path')}
            
            Statistics:
            > Number of Lines: {_stat.get('line')}
            > Number of Paragraph: {_stat.get('paragraph')}
            > Number of Sentences: {_stat.get('sentence')}
            > Number of Words: {_stat.get('word')}
            
            Truncated Document:
            {_truncated_document}
        """)

        _doc.get_content()
        _doc.get_paragraphs()
        _doc.get_sentences()
        _doc.get_words()
        _doc.get_tokens()
        _doc.get_metadata()
        _doc.to_dataframe()

        # Random in RANDOM_SEARCH_POOL and search in documents
        # Shuffle Search
        random.shuffle(RANDOM_SEARCH_POOL)
        _key_word = random.choice(RANDOM_SEARCH_POOL)
        LOG.info(f"Random search keyword value: {_key_word}")
        res=_doc.search(keyword=_key_word)
        LOG.info(f"Result: {res}")

        # Write
        _doc.write_excel(target=os.path.join(args.destination, "excel", f"{_id}.xlsx"))
        _doc.write_parquet(target=os.path.join(args.destination, "parquet", f"{_id}.parquet"))

    for obj, file_name in zip(
        [METADATA, ATTRIBUTE], 
        ["F_DOCUMENT_METADATA.xlsx", "F_DOCUMENT_ATTRIBUTES.xlsx"]
    ):
        with pd.ExcelWriter(os.path.join(args.destination, file_name), mode='w') as writer:
            obj.to_excel(writer, sheet_name='DATA', engine='xlsxwriter')