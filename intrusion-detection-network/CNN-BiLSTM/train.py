import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import keras

from sklearn.model_selection import StratifiedKFold
from keras import layers, Sequential, Input

####################################################### DATA LOAD #

data = pd.read_csv(r"data\cnn1d_bilstm.csv")
x = data.drop(columns=["class"])
y = data["class"]

################################################ NET ARCHITECTURE #

keras.utils.set_random_seed(123)
net = Sequential(
    [
        Input(shape=(len(x.columns), 1)),
        # Feature Extraction CNN-1D
        layers.Conv1D(filters=64, kernel_size=122, padding="same", activation="relu"),
        layers.MaxPool1D(pool_size=5),
        layers.BatchNormalization(),
        # Bidirectional LSTM
        layers.Bidirectional(layers.LSTM(units=64, return_sequences=False)),
        layers.Reshape((128, 1)),
        layers.MaxPool1D(pool_size=5),
        layers.BatchNormalization(),
        layers.Bidirectional(layers.LSTM(units=128, return_sequences=False)),
        # Output
        layers.Dropout(rate=0.5),
        layers.Dense(units=5),
        layers.Activation("softmax"),
    ]
)

net.compile(
    loss=keras.losses.CategoricalCrossentropy(from_logits=False),
    optimizer="adam",
    metrics=["accuracy"],
)

net.summary()

############################### TRAINING ON CROSS VALIDATION MOOD #

kfold = StratifiedKFold(n_splits=5, shuffle=True, random_state=123)
kfold.get_n_splits(x, y)

folds = []
for train_index, test_index in kfold.split(x, y):
    xtrain, xdev = x.iloc[train_index], x.iloc[test_index]
    ytrain, ydev = y.iloc[train_index], y.iloc[test_index]

    # Prepare training data
    xtrain = xtrain.values
    xtrain = np.reshape(xtrain, (xtrain.shape[0], xtrain.shape[1], 1))

    dummies = pd.get_dummies(ytrain)
    ytrain = dummies.values
    num_classes = len(dummies.columns)

    # Prepare testing data
    xdev = xdev.values
    xdev = np.reshape(xdev, (xdev.shape[0], xdev.shape[1], 1))

    dummies_test = pd.get_dummies(ydev)
    ydev = dummies_test.values

    net.fit(
        xtrain,
        ytrain,
        validation_data=(xdev, ydev),
        epochs=10,
    )

    # Evaluate the net
    pred = net.predict(xdev)
    pred = np.argmax(pred, axis=1)
    yeval = np.argmax(ydev, axis=1)
    score = keras.metrics.Accuracy(yeval, pred)
    folds.append(score)
    print(f"Validation score: {score}")

average_score = np.mean(folds)
print("Average Validation Score: {average_score}")
