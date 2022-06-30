from typing import List
from gensim.models import Word2Vec
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from pathlib import Path



class DocToVec:
    
    def __init__(self, dataset:List[List] , vec_size = 200 , model_path = 'word2vec.model'):
        """ Here we train our model and calculate tf-idf weights.

        Args:
            dataset (List[List]): Each item of this list is a list of tokens obtained from a document.
            vec_size (int, optional): The size of the vector of each document. Defaults to 200.
            model_path (str, optional): The path of pre-trained model. If there is no file in the specified 
            path, It trains a model with the dataset and saves the trained model. Defaults to 'word2vec.model'.
        """

        self.vec_size = vec_size
        
        
        
        if not Path(model_path).is_file():
            print('There is no pre-trained model. Going to train a model ...')
            self.wordToVecModel = Word2Vec(
                window = 10,
                min_count=2,
                workers=4,
                vector_size = self.vec_size
            )
        
            self.wordToVecModel.build_vocab(dataset)
            
            self.wordToVecModel.train(
                dataset,
                total_examples = self.wordToVecModel.corpus_count,
                epochs = 20,
            )
            
            self.wordToVecModel.save(model_path)
            
        else:
            
            print('Loading the model ...')
            self.wordToVecModel = Word2Vec.load(model_path)
        
        con_train_data = [" ".join(a) for a in dataset]
        
        self.tfIdfVectorizer=TfidfVectorizer(use_idf=True,
                                        dtype = np.float64,
                                        lowercase = False,
                                        vocabulary = self.wordToVecModel.wv.index_to_key)
        
        self.tfIdfVectorizer.fit(con_train_data)
        
        dictionary = self.tfIdfVectorizer.get_feature_names()
        self.dictToNum = {d:i for i,d in enumerate(dictionary)}
        
        
    def embed(self, tokens:List):
        """Maps the input to a vector

        Args:
            tokens (List): List of tokens (don't forget to do preprocessing before 
            extracting tokens)

        Returns:
            Numpy Array: The vector of document
        """
        
        ti = self.tfIdfVectorizer.transform([" ".join(tokens)])
        
        weights = np.squeeze(np.asarray(ti[0].T.todense()))
        
        vec = np.zeros((self.vec_size,))
        sum_weights = 0
        for k in set(tokens):
            try:
                word_vec = self.wordToVecModel.wv[k]
                weight = weights[self.dictToNum[k]]
                vec += word_vec * weight
                sum_weights += weight
            except KeyError:
                pass
        vec /= sum_weights
        return vec
        
        
        
        