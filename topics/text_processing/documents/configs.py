import sys
import os

# Path Append
sys.path.append(os.path.abspath(os.curdir))

# Config
# Folder
TEMP_DIR = os.path.join('temp')
SOURCES_DIR = os.path.join('data', 'sources')
OUTPUTS_DIR = os.path.join(TEMP_DIR, 'document')

# Variable
SUPPORTED_FILE_TYPES = ["*.doc", "*.docx", "*.doc", "*.txt"]
TRUNCATED_LENGTH=500
SAMPLE_METADATA = {
    'metadata': {
        'language': None,
        'title': None,
        'subject': None,
        'entity': None,
        'source': None,
        'number': None,
        'type': None,
        'issued-date': None,
        'effective-date': None,
        'is-internal': True
    }
}
