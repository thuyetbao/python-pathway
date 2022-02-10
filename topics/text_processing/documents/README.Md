# **Document Search Application - Hackathon Solution**

## **Overview**

This repo folks source code from the backend component that we implemented in our **Document Resources Management System Mobile App** in the One Mount Hackathon contest has been organized at Ha Noi, 2021. Our solution matches with feasibility to implement and be a workable prototype.

Our application contains a search engine to search all legal documents in our company, and solved problems that we faced in our workplace:

+ Its supports full-text search, instead of searching from metadata only (title, abstracts, short description,...), then reduced time to deep-dive into the body of document when the users see matches keyword.

+ Its centralization knowledge, follow the `single source of truth` principle and is served through friendly UI in mobile.

+ It contains interactive modules that connect with user data, such as search behaviors, related documents to build a persona box with useful information.

**Logic Implemented**

By researching a lot of paper walkthroughs, we adopt the following components that we try to deploy to our systems.

![Hackathon-OM-Logic-System-Design](/assets/images/hackathon/Hackathon-Logic-System-Design.png)

**Architecture**   

By leveraging our cloud infrastructure, we used a lot of products offered by Google to deliver our backend components: 

+ Schedule, Functions: Cloud Schedule, Cloud Functions, Data Proc

+ Text Extract, Transformation: Translation API, Vision API, Natural Language API

+ Storage: BigQuery, Cloud Storage

Then, we use low-code Outsystems to build Front End component that will pack our information and served it through the mobile application. We put Front End/Back End in different virtual machine instances (for securities purposes)

![Hackathon-OM-SAD](/assets/images/hackathon/Hackathon-SAD.png)

Based on that, behind the scenes, we have designed a data pipeline to extract information and information from our document.

**Data Pipelines**

There is a consistent process that the Back End component will cover for the document journeys. The diagram below will show that:

![Hackathon-OM-SAD](/assets/images/hackathon/Hackathon-Interactive-Steps.png)

When document owners or operators publish a document into the system, the Backend then triggers the following four steps:

**Step 1**:  Metadata, Document Read.

This step pulls metadata of the document based on the fill-in of the user through operation UI with the below sample:

```yml
metadata:
    entity: Company Sample A
    language: VIE
    number: "No. 120"
    issued-date: 2021-11-04
    effective-date: 2022-01-01
    source: Business Development
    subject: Strategic Opportunities Template
    title: Strategic Opportunities Template
    type: Internal Regulation
    is-internal: true
```

The number of annotating metadata from a document will be increased time-to-time because it can be input by the document owner or operators, some can be extracted automatically based on text mapping then still need to be verified later. 

Then, we read the document and convert it into a text file `*.txt` and translate English/Vietnamese depending on the language of the document. 

The endpoint of this step has three files: metadata in `.yml`, two text files in desired languages

**Step 2**: At our core, we designed a Document class that has some methods listed below:

Method Table

| Method | Feature | Description | Is Public |
| :----- | :------ | :---------- | :-------- |
| _read_document |  Process document | Process to parse document information from files, supported file type are text `*.txt`, word (`*.doc`, `*.docx`), and with Vision API, we can support PDF files (`*.pdf`) and images (`*.png`)  | False  |
| _extract_document |  Extract Content | Based on the processed text, we parse the document into one dictionary paragraphs, sentences, words for both English and Vietnamese, return a dictionary of position and types relative  | False  |
| _parse_dictionary |  Separated Content Components | Separated dictionary into single dictionary with following synopsis `{'position': number, 'components': string}` | False  |
| _get_unique_words | Tokens create | Created set of words using in document | False  |
| _content_to_df | Document tabular form | Parse content of document into data frame | False  |
| check_valid_ext | Util - Validation extension of file | Check for the extension of the file with target extension | True  |
| _check_file | Util - Validation file exists | If the file exists, return True, else False, instead of error | False  |
| get_id | Get the ID of Document | Hashed generate based on the file name. Example: Db9c73ec7aee3cbc103a29d07938b5c39 | True  |
| get_document | Get document | Document text that read from source | True  |
| get_content | Get contents | Dictionary of all components of the document, including paragraphs, sentences, words | True  |
| get_paragraphs | Get paragraphs | Dictionary of paragraphs only. Example: `{'position': 1, 'paragraph': "This is first paragraph, included multiple rows"}` | True  |
| get_sentences | Get sentences | Dictionary of sentences only. Example: `{'position': 1, 'sentence': "This is first sentence"}`  | True  |
| get_words | Get words | Dictionary of words only. Example: `{'position': 1, 'word': "This"}`  | True  |
| get_tokens | Get lists | Array that contains set of words | True  |
| get_metadata | Get Metadata | Dictionary of metadata that get from document owner | True  |
| to_dataframe | Get Dataframe | Dataframe of document | True  |
| statistics | Document basic statistics | Dictionary of basic statistics, count number of contents (number of paragraphs, number of sentences, number of words) | True  |
| write_excel | Write to Excel | Write data frame into excel file | True  |
| write_parquet | Write to Parquet | Write dataframe into parquet file | True  |
| update_metadata | Update Metadata | When there are updated metadata information, then we trigger information related to document | True  |
| search | Simple search backbone by `thefuzz` library | Search keyword in a document then returned related components with limit and threshold | True  |


