# Open Information Extraction from Medical Papers

Welcome to the **Open Information Extraction (OIE)** project repository. The primary objective of this project is to leverage publicly available medical papers to extract valuable information using Open Information Extraction techniques. By utilizing various scripts and algorithms, this project aims to identify and organize information present within the documents into structured triples.

## Table of Contents

- [Introduction](#introduction)
- [Files](#files)
- [Usage](#usage)
- [Clustering Analysis](#clustering-analysis)
- 

## Introduction

The field of medical research generates a vast amount of textual data, which often contains hidden insights in the form of entities and their relationships. This project focuses on extracting valuable information from medical papers, specifically targeting entities of interest and their associations. The information extraction process involves multiple steps, including extraction of relevant sentences, processing, and ultimately generating structured triples for further analysis.

## Files

The following files are integral to the information extraction process:

- `extract_json.py` and `extract_xml.py`: These scripts extract sentences related to conflict of interest, acknowledgment, and funding from medical papers in JSON and XML formats, respectively.

- `process_coi.py`: This script takes the extracted sentences and splits them to generate inputs for the OIE model. The OIE model then generates triples in the form (subject, predicate, object) from these sentences.

- `extract_predicate_and_oie_result.py`: This script processes the triples obtained from the OIE model and organizes them into a dictionary, where paper links serve as keys and triples as values.

- `reverb_algo.py`: Utilizing the ReVerb algorithm, this script identifies and extracts additional triples that complement those obtained from the OIE model.

- `write_json.py`: Triples from both the OIE model and the ReVerb algorithm are combined with paper links, authors, and titles, and written into a JSON file for further analysis.

- `filtering_predicate.py`: This script filters the extracted predicates to retain only the most meaningful ones.

## Usage

To use this project, follow these steps:

1. Run `extract_json.py` or `extract_xml.py` to obtain sentences related to conflict of interest, acknowledgment, and funding.

2. Process these sentences using `process_coi.py` to generate inputs for the OIE model. Run the model and obtain triples.

3. Use `extract_predicate_and_oie_result.py` to organize OIE triples by paper links.

4. Employ `reverb_algo.py` to extract additional triples using the ReVerb algorithm.

5. Combine the triples obtained from both sources using `write_json.py`. The resulting JSON file will contain triples, paper links, authors, and titles.

6. For a more refined set of predicates, run `filtering_predicate.py`.

## Clustering Analysis

Apart from the main goal of extracting triples, this project also explores clustering of extracted predicates. The `silhouette_analyze.ipynb` notebook provides insights into clustering using the silhouette criterion and experimenting with DBScan clustering.


---
