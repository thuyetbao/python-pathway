import os
import string
import re
import hashlib
import pandas as pd
from thefuzz import process
import yaml

class Document(object):
    """Document is a class represented for any files in various type (txt, path, png)
    then bake it into a mechanic to enrich document metadatas.

    Return:
        [Document]: Document Class 

    Example:
        samp = Document(path='data/sources/sample.txt')
        samp.write_parquet('temp/t.parquet')
        samp.write_excel('temp/t.xlsx')
    """
    
    def __init__(self, path: str = None):

        # Mechanic
        self.path = path
        self.original_path, self.file = os.path.split(self.path)
        self.file_name, self.file_ext = os.path.splitext(self.file)
        self.file_metadata = os.path.join(self.original_path, self.file_name + ".yml")
        
        metadata = {}
        if os.path.isfile(self.file_metadata):
            # Metadata
            try:
                with open(self.file_metadata) as f:
                    metadata = yaml.load(f, Loader=yaml.FullLoader).get('metadata')
            except Exception:
                self.file_metadata = None
                raise Exception
        else:
            import subprocess
            try:
                subprocess.run(
                    ['py', 'topics/text_processing/documents/metadatas.py', '--file', self.file_metadata], 
                    capture_output=True, text=True, check = True, timeout=60
                )
            except Exception:
                self.file_metadata = None
                raise Exception

        # Attributes
        self.language = safe_dict_extract(d = metadata, key = 'language')
        self.title = safe_dict_extract(d = metadata, key = 'title')
        self.subject =  safe_dict_extract(d = metadata, key = 'subject')
        self.entity = safe_dict_extract(d = metadata, key = 'entity')
        self.source = safe_dict_extract(d = metadata, key = 'source')
        self.number = safe_dict_extract(d = metadata, key = 'number')
        self.type = safe_dict_extract(d = metadata, key = 'type')
        self.issued_date = safe_dict_extract(d = metadata, key = 'issued-date')
        self.effective_date = safe_dict_extract(d = metadata, key = 'effective-date')
        self.is_internal = safe_dict_extract(d = metadata, key = 'is-internal')

        # Components
        self.id = f"D{hashlib.md5(self.file.encode()).hexdigest()}"
        self.document = self._read_document()
        self.content = self._extract_content()
        self.paragraphs, self.sentences, self.words =  self._parse_dictionary()
        self.tokens = self._get_unique_words()
        self.document_dataframe = self._content_to_df()

    def _read_document(self):
        
        # Validate File Exits
        if not os.path.isfile(self.path):
            raise FileNotFoundError('There are folder, not exists any file. Check your path')
        
        # Processing
        if self.file_ext == ".txt":
            with open(self.path, 'r', encoding='UTF-8') as f:
                cont = f.read()
        elif self.file_ext in (".doc", ".docx"):
            import textract
            parse_content = textract.process(self.path, input_encoding='UTF-8', output_encoding='UTF-8', extension=self.file_ext).decode('UTF-8')
            cont = ''.join(parse_content)
        else:
            raise Exception(f"Currently not supported this extentsion {self.file_ext}")

        # Decoding
        content = cont.encode('UTF-8', "ignore").decode('UTF-8')

        # Replace Whitespace
        # \u200b is a "zero-width-space" in Unicode.
        # Ref: https://stackoverflow.com/questions/35657620/illegal-character-error-u200b
        content = content.replace(u'\u200b', ' ').replace('  ', ' ')

        # Special Chraracter
        # Ref: https://stackoverflow.com/questions/5843518/remove-all-special-characters-punctuation-and-spaces-from-string
        content = re.sub('\W+', ' ', content).strip()

        return content


    def _extract_content(self):

        # Special Character
        # b'\xe2\x80\x93' -> TODO: Need to revert to bytes then excluded Special characters

        # Define
        contents = {}
        _paragraph = list(filter(lambda x: x not in ('', string.punctuation), self.document.split('\n\n')))

        # Paragraphs
        for ind_par, par in zip(range(1, len(_paragraph) + 1), _paragraph):

            sentences = {}
            _sentences = list(filter(lambda x: x not in ('', string.punctuation), par.split('\.')))
            
            # Sentences
            for ind_sen, sen in zip(range(1, len(_sentences) + 1), _sentences):

                words = {}
                _words = list(filter(lambda x: x not in ('', string.punctuation), sen.split()))

                # Words
                for ind_wor, wor in zip(range(1, len(_words) + 1), _words):
                    words.update({ind_wor: {
                        'position': ind_wor,
                        'word': wor
                    }})

                sentences.update({ind_sen: {
                    'position': ind_sen,
                    'sentence': sen,
                    'words': words
                }})

            contents.update({ind_par: {
                'position': ind_par,
                'paragraph': par,
                'sentences': sentences
            }})

        return contents

    def _parse_dictionary(self):
        
        all_paragraphs = []
        all_sentences = []
        all_words = []
        
        for i in range(len(self.content)):
            all_paragraphs.append(self.content.get(i+1).get('paragraph'))
            sents = self.content.get(i+1).get('sentences')
            for j in range(len(sents)):
                all_sentences.append(sents.get(j+1).get('sentence'))
                words = sents.get(j+1).get('words')
                for k in range(len(words)): 
                    w = words.get(k+1).get('word')
                    all_words.append(w)

        paragraphs_dict = {}
        for ind, p in zip(list(range(1, len(all_paragraphs) + 1)), all_paragraphs):
            paragraphs_dict.update({ind: {
                'position': ind,
                'paragraph': p
                }
            })

        sentences_dict = {}
        for ind, s in zip(list(range(1, len(all_sentences) + 1)), all_sentences):
            sentences_dict.update({ind: {
                'position': ind,
                'sentence': s
                }
            })

        word_dict = {}
        for ind, w in zip(list(range(1, len(all_words) + 1)), all_words):
            word_dict.update({ind: {
                'position': ind,
                'word': w
                }
            })
        
        return paragraphs_dict, sentences_dict, word_dict


    def _get_unique_words(self):
        all_words = []
        for i in range(len(self.words)):
            all_words.append(self.words.get(i+1).get('word'))
        return list(set(all_words))

    def _content_to_df(self):
        _tabu_tuples = []
        for cont, ty in zip(
            [self.paragraphs, self.sentences, self.words],
            ['paragraph', 'sentence', 'word']
        ):
            for _posi in range(1, len(cont)):
                _info = cont[_posi]
                _value = _info.get(ty)
                _tabu_tuples.append((self.id, ty, _posi, _value, hashlib.md5(_value.encode()).hexdigest()))
        df = pd.DataFrame(_tabu_tuples,columns=['document_id', 'type', 'position', 'value', 'hashed_content_md5'])
        return df
        
    def write_excel(self, target):

        # Valid File
        if self.check_valid_ext(target, "xlsx") is False:
            raise ValueError(f"Target file not good {target}")

        with pd.ExcelWriter(target, mode='w') as writer:
            self.document_dataframe.to_excel(writer, sheet_name='DATA', engine='xlsxwriter')

    def write_parquet(self, target):

        # Valid File
        if self.check_valid_ext(target, "parquet") is False:
            raise ValueError(f"Target file not good {target}")

        self.document_dataframe.to_parquet(path=target)

    def get_id(self):
        return self.id

    def get_document(self):
        return self.document

    def get_content(self):
        return self.content

    def get_paragraphs(self):
        return self.paragraphs

    def get_sentences(self):
        return self.sentences

    def get_words(self):
        return self.words

    def get_tokens(self):
        return self.tokens

    def get_metadata(self):
        return {
            'id': self.id,
            'language': self.language,
            'title': self.title,
            'subject': self.subject,
            'entity': self.entity,
            'source': self.source,
            'type': self.type,
            'issued_date': self.issued_date,
            'effective_date': self.effective_date,
            'is_internal': self.is_internal
        }

    def to_dataframe(self):
        return self.document_dataframe

    def statistics(self):
        return {
            'paragraph': len(self.content),
            'sentence': len(self.sentences),
            'word': len(self.words)
        }

    def update_metadata(self, path: str = None):
        fi = os.path.basename(path)
        fin, fie = os.path.split(fi)
        if os.path.isfile(path) and fie == 'yml':
            if path != self.file_metadata:
                # Metadata
                try:
                    with open(self.file_metadata) as f:
                        metadata = yaml.load(f, Loader=yaml.FullLoader).get('metadata')
                except Exception:
                    self.file_metadata = None
                    raise Exception

        # Update
        self.language = safe_dict_extract(d = metadata, key = 'language')
        self.title = safe_dict_extract(d = metadata, key = 'title')
        self.subject =  safe_dict_extract(d = metadata, key = 'subject')
        self.entity = safe_dict_extract(d = metadata, key = 'entity')
        self.source = safe_dict_extract(d = metadata, key = 'source')
        self.number = safe_dict_extract(d = metadata, key = 'number')
        self.type = safe_dict_extract(d = metadata, key = 'type')
        self.issued_date = safe_dict_extract(d = metadata, key = 'issued-date')
        self.effective_date = safe_dict_extract(d = metadata, key = 'effective-date')
        self.is_internal = safe_dict_extract(d = metadata, key = 'is-internal')

    def search(self, keyword: str, limit: int = 10, threshold: int = 50):
        _satified = []
        for wo, ty in zip(
            [self.paragraphs, self.sentences, self.words],
            ['paragraph', 'sentence', 'word']
        ):
            seach_pool = wo.values()
            _pool = process.extract(keyword, seach_pool, limit=limit)
            for w, thr in _pool:
                if thr >= threshold:
                    _satified.append((ty, w, thr))
        return _satified

    @staticmethod
    def check_valid_ext(path, ext):
        ffile = os.path.basename(path)
        fname, fext = os.path.splitext(ffile)
        result = False
        if fext == "." + ext:
            result = True
        return result

    def _check_file(path):
        result = False
        if os.path.isfile(path):
            result = True
        return result


def safe_dict_extract(d: dict = {}, key: str = None):
    return d.get(key) if d.get(key) is not None else None
