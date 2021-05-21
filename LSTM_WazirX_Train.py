#import packages
import pandas as pd
import numpy as np

#to plot within notebook
import matplotlib.pyplot as plt

#importing required libraries
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM
from keras.models import model_from_json


#setting figure size
from matplotlib.pylab import rcParams
rcParams['figure.figsize'] = 20,200

#for normalizing data
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler(feature_range=(0, 1))

#read the file
df = pd.read_csv('Stockvol.csv')

#print the head



#setting index as date
df["['date'"] = [str(x).split("'")[1] for x in df["['date'"]]
# print(df[" 'BTC/USDT'"])

df["['date'"] = pd.to_datetime(df["['date'"])#,format='%Y-%m-%d %H:%M')
df.index = df["['date'"]


df=df.rename(columns={"['date'":"Date"})
df=df.rename(columns={" 'BTC/USDT'":"Close"})


#creating dataframe
data = df.sort_index(ascending=True, axis=0)
new_data = pd.DataFrame(index=range(0,len(df)),columns=['Date', 'Close'])
last=0



for i in range(0,len(data)):
    new_data['Date'][i] = data['Date'][i]
    new_data['Close'][i] = data['Close'][i]
    last = data['Close'][i]
    ld = data['Date'][i]


# new_data=new_data[20000:]
# print(new_data.head())

# plt.plot(new_data[['Close']])
# plt.show()

# print(ld)
sss=  (pd.date_range(ld, periods=91, freq="min"))
ld=[]
for xx in sss:
    ld.append(str(xx))
# print(new_data['Date'][i-1])
# ld=ld[1:]

# print(ld)

for x in range(1,90):
    new_data.loc[len(new_data.index)+x] = [ld[x],last] 

print(new_data[-13:])

#setting index

new_data.index = new_data.Date
new_data.drop('Date', axis=1, inplace=True)

#creating train and test sets
dataset = new_data.values
ll=len(dataset)-90
vl=ll//9
tl=ll-vl
# print(type(new_data))
# for x in range(90):
#     dataset= np.append(dataset,[[last,]],axis=0)
#     new_data.loc[len(new_data.index)+x] = [last] 

train = dataset[0:tl,:]
valid = dataset[tl:,:]

# print(valid)

# converting dataset into x_train and y_train
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(dataset)

# print(scaled_data)


x_train, y_train = [], []
for i in range(200,len(train)):
    x_train.append(scaled_data[i-200:i,0])
    y_train.append(scaled_data[i,0])
x_train, y_train = np.array(x_train), np.array(y_train)

# print(x_train)

x_train = np.reshape(x_train, (x_train.shape[0],x_train.shape[1],1))

# print(x_train)


# create and fit the LSTM network
model = Sequential()
model.add(LSTM(units=400, return_sequences=True, input_shape=(x_train.shape[1],1)))
model.add(LSTM(units=400))
model.add(Dense(1))

model.compile(loss='mean_squared_error', optimizer='adam')
model.fit(x_train, y_train, epochs=1, batch_size=1, verbose=2)

#predicting 246 values, using past 200 from the train data
inputs = new_data[len(new_data) - len(valid) - 200:].values
inputs = inputs.reshape(-1,1)
inputs  = scaler.transform(inputs)

X_test = []
for i in range(200,inputs.shape[0]):
    X_test.append(inputs[i-200:i,0])
X_test = np.array(X_test)

X_test = np.reshape(X_test, (X_test.shape[0],X_test.shape[1],1))
closing_price = model.predict(X_test)
closing_price = scaler.inverse_transform(closing_price)


# serialize model to JSON
model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
model.save_weights("model.h5")
print("Saved model to disk")
 


# rms=np.sqrt(np.mean(np.power((valid-closing_price),2)))
# print(rms)



#for plotting
train = new_data[:tl]
valid = new_data[tl:]

print(len(closing_price))
print(len(valid))


valid['Predictions'] = closing_price
plt.plot(train['Close'][tl-200:])
plt.plot(valid[['Close','Predictions']])
plt.show()