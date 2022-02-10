# Global
import os
import sys
import argparse
import yaml
import fnmatch
import logging
from datetime import date

# Path Append
sys.path.append(os.path.abspath(os.curdir))

# Internals
from topics.text_processing.documents.configs import (
    TEMP_DIR, SOURCES_DIR, SAMPLE_METADATA, SUPPORTED_FILE_TYPES
)

# Log
LOG = logging.getLogger(__name__)
logging.basicConfig(
    filename=os.path.join(TEMP_DIR, f"document_metadata_{date.today().strftime('%Y%m%d')}.log"),
    encoding='UTF-8',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S |',
    format='%(asctime)s - %(levelname)s - Thread: %(thread)d - Message: %(message)s'
)

if __name__ == '__main__':

    # CLI
    parser = argparse.ArgumentParser(description="""
        Metadata File Auto Parsing

        Synponis:
        py topics/text_processing/documents/extract_documents.py --source SOURCE --file FILE

        Where
            SOURCE: sources contain multiple document in various files types (Default is 'data/sources')
            FILE: single file to parse, it will replace the targeted source dir 
        
        Return:
            Metadata YML file in case there is not exists.
            
            Same file name with the targeted file list (or maybe single) with extension '*.yml'
            
            It included
            ---
            metadata:
                entity: null
                language: null
                number: null
                issued-date: null
                effective-date: null
                source: null
                subject: null
                title: null
                type: null
                is-internal: false
            ---

        Note:
            1. --file argument will have priority higher than --source argument 
            2. All logs will captured daily within suffix 'temp/metadatas_YYYYMMDD.log'

        Examples:
        
        ```bash
        py --source data/sources/
        ```
    """)
    parser.add_argument(
        "--source",
        dest='source',
        default=SOURCES_DIR, type=str,
        help="The sources of documents to parse metadata"
    )
    parser.add_argument(
        "--file",
        dest='file', 
        type=str,
        help="The sources of documents need to analyze"
    )
    args = parser.parse_args()

    # Log
    LOG.info(f"Working add metadata at source: {args.source}")

    # File Path
    if args.file is not None:
        if len([args.file]) != 1:
            raise Exception("The 'file' argument can't not have multiple value, please use one file only") 
        FILES = [args.file]
        for f in FILES:
            if os.path.isfile(f) is False:
                raise Exception(f"Not exists file '{f}'")
    else:
        for root, dirs, files in os.walk(args.source):
            FILES=[]
            for f in files:
                # Selected Filter
                if any([fnmatch.fnmatch(f, pat) for pat in SUPPORTED_FILE_TYPES]):
                    FILES.append(f)

    # Log
    #LOG.info(f"There are total of {len(FILES)} files that satisfied supported files type ") #{', '.join(SUPPORTED_FILE_TYPES)}

    # Add `*.yml` file
    for f in FILES:
        ffile = os.path.basename(f)
        fname, fext = os.path.splitext(ffile)
        fmeta_name = "{}.yml".format(fname)
        fmeta = os.path.join(args.source, fmeta_name)
        if not os.path.exists(fmeta):
            try:
                with open(fmeta, 'w') as file:
                    yaml.dump(SAMPLE_METADATA, file)
                LOG.info(f"[{FILES.index(f)+1}/{len(FILES)}] Created {fmeta_name} represented metadata for {ffile}.")
            except Exception as e:
                LOG.error(f"Error when create mapping metadata for {ffile} at '{args.source}'")
