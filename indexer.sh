python -m pyserini.index -collection JsonCollection \
                         -generator DefaultLuceneDocumentGenerator \
                         -threads 1 \
                         -input /home/wang/xaiss/datasets/scidocs/corpus_json \
                         -index /home/wang/xaiss/datasets/scidocs/corpus_index \
                         -storePositions -storeDocvectors -storeRaw \
                         -stemmer 'krovetz'