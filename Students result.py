import numpy as np

scores = np.array([
    [78, 85, 90],
    [88, 79, 92],
    [84, 76, 88],
    [90, 93, 94],
    [75, 80, 70]
])

std_avg_score = np.mean(scores, axis=1 )
print(f"Students average scores:{std_avg_score.round(2)}")

sub_avg_score = np.mean(scores, axis=0)
print(f"Subjects average scores:{sub_avg_score.round(2)}")

total_score = np.sum(scores, axis=1)
high_std_score = np.argmax(total_score)
print(f"Student index with highest score:",high_std_score)

scores[:,2] +=5
print(f"Updated scores after bonus", scores)
