import keras
from keras.models import Sequential
from keras.models import load_model
from keras.layers import Dense
from keras.optimizers import Adam
import math
import numpy as np
import random
from collections import deque
import sys
import time

class Agent:
    def __init__(self, state_size, is_eval=False, model_name=""):
        self.state_size = state_size # normalized previous days
        self.action_size = 3 # sit, buy, sell
        self.memory = deque(maxlen=1000)
        self.inventory = []
        self.model_name = model_name
        self.is_eval = is_eval
        self.gamma = 0.95
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.model = load_model(model_name) if is_eval else self._model()
    def _model(self):
        model = Sequential()
        model.add(Dense(units=64, input_dim=self.state_size, activation="relu"))
        model.add(Dense(units=32, activation="relu"))
        model.add(Dense(units=8, activation="relu"))
        model.add(Dense(self.action_size, activation="linear"))
        model.compile(loss="mse", optimizer=Adam(lr=0.001))
        return model
    def act(self, state):
        if not self.is_eval and random.random()<= self.epsilon:
            return random.randrange(self.action_size)
        options = self.model.predict(state)
        return np.argmax(options[0])
    def expReplay(self, batch_size):
        mini_batch = []
        l = len(self.memory)
        for i in range(l - batch_size + 1, l):
            mini_batch.append(self.memory[i])
        for state, action, reward, next_state, done in mini_batch:
            target = reward
            if not done:
                target = reward + self.gamma * np.amax(self.model.predict(next_state)[0])
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

def formatPrice(n):
    return("-USDT. " if n<0 else "USDT. ")+"{0:.2f}".format(abs(n))
def getStockDataVec(key):
    vec = []
    lines = open(key+".csv","r").read().splitlines()
    for line in lines[7000:]:
        x=line.split(",")[1]
        if x=="null":
          x=0
        # print(float(line.split(",")[4]))
        vec.append(float(x))
        #print(vec)
    return vec 
def sigmoid(x):
    # print(x)
    if x>20:
        return 1
    if x<20:
        return 0
    return 1/(1+np.exp(-x))
def getState(data, t, n):
    d = t - n + 1
    block = data[d:t + 1] if d >= 0 else -d * [data[0]] + data[0:t + 1] # pad with t0
    res = []
    for i in range(n - 1):
        res.append(sigmoid(block[i + 1] - block[i]))
    return np.array([res])

def train(ws,ec):
    stock_name = "Stockvol"
    window_size = ws
    episode_count = ec
    stock_name = str(stock_name)
    window_size = int(window_size)
    episode_count = int(episode_count)
    agent = Agent(window_size)
    data = getStockDataVec(stock_name)
    l = len(data) - 1
    batch_size = 32
    tic = time.perf_counter()


    for e in range(episode_count + 1):
        print("--------------------------------")
        print("Episode " + str(e) + "/" + str(episode_count))
        state = getState(data, 0, window_size + 1)
        total_profit = 0
        agent.inventory = []
        for t in range(l):
            action = agent.act(state)
            # sit
            # print(action)
            next_state = getState(data, t + 1, window_size + 1)
            reward = 0
            tt = time.localtime()
            ct = time.strftime("%H:%M:%S", tt)

            if action == 1: # buy
                agent.inventory.append(data[t])
                print(str(ct)+" : Buy: " + formatPrice(data[t]))
            elif action == 2 and len(agent.inventory) > 0: # sell
                bought_price = window_size_price = agent.inventory.pop(0)
                reward = max(data[t] - bought_price, 0)
                total_profit += data[t] - bought_price
                print(str(ct)+" : Sell: " + formatPrice(data[t]) + " | Profit: " + formatPrice(data[t] - bought_price))
            done = True if t == l - 1 else False
            agent.memory.append((state, action, reward, next_state, done))
            state = next_state
            if done:
                print("--------------------------------")
                print("Total Profit: " + formatPrice(total_profit))
                print("--------------------------------")
            if len(agent.memory) > batch_size:
                agent.expReplay(batch_size)
        if e % 10 == 0:
            agent.model.save(str(e))
        toc = time.perf_counter()
        print(f"Training finished in {toc - tic:0.4f} seconds")

def test(bs,iv):
    stock_name = "Stockvol"
    model_name = "0"
    model = load_model(model_name)
    window_size = model.layers[0].input.shape.as_list()[1]
    agent = Agent(window_size, True, model_name)
    data = getStockDataVec(stock_name)
    print(data)
    l = len(data) - 1
    batch_size = bs
    state = getState(data, 0, window_size + 1)
    print(state)
    total_profit = 0
    agent.inventory = iv
    print(l)
    tic = time.perf_counter()

    for t in range(l):
        action = agent.act(state)
        # print(action)
        # sit
        next_state = getState(data, t + 1, window_size + 1)
        reward = 0
        tt = time.localtime()
        ct = time.strftime("%H:%M:%S", tt)
        if action == 1: # buy
            agent.inventory.append(data[t])
            print(str(ct)+" Buy: " + formatPrice(data[t]))
        elif action == 2 and len(agent.inventory) > 0: # sell
            bought_price = agent.inventory.pop(0)
            reward = max(data[t] - bought_price, 0)
            total_profit += data[t] - bought_price
            print(str(ct)+" Sell: " + formatPrice(data[t]) + " | Profit: " + formatPrice(data[t] - bought_price))
        done = True if t == l - 1 else False
        agent.memory.append((state, action, reward, next_state, done))
        state = next_state
        if done:
            print("--------------------------------")
            print(stock_name + " Total Profit: " + formatPrice(total_profit))
            print("--------------------------------")
            print ("Total profit is:",formatPrice(total_profit))
    toc = time.perf_counter()
    print(f"Testing finished in {toc - tic:0.4f} seconds")


train(1000,7)                #window_size and episode count

# test(16,[59000,58000])     #batch_size &inventory