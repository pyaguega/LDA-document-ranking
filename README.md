Project using NLP AI to extract keyword-based topics from scientific reports.
First approach was using LDA, but turned out to be outdated and unsustainable.
Second approach was using BERT, a pre-trained large language model by Google. 
Final approach used SciBert, a scientific-language application of BERT, alongside a harmonic mean of cosine similarity and BM-25 metrics to rank documents by how well they reflected the query.
