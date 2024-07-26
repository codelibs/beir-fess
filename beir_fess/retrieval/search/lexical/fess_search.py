from beir.retrieval.search import BaseSearch
import requests
import string
import tqdm
import time
from typing import List, Dict, Any


def sleep(seconds):
    if seconds:
        time.sleep(seconds)


class FessSearch(BaseSearch):
    def __init__(self, index_name: str, hostname: str = "http://localhost:8080", access_token: str = None,
                 language: str = "en", initialize: bool = True, bulk_size: int = 100, sleep_for: int = 2):
        self.results = {}
        self.initialize = initialize
        self.sleep_for = sleep_for
        self.index_name = index_name
        self.hostname = hostname
        self.access_token = access_token
        self.language = language
        self.bulk_size = bulk_size
        if self.initialize:
            self.initialise()
        symbols = string.punctuation
        self.translation_table = str.maketrans(symbols, ' ' * len(symbols))

    def initialise(self):
        response = requests.delete(f"{self.hostname}/api/admin/searchlist/query",
                                   headers={
                                       "Content-Type": "application/json",
                                       "Authorization": self.access_token
                                   },
                                   json={
                                       "q": "*:*"
                                   })
        if response.json().get("response", {}).get("status") != 0:
            raise ValueError("Failed to delete all documents.")

    def search(self, corpus: Dict[str, Dict[str, str]], queries: Dict[str, str], top_k: int, *args, **kwargs) -> Dict[str, Dict[str, float]]:

        # Index the corpus within Fess
        # False, if the corpus has been already indexed
        if self.initialize:
            self.index(corpus)
            # Sleep for few seconds so that Fess indexes the docs properly
            sleep(self.sleep_for)

        # retrieve results from BM25
        query_ids = list(queries.keys())
        queries = [queries[qid] for qid in query_ids]

        progress = tqdm.tqdm(unit="queries", total=len(query_ids))
        for query_id, query in zip(query_ids, queries):
            # Add 1 extra if query is present with documents
            docs = self._get_docs(query, top_k + 1)
            scores = {}
            for doc in docs:
                corpus_id = doc['corpus_id']
                score = doc['score']
                if corpus_id != query_id:  # query doesnt return in results
                    scores[corpus_id] = score
                self.results[query_id] = scores
            progress.update(1)
        progress.close()
        return self.results

    def _get_docs(self, query: str, size: int):
        results: List[Dict[str, Any]] = []
        response = requests.get(f"{self.hostname}/api/v1/documents",
                                headers={
                                    "Content-Type": "application/json",
                                },
                                params={
                                    "q": query,
                                    "start": 0,
                                    "num": size,
                                })
        if response.status_code == 200:
            for doc in response.json().get("data", []):
                results.append({
                    "corpus_id": doc.get("url").split('/')[-1],
                    "score": doc.get("score", 0.0)
                })
        return results

    def index(self, corpus: Dict[str, Dict[str, str]]):
        progress = tqdm.tqdm(unit="docs", total=len(corpus))
        def send_bulk(bulk_data):
            response = requests.post(f"{self.hostname}/api/admin/documents/bulk",
                                    headers={
                                        "Content-Type": "application/json",
                                        "Authorization": self.access_token
                                    },
                                    json={
                                        "documents": bulk_data
                                    })
            if response.json().get("response", {}).get("status") != 0:
                raise ValueError(f"response: {response.json()}")
            progress.update(len(bulk_data))
        docs: List[Dict[str, Any]] = []
        for idx in corpus:
            title = corpus[idx].get("title", "")
            if len(title) == 0:
                title = "-"
            content = corpus[idx].get("text", "")
            docs.append({
                "lang": self.language,
                "title": title,
                "content": content,
                "content_length": f"{len(content)}",
                "url": f"http://beir.codelibs.org/{self.index_name}/{idx}",
                "host": "beir.codelibs.org",
                "site": f"beir.codelibs.org/{self.index_name}/{idx}",
                "filename": f"{idx}.html",
                "mimetype": "text/plain",
                "filetype": "text",
                "click_count": 0,
                "favorite_count": 0,
                "boost": 1.0,
                "last_modified": "1970-01-01T00:00:00.000Z",
                "timestamp": "1970-01-01T00:00:00.000Z",
                "created": "1970-01-01T00:00:00.000Z",
                "role": ["Rguest"]
                })
            if len(docs) >= self.bulk_size:
                send_bulk(docs)
                docs = []
        if len(docs) > 0:
            send_bulk(docs)
        progress.close()
