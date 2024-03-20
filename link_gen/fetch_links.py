
# import faiss
import numpy as np

class FaissSearch:
    def __init__(self) -> None:
        pass

    def index_search(self,user_input,embeddings,model):
        index=faiss.IndexFlatL2(embeddings.shape[1])
        index.add(embeddings)
        query_distance=model.encode([user_input])[0]

        distances,indexes=index.search(np.array([query_distance]),k=2)
        return distances,indexes
