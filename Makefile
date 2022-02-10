SHELL=/usr/bin/bash

document_dir=topics/text_processing/documents
document_source=data/sources
document_destination=temp/document

# Example:
# make document-metadata dir=topics/text_processing/documents source=data/sources
document-metadata:
	py ${document_dir}/metadatas.py --source ${document_source}


document-extract:
	py ${document_dir}/extracts.py --source ${document_source} --destination ${document_destination}
