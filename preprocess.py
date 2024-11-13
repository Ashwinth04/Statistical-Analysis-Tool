import pandas as pd
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import sys
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import seaborn as sns


def preprocess_data(filename, target):
    # Load the dataset
    filename = filename[1:-1]
    target = target[1:-1]
    data = pd.read_csv(filename)
    
    # Convert categorical variables to integers (excluding the target column)
    label_encoders = {}
    for column in data.select_dtypes(include=['object']).columns:
        le = LabelEncoder()
        data[column] = le.fit_transform(data[column])
        label_encoders[column] = le
    
    # Normalize the data except the target column

    scaler = MinMaxScaler()
    columns_to_scale = [col for col in data.columns if col != target]

    
    # Normalize only the numerical columns
    data[columns_to_scale] = scaler.fit_transform(data[columns_to_scale])
    
    # Save or return the processed data
    data.to_csv('processed_' + filename, index=False)
    print(f"Processed data saved to 'processed_{filename}'")

def detect_outliers(filename, target_variable):
    # Load the CSV data into a DataFrame
    filename = filename[1:-1]
    target_variable = target_variable[1:-1]
    df = pd.read_csv(filename)

    # Check if the target variable exists in the DataFrame
    if target_variable not in df.columns:
        print(f"Error: Target variable '{target_variable}' not found in the dataset.")
        return

    # Separate features and target class
    features = df.drop(columns=[target_variable])

    # Identify outliers in the feature columns using IQR method
    outlier_indices = []

    for column in features.columns:
        # Get the column data for outlier detection
        column_data = features[column]
        
        # Calculate the IQR for each feature
        Q1 = column_data.quantile(0.25)
        Q3 = column_data.quantile(0.75)
        IQR = Q3 - Q1
        
        # Define the lower and upper bounds for outliers
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        # Identify the outliers for this column
        outliers = df[(column_data < lower_bound) | (column_data > upper_bound)]
        
        # Collect the indices of the outliers
        outlier_indices.extend(outliers.index)

    # Remove duplicates as some rows may have outliers in multiple columns
    outlier_indices = sorted(set(outlier_indices))

    if outlier_indices:
        # Print the outliers with their indices and respective feature values
        print(f"Outliers detected:\n")
        outliers_data = df.iloc[outlier_indices]
        print(outliers_data)
    else:
        print("No outliers detected.")



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


def reduce_dimensions(filename, method, n_components):
    # Load data from CSV
    data = pd.read_csv(filename[1:-1])
    method = method[1:-1]
    n_components = int(n_components[1:-1])
    # Separate features and target (if LDA is used)
    if method == 'LDA':
        if 'target' not in data.columns:
            raise ValueError("LDA requires a 'target' column in the data.")
        X = data.drop(columns=['target'])
        y = data['target']
    else:
        X = data
        y = None

    # Select and apply the dimensionality reduction method
    if method == 'PCA':
        model = PCA(n_components=n_components)
        transformed_data = model.fit_transform(X)
    elif method == 'LDA':
        model = LDA(n_components=n_components)
        transformed_data = model.fit_transform(X, y)
    elif method == 'TSNE':
        model = TSNE(n_components=n_components)
        transformed_data = model.fit_transform(X)
    else:
        raise ValueError("Invalid method. Choose 'PCA', 'LDA', or 'TSNE'.")

    # Convert the result to a DataFrame and save as a CSV file
    output_filename = f"reduced_{method}_{n_components}_dimensions.csv"
    transformed_df = pd.DataFrame(transformed_data, columns=[f"Dim{i+1}" for i in range(n_components)])
    if y is not None:
        transformed_df['target'] = y.values  # Add target column back for LDA results
    transformed_df.to_csv(output_filename, index=False)
    
    print(f"Dimensionality reduction complete. Output saved to {output_filename}.")

def boxplot(filename, target_variable, output_filename="boxplot.png"):
    # Load the CSV data into a DataFrame
    filename = filename[1:-1]
    target_variable = target_variable[1:-1]
    df = pd.read_csv(filename)
    
    # Check if the target variable exists in the DataFrame
    if target_variable not in df.columns:
        print(f"Error: Target variable '{target_variable}' not found in the dataset.")
        return
    
    # Exclude the target variable from the features
    features = [col for col in df.columns if col != target_variable]
    
    # Create a boxplot for the remaining features
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df[features])  # Pass the data as a DataFrame with the selected features
    
    # Add labels and title
    plt.title(f'Boxplot for Features Excluding "{target_variable}"')
    plt.xlabel('Features')
    plt.ylabel('Values')
    
    # Save the plot to a file
    plt.savefig(output_filename)
    
    # Optionally close the plot to free memory
    plt.close()

    print(f"Boxplot saved as {output_filename}")
