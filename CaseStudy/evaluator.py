# evaluator.py
import re, pandas as pd

filler_words = ["um","uh","like","you know","hmm","erm","ah","mm"]

def tokenize_words(text):
    return re.findall(r"\b[\w']+\b", text.lower())

def tokenize_sentences(text):
    s = re.split(r'(?<=[.!?])\s+', text.strip())
    return [x for x in s if x]

def count_filler(text):
    t = text.lower()
    return sum(len(re.findall(r"\b"+re.escape(fw)+r"\b", t)) for fw in filler_words)

def lexical_diversity(words):
    return len(set(words))/len(words) if words else 0

def score_transcript(transcript, rubric_path="sample_rubric.csv"):
    rub = pd.read_csv(rubric_path)
    words = tokenize_words(transcript)
    sents = tokenize_sentences(transcript)

    word_count = len(words)
    sent_count = len(sents)
    avg_sent_len = word_count/sent_count if sent_count else word_count
    filler_ratio = count_filler(transcript)/word_count if word_count else 0
    unique_ratio = lexical_diversity(words)

    tx = transcript.lower()
    kw = ["nman","non-academic","financial","emotional","eq","iq","creativity","multimodal","personalized","equity"]
    rel = sum(1 for k in kw if k in tx)/len(kw)*100

    clarity = max(0, 100*(1-abs(avg_sent_len-14)/10))
    clarity = 0.7*clarity + 0.3*(unique_ratio*100)

    conc = 100 if 60<=word_count<=140 else max(30, 100 - abs(word_count-100)/2)

    vocab = unique_ratio*100*0.8 + (1-filler_ratio)*100*0.2

    passion = 60

    creativity = 30 if "creativity" in tx else unique_ratio*40

    scores = {
        "Clarity & Structure": round(clarity,1),
        "Content Relevance": round(rel,1),
        "Conciseness": round(conc,1),
        "Vocabulary": round(vocab,1),
        "Passion": round(passion,1),
        "Creativity": round(creativity,1)
    }

    total = 0
    for _,r in rub.iterrows():
        total += scores[r['criterion']] * r['weight']

    return scores, round(total,1)

if __name__=="__main__":
    t = open("sample_transcript.txt").read()
    s, w = score_transcript(t)
    print(s)
    print("Weighted:", w)
