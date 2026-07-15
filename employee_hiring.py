# Model Evaluation Scripts
# import tensorflow as tf
import numpy as np
from sklearn.model_selection import train_test_split
# Temporary fix - replace tensorflow with sklearn equivalent
try:
    import tensorflow as tf
except ImportError:
    tf = None
    
#Employee features
#[Employee, Interview score, communication]

x = np.array([
    [1,55,50],
    [2,60,58],
    [3,65,62],
    [4,72,70],
    [5,80,78],
    [6,88,85],
    [7,92,90],
    [8,95,94],
    [9,68,54],
    [5,82,80],
    [6,85,81],
    [7,91,88],
])

#0 - rejected, 1 - hired
y = np.array([
    0,
    0,
    0,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,

])

#Split the data set
x_train, x_test, y_train, y_test = train_test_split(
    x,
    y,
    test_size=0.2,
    random_state=42
)

#Build the neural network
model = tf.keras.Sequential([
    tf.keras.layers.Dense(8, activation='relu'),
    tf.keras.layers.Dense(4, activation='relu'),  
    tf.keras.layers.Dense(1, activation='sigmoid')
])

#Compile the model
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

#Train the model
model.fit(x_train,y_train,epochs=150)

#Evaluate the model
loss,accuracy=model.evaluate(x_test,y_test)

print("Loss:", loss)
print("Accuracy:", accuracy)

#Prediction
new_employee = np.array([
    [2,45,48]
])
prediction = model.predict(new_employee)
print("prediction:", prediction)

#Predict every employee in the dataset
predictions = model.predict(x_test)
predicted_labels = (predictions >=0.5).astype(int)

#Display the actual answers and model predictions
print("Actual labels")
print(y_test)

print("Predicted labels")
print(predicted_labels)

#Save the trained model
# model.save("employee_hiring_model.keras")
# print("Model Saved Successfully")