import pandas as pd
import matplotlib.pyplot as plt
csv_file='sherry.csv'
data = pd.read_csv(csv_file)
likes = list(data["likes"])[:50][::-1]
timestamp = list(data["time"])[:50][::-1]
x= timestamp
y= likes
plt.scatter(x,y)
plt.xlabel('timestamp->')
plt.ylabel('likes->')
plt.title('Insta')
plt.show()