**Step 3**: Storage Output

We then store the output we gather from steps 1 and 2 into a database:

1. Raw files [Uploaded file, Process Text, Translated Text, Metadata] will go to Cloud Storage.

2. The content of the document in the data frame will go to BigQuery to transform around more steps to become useful information.

**Step 4**: Data Models

Based on the data from step 3, we can generate various useful targeted outputs that support use-case in the UI functional. We then, combined from both user search processors, the related of the document to create new data models and backed by using `dbt (data build tool)` in BigQuery environment.

Let example:

1. Synonym Keyword: all suggest related words based on keywords, separated by `|`.

```
keyword:
    string: Ha Noi
    related: Ho Chi Minh|Hai Phong|Ninh Binh|Vinh Phuc
```

2. Most Search: at least top-N search in a period.

```
most_search:
    1: Salary
    2: License
    3: Tax
    ...
```

We then can serve it through API for Front End can get from that with updated data, can be in real-time.

## **Quickstart**

So at this repo, we mirror steps 1 and 2 which cover the baking journey from sources and focus on the usage of Document class.
Below will represent the source code folders and files hierarchy.

```bash
.
src/
|____ documents/ # Document Module
    |____ __init__.py  
    |____ __version__.py # Version of module
    |____ documents.py # Document Class
topics/
|____ text_processing/  
    |____ document/ # Pipelines
        |____ __init__.py
        |____ configs.py # Configuration file
        |____ extracts.py # Extract Document Information
        |____ metadatas.py # Parse metadata
        |____ README.Md

Makefile # has 2 targets related to Document
```

1. Installment:

    We used python version 3.9.1 and install dependencies

    ```
    py -m pip install pandas>=1.1.5 thefuzz==0.19.0
    ```

2. Configuration:

    You can skip this because it set up a default for the three folders below,
    or you can replace in [configs file](configs.py)

    `TEMP_DIR`: temporary folder, which contains a log file

    `SOURCES_DIR`: source of files, which has been stored raw file from uploaded document.
    
    `OUTPUTS_DIR`: source of processed file and data extraction. 

    Remember this, this can be largely based on the file sizes, so remember to put the file into `.gitignore` to not affect the codebase.

    Based on the number of handle read the document from file type, we can extend or reduced the glob file extension we can support. `SUPPORTED_FILE_TYPES` currently support ["*.doc", "*.docx", "*.doc", "*.txt"].

3. Using CLI to interactive with module:

    Added metadata for the source folder, if not exists related `*.yml` file.

    ```bash
    py topics/text_processing/documents/metadatas.py --source data/sources/
    ```

    Extract information and send it to the destination folder.

    ```bash
    py topics/text_processing/documents/extracts.py --source data/sources/ --destination temp/document
    ```
    
    or, with `Makefile`, we will have 2 targets that automatically process above. You can change the config variables declared with the `document_*` prefix.

    ```Makefile
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
    ```

    Then, we can use it by below command:

    ```bash
    make document-metadata
    make document-extract
    ```

    After all, you can see all things in the destination folder. E.g:

    ![Hackathon-Sample-Output](/assets/images/hackathon/Hackathon-sample-output-folders.png)

    with:

    `F_DOCUMENT_METADATA.xlsx` will likely like this

    ![Hackathon-Sample-Output](/assets/images/hackathon/Hackathon-sample-output-F_METADATA.png)

    `F_DOCUMENT_METADATA.xlsx` will likely like this

    ![Hackathon-Sample-Output](/assets/images/hackathon/Hackathon-sample-output-F_ATTRIBUTES.png)

    

## **Note**

1. Replica Source Code: This is just fragmented code, represented around 35% proposition compared to what we implemented in the contest. Its has enhancement with code style and package it into a module. 

2. We welcome idea contributions and comments/feedback for our solutions.

## **Our Team**

Our team has five members who come from various sub-company in One Mount and have different backgrounds (Human Resources, Sales Development, Technology, and Data).

1. Viet, Nguyen Thi Hong. [VinID Pay]
2. Trang, Luu Thi Linh. [VinID Pay]
3. Long, Nguyen Thanh. [One Mount]
4. Quan, Huynh Thanh. [One Mount]
5. Bao, Truong Thuyet. [One Mount]

Details information, images, screenshots about the competition have been published in [One Mount Official Facebook](https://www.facebook.com/onemountgrp/posts/437679634752435).

## **Source Referrences**

1. Text Analysis Pipelines [Towards Ad-hoc Large-Scale Text Mining] of Henning Wachsmuth
