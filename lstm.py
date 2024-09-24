import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import matplotlib.pyplot as plt

# Load and preprocess the data
def load_and_preprocess_data(file_path):
    df = pd.read_csv(file_path, parse_dates=['timestamp'])
    df.set_index('timestamp', inplace=True)
    # Remove the 'SUM' column
    df = df.drop('SUM', axis=1)
    return df

# Create sequences for LSTM input
def create_sequences(data, sequence_length):
    X, y = [], []
    for i in range(len(data) - sequence_length):
        X.append(data[i:(i + sequence_length)])
        y.append(data[i + sequence_length])
    return np.array(X), np.array(y)

# Build the LSTM model
def build_model(input_shape, output_shape):
    model = Sequential([
        LSTM(50, activation='relu', input_shape=input_shape, return_sequences=True),
        LSTM(50, activation='relu'),
        Dense(output_shape)  # output units for 31 residents (excluding SUM)
    ])
    model.compile(optimizer='adam', loss='mse')
    return model

# Main function
def main():
    # Load and preprocess the data
    df = load_and_preprocess_data('data/customer_power_data.csv')
    
    # Prepare the data for LSTM
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(df)
    
    # Create sequences
    sequence_length = 24  # Use 24 hours of data to predict the next hour
    X, y = create_sequences(scaled_data, sequence_length)
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Build and train the model
    model = build_model((X_train.shape[1], X_train.shape[2]), df.shape[1])
    history = model.fit(X_train, y_train, epochs=50, batch_size=32, validation_split=0.2, verbose=1)
    
    # Evaluate the model
    loss = model.evaluate(X_test, y_test, verbose=0)
    print(f'Test loss: {loss}')
    
    # Make predictions
    predictions = model.predict(X_test)
    
    # Inverse transform the predictions and actual values
    predictions = scaler.inverse_transform(predictions)
    y_test = scaler.inverse_transform(y_test)
    
    # Plot the results for the first resident
    plt.figure(figsize=(12, 6))
    plt.plot(y_test[:, 0], label='Actual')
    plt.plot(predictions[:, 0], label='Predicted')
    plt.legend()
    plt.title('Actual vs Predicted Power Usage for Resident 1')
    plt.show()

    # Calculate and print the sum of predictions for all residents
    sum_predictions = np.sum(predictions, axis=1)
    sum_actual = np.sum(y_test, axis=1)
    
    plt.figure(figsize=(12, 6))
    plt.plot(sum_actual, label='Actual Sum')
    plt.plot(sum_predictions, label='Predicted Sum')
    plt.legend()
    plt.title('Actual vs Predicted Sum of Power Usage for All Residents')
    plt.show()

if __name__ == '__main__':
    main()
