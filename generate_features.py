from spacy.lang.en import STOP_WORDS
import numpy as np
import json
import spacy
import time
import re
import os
import argparse

def load_model(model_name="en_core_web_lg"):
    # Calculate time to load model
    start_time = time.time()
    nlp = spacy.load(model_name)
    print('Time to load model: ', time.time() - start_time)

    return nlp

def features_extractor(model, DATASET_NAME='train'):
    # Load questions json to make template
    features = keywords = json.load(open('json_files/{}.json'.format(DATASET_NAME)))

    # Assign new empty list for keywords
    questions = keywords['data']
    keywords['data'] = []
    features['data'] = []
    count = 0

    for i, question in enumerate(questions):
        if i % 1000 == 0:
            print("{}/{} ({:.2f}%)".format(i, len(questions), 100*i/len(questions)))

        # Get meta data
        question_id = question['questionId']
        sent = question['question']
        question['keywords'] = []

        # Append answers to keyword list
        ans = min(question['answers'], key=lambda x: len(x))
        ans = ans.split(', ')
        for a in ans:
            # Increase keyword count (for indexing)
            count += 1
            # Create keyword data
            keyword = {
                "id": count,
                "questionId": question_id,
                "keyword": a,
                "isAnswer": True,
            }
            # Process with spaCy pipeline
            w = model(a)
            vector = np.zeros(300)
            for t in w:
                if t.text.lower() not in STOP_WORDS:
                    vector += t.vector
            vector /= np.linalg.norm(vector)
            # Create feature data
            feature = {
                "id": count,
                "feature": vector.tolist()
            }
            question['keywords'].append(keyword)
            keywords['data'].append(keyword)
            features['data'].append(feature)

        # Process with spaCy NLP pipeline
        doc = model(sent)

        # Extract VERB from sentence
        v_list = [ent for ent in doc if ent.pos_ == 'VERB']
        # Construct a keyword list with Noun Chunks, NER results, and VERBs.
        kw = list(doc.noun_chunks) + list(doc.ents) + v_list
        # Remove duplicates
        kw = list({x.text.lower():x for x in kw}.values())
        # Sort by their position in the sentence
        kw.sort(key=lambda x: re.search(re.escape(x.text.lower()), sent.lower()).start())

        for w in kw:
            # Increase keyword count (for indexing)
            count += 1
            # Create keyword data
            keyword = {
                "id": count,
                "questionId": question_id,
                "keyword": w.text,
                "isAnswer": False,
            }
            # Create feature data
            vector = np.zeros(300)
            if isinstance(w, spacy.tokens.token.Token): w = [w]
            for t in w:
                if t.text.lower() not in STOP_WORDS:
                    vector += t.vector
            vector /= np.linalg.norm(vector)
            
            feature = {
                "id": count,
                "feature": vector.tolist()
            }
            question['keywords'].append(keyword)
            keywords['data'].append(keyword)
            features['data'].append(feature)

    # Save data to json file 
    full = json.load(open('json_files/{}.json'.format(DATASET_NAME)))
    full['data'] = questions
    os.makedirs(f'{DATASET_NAME}_features', exist_ok=True)
    with open('{}_features/{}_with_keywords.json'.format(DATASET_NAME, DATASET_NAME), 'w') as fo:
        json.dump(full, fo)
    with open('{}_features/{}_keywords.json'.format(DATASET_NAME, DATASET_NAME), 'w') as fo:
        json.dump(keywords, fo)
    with open('{}_features/{}_features.json'.format(DATASET_NAME, DATASET_NAME), 'w') as fo:
        json.dump(features, fo)


if __name__ == "__main__":
    # Argparse keyword
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default='train', type=str)
    args = parser.parse_args()

    # Load model 
    nlp_model = load_model()
    try:
        features_extractor(nlp_model, args.data)
    except:
        assert "Wrong keyword. Please try again."