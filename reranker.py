import os
os.environ["CUDA_VISIBLE_DEVICES"] = "1"
import json
import numpy as np
from intent_exs import IntentEXS
from pyserini.search.lucene import LuceneSearcher  
from beir.reranking.models import CrossEncoder

def search_intent(index_path, query):

    searcher = LuceneSearcher(index_path)   # load a searcher from pre-computed index.

    hits = searcher.search(query)

    # Print the first 10 hits:
    #for i in range(0, 10):
    #    print(f'{i+1:2} {hits[i].docid:15} {hits[i].score:.5f}')

    # extract the retrieved doc ids and doc contents.
    doc_ids = [hit.docid for hit in hits]
    docs = dict([(hit.docid, json.loads(searcher.doc(hit.docid).raw())['contents']) for hit in hits])

    # Load a reranking model
    model = 'cross-encoder/ms-marco-electra-base'
    reranker = CrossEncoder(model)

    # build query-doc pair for reranking model as input.
    sentence_pairs = []
    for doc_id in doc_ids:
        doc_text = docs[doc_id]
        sentence_pairs.append([query, doc_text])
    rerank_scores = reranker.predict(sentence_pairs, batch_size=1)

    # show reranked docs.
    reranked_docids = np.array(doc_ids)[np.argsort(rerank_scores)[::-1]]
    for i, doc_id in enumerate(reranked_docids):
        print('doc_id =', doc_id)
        #if i < 1:
        print('contents =', docs[doc_id])



    # build corpus for IntentEXS explain function
    corpus = {'query': query,
            'scores': dict([(doc_id, score) for doc_id, score in zip(doc_ids, rerank_scores)]),
            'docs': docs
    }
    params = {'top_idf': 10, 'topk': 5, 'max_pair': 100, 'max_intent': 10, 'style': 'random'}


    # Init the IntentEXS object.
    Intent = IntentEXS(reranker, index_path, 'bm25')
    expansion = Intent.explain(corpus, params)
    print(expansion)

    return expansion, docs[reranked_docids[0]]



if __name__== '__main__':
    index_path = '/home/wang/xaiss/datasets/scidocs/corpus_index'
    query = 'what is explainable AI'
    expansion, top_doc = search_intent(index_path, query)
    print(expansion)
