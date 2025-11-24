from evaluator import score_transcript

t = open("sample_transcript.txt").read()
scores, total = score_transcript(t)
print("Scores:", scores)
print("Total:", total)
