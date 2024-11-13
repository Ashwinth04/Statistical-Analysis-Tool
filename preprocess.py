import pandas as pd
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, accuracy_score, classification_report
import sys
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score



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

def run_svm(filename, target, gamma=1.0, C=1.0):
    """
    Train and evaluate an SVM model with given parameters.
    
    Parameters:
    filename (str): Path to the CSV file
    target (str): Name of the target variable
    gamma (float): Kernel coefficient for 'rbf' kernel
    C (float): Regularization parameter
    """
    # Load and prepare the dataset
    filename = filename[1:-1]
    target = target[1:-1]
    data = pd.read_csv(filename)
    
    # Separate features and target variable
    X = data.drop(columns=[target])
    y = data[target]
    
    # Split the dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Create and train the SVM model
    svm_model = SVC(gamma=gamma, C=C, kernel='rbf')
    svm_model.fit(X_train, y_train)
    
    # Make predictions
    y_pred = svm_model.predict(X_test)
    
    # Calculate and print metrics
    accuracy = accuracy_score(y_test, y_pred)
    print("\nSVM Model Performance:")
    print(f"Accuracy: {accuracy:.4f}")


def run_knn(filename, target, n_neighbors=5):
    """
    Train and evaluate a KNN model.
    
    Parameters:
    filename (str): Path to the CSV file
    target (str): Name of the target variable
    n_neighbors (int): Number of neighbors to use
    """
    # Load and prepare the dataset
    filename = filename[1:-1]
    target = target[1:-1]
    data = pd.read_csv(filename)
    
    # Separate features and target variable
    X = data.drop(columns=[target])
    y = data[target]
    
    # Split the dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Create and train the KNN model
    knn_model = KNeighborsClassifier(n_neighbors=n_neighbors)
    knn_model.fit(X_train, y_train)
    
    # Make predictions
    y_pred = knn_model.predict(X_test)
    
    # Calculate and print metrics
    accuracy = accuracy_score(y_test, y_pred)
    print("\nKNN Model Performance:")
    print(f"Accuracy: {accuracy:.4f}")
    print("\nDetailed Classification Report:")
    print(classification_report(y_test, y_pred))
    
    # Optional: Find optimal k value
    def optimize_k():
        k_range = range(1, 31)
        k_scores = []
        
        for k in k_range:
            knn = KNeighborsClassifier(n_neighbors=k)
            scores = cross_val_score(knn, X_train, y_train, cv=5, scoring='accuracy')
            k_scores.append(scores.mean())
        
        # Plot k values vs accuracy
        plt.figure(figsize=(10, 6))
        plt.plot(k_range, k_scores)
        plt.xlabel('Value of K')
        plt.ylabel('Cross-validated Accuracy')
        plt.title('Accuracy vs. K Value')
        plt.savefig('knn_optimization.png')
        plt.close()
        
        # Get optimal k
        optimal_k = k_range[k_scores.index(max(k_scores))]
        print(f"\nOptimal k value: {optimal_k}")
        print(f"Best accuracy: {max(k_scores):.4f}")
        
        return optimal_k

    def analyze_feature_importance():
        """
        Analyze feature importance using permutation importance
        """
        from sklearn.inspection import permutation_importance
        
        result = permutation_importance(knn_model, X_test, y_test, n_repeats=10, random_state=42)
        feature_importance = pd.DataFrame({
            'feature': X.columns,
            'importance': result.importances_mean
        }).sort_values('importance', ascending=False)
        
        print("\nFeature Importance:")
        print(feature_importance)
        
        # Plot feature importance
        plt.figure(figsize=(10, 6))
        plt.bar(feature_importance['feature'], feature_importance['importance'])
        plt.xticks(rotation=45)
        plt.title('Feature Importance in KNN Model')
        plt.tight_layout()
        plt.savefig('knn_feature_importance.png')
        plt.close()
    
    # Run feature importance analysis
    optimize_k()
    analyze_feature_importance()
    
    return knn_model