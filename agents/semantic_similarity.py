"""Agent comparing semantic similarity between sentences"""

from sentence_transformers import SentenceTransformer, util

class semanticAgent():
    def __init__(self, path):
        self.model= SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        self.task='semantic_similarity'
    
    def compare_sentences(self, sentence1, sentence2):
        # Encode sentences to get their embeddings
        embedding1 = self.model.encode(sentence1, convert_to_tensor=True)
        embedding2 = self.model.encode(sentence2, convert_to_tensor=True)

        # Compute cosine similarity
        similarity = util.pytorch_cos_sim(embedding1, embedding2).item()
        
        return similarity
    
    def get_scores(self, blind_agent_answer, options):
        scores=[]
        for sentence in options:
            similarity=self.compare_sentences(sentence, blind_agent_answer)
            scores.append(similarity)
        return scores.index(max(scores)), scores

    