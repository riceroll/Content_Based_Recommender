# Content_Based_Recommender
Recommender academic articles with content-based recommender.

## Introduction
Use content-based recommender to recommend papers most similar to a specific paper based on their content. The similarity can be adopted as the rating between papers, and collaborative filtering recommender can use the rating matrix to recommend papers better. The code of collaborative filtering is [here](https://github.com/riceroll/Collaborative_Filtering_Recommender).

### Dataset
Abstracts of academic articles from fields natural language processing, which is crawled from IEEE and ACM.

## Requirements

- Python-2.7
- nltk(python)

## Quick Start
Run the recommender by typing:
```bash
python CB_Recommender.py [serial_number(int)=the serial number of the paper]
```

To use your own data, change the variable 'file_papers' to load your data.


## References

- [Natural Language Toolkit](http://www.nltk.org/)
