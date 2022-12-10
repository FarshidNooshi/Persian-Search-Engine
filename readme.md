<div align="center">
<h1> In The Name Of GOD </h1>
</div>

# Persina Search Engine
[![License: APACHE-2.0](https://img.shields.io/github/license/FarshidNooshi/Information-Retrieval)](https://opensource.org/licenses/Apache-2.0)
![GitHub contributors](https://img.shields.io/github/contributors/FarshidNooshi/Information-retrieval)

# About The Project

This Project is For my Information Retrieval Course Project which was three phases and has various techniques in information retrieval such as TF-IDF scoring, Clusterring techniques and ... . below is a brief introduction to this course.

# Preprocessing Section

For all query answering approaches, we need a positional posting list which is extracted in Phase 1 section
Also for word embedding purposes, a word to vector model is constructed.

# Categorization

In order to answer queries fast enough, we need to categorize documents and queries. 
In third section a **KNN** Approach is implemented
In third section an unsupervised approach is implemented using the **K-means algorithm**.

# Query answering

Multiple query answering approaches are implemented:
+ Simple common word counting approach in Phase 1 and 2.
+ An approach based on inner product and tf-idf in Phase 2 which uses champion lists in order to speed up.
+ A word embedding-based approach with inner product criteria in Phase 1.
+ A fast version of the word embedding approach in Phase 2 which uses clusters in order to speed up.
+ A category aware approach in Phase 3 that user enters the category along with the query itself.
+ Bulk inserting data to the ElasticSearch and using ElasticSearch as another solution for using in products in Phase 3.

---

# Information Retrieval

Information retrieval is the process through which a computer system can respond to a user's query for text-based information on a specific topic. Web search is one of the most important applications of information retrieval techniques and an area in which most people interact with IR systems. The goal of this course is to introduce students with the basics, models, tools and applications of the modern information retrieval.

# Contents

This repository is for my Information Retrieval course project at the Amirkabir University of Technology and contains the following files:

- [Phase1.md](Phase_1): the first phase of the project.
- [Phase2.md](Phase_2): the second phase of the project.
- [Phase3.md](Phase_3): the third phase of the project.
- [notebooks.md](notebooks): the notebooks for the project.

## Topics 

The topics in this course are:

- **Text Preprocessing and vocabulary construction**
  - Document and word separation
  - Normalization
  - Stemming and lemmatization
  - Spelling correction
- **Indexing**
  - Index construction
  - Index compression
- **Retrieval and ranking methods**
  - Boolean, Vector-based, Probabilistic Retrieval
- **Performance evaluation for information retrieval methods**
- **Query languages and operators**
- **Document classification and clustering**
- **Web search**
  - Basics
  - Crawling
  - Link analysis
- **IR-based applied systems**

# Instructor

The Information Retrieval course in Spring 2022 at the Computer Engineering Department in Amirkabir University of Technology is taught by:
[**Assoc. Prof. Ahmad Nickabadi**](https://scholar.google.com/citations?user=pSMNSZwAAAAJ&hl=en)

# Textbook

C. D. Manning, P. Raghavan, H. Schütze, Introduction to Information Retrieval, Cambridge University Press. 2008.
