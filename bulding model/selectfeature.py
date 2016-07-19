##GLM modeling, plot with stat parameters
from sklearn.feature_selection import RFE
from sklearn.linear_model import LinearRegression
from sklearn.cross_validation import cross_val_predict
from sklearn import linear_model
import matplotlib.pyplot as plt
def computing_stat(X, Y):
   lr = LinearRegression()
   lr.fit(X, Y)
   #r^2 of model
#     lr.score(X, Y)
#     # The mean square error
#     print("Residual sum of squares: %.2f"
#           % np.mean((lr.predict(X) - Y) ** 2))
#     # Explained variance score: 1 is perfect prediction
#     print('Variance score: %.2f' % lr.score(X, Y))
   return np.mean((lr.predict(X) - Y) ** 2), lr.score(X, Y)

#return least sig feature
def remove_one_feature(X, Y, names):
   lr = LinearRegression()
   rfe = RFE(lr, n_features_to_select=1)
   rfe.fit(X,Y)
   rank = (sorted(zip(map(lambda x: round(x, 4), rfe.ranking_), names)))
   print(rank)
   return rank[-1][1]

total_feature = 298
drop_feature = [] #str type
num_feature = []
r2 = []
rss = []
feature = []
for i in range(total_feature-5):
   array = training.values
   Y = array[:,-1]
   X = array[:, 0:-2]
   names = training.columns
   rss_temp, r2_temp = computing_stat(X, Y)
#     print("fished stats")
   rss.append(rss_temp)
   r2.append(r2_temp)
   num_feature.append(total_feature-i)
   drop = remove_one_feature(X, Y, names)
#     print("fished remove one "+i)
   drop_feature.append(drop)
   training = training.drop(drop, axis=1)
   #print(i)