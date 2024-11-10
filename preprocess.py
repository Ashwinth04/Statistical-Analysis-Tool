import pandas as pd
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

def preprocess_data(filename, target):
    # Load the dataset
    data = pd.read_csv(filename)
    
    # Convert categorical variables to integers (excluding the target column)
    label_encoders = {}
    for column in data.select_dtypes(include=['object']).columns:
        le = LabelEncoder()
        data[column] = le.fit_transform(data[column])
        print("HI")
        label_encoders[column] = le
    
    # Normalize the data except the target column

    scaler = MinMaxScaler()
    columns_to_scale = [col for col in data.columns if col != target]

    
    # Normalize only the numerical columns
    data[columns_to_scale] = scaler.fit_transform(data[columns_to_scale])
    
    # Save or return the processed data
    data.to_csv('processed_' + filename, index=False)
    print(f"Processed data saved to 'processed_{filename}'")


def linear_regression(filename, target):
    # Load the dataset
    filename = filename[1:-1]
    target = target[1:-1]
    data = pd.read_csv(filename)
    
    # Separate features and target variable
    X = data.drop(columns=[target])
    y = data[target]
    
    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Create a Linear Regression model
    model = LinearRegression()
    
    # Train the model
    model.fit(X_train, y_train)
    
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Evaluate the model
    mse = mean_squared_error(y_test, y_pred)
    
    print(f"Model trained. Mean Squared Error: {mse}")
    
    # Return the coefficients (optional)
    return model.coef_, model.intercept_

