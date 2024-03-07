from sentence_transformers import SentenceTransformer


class Embedding:

  def __init__(self):
    pass

  def get_embedding(self, sentences):
    model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
    embeddings = model.encode(sentences)

    return embeddings ,model   

  
