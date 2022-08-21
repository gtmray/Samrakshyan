import os
import matplotlib.pyplot as plt
import seaborn as sns
plt.rcParams.update({'font.size': 22})
sns.set()

bird_count = {}
DATA_PATH = '/content/drive/MyDrive/10SecSplitMajor'
BIRDS = os.listdir(DATA_PATH)

for bird in BIRDS:
    bird_count[bird] = len(os.listdir(os.path.join(DATA_PATH, bird)))

k = sorted(bird_count.items(), key=lambda x:x[1], reverse=True)
x = [i[0] for i in k]
y = [i[1] for i in k]

plt.figure(figsize=(20, 10))
ax = sns.barplot(x, y, color='black')
for p in ax.patches:
    ax.annotate(str(int(p.get_height())), (p.get_x() * 1.005, p.get_height() * 1.005))
plt.title('All audio files count after 10 seconds splitting', fontsize=15)
plt.xlabel('Birds', fontsize=15)
plt.ylabel('Files Count', fontsize=15)
ax.tick_params(axis='both', which='major', labelsize=15)
plt.xticks(rotation=90)