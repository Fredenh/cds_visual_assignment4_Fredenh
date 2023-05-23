# Importing necessary tools and packages
import os
import numpy as np
import cv2
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier

def main():
    # Defining the folder names corresponding to each class
    folder_names = ["badminton", "padel", "squash", "table_tennis", "tennis"]

    # Initializing the data and labels by creating empty lists with each
    X_dataset = []
    y_labels = []

    # Loading and preprocessing the images
    for label, folder in enumerate(folder_names):
        # Full path to folder with labels
        folder_path = os.path.join(".", "in", folder)
        # Iterating through every file 
        for filename in os.listdir(folder_path):
            # Path to image files
            image_path = os.path.join(folder_path, filename)
            # Loading image with OpenCV's cv2.IMREAD_GRAYSCALE
            image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            # Resizing images to a desired size. More to the point of consistent image sizes since they all are of different origin on Pexels
            resized_image = cv2.resize(image, (255, 255))
            # Appending the preprocessed images and identified labels to the empty lists from before
            X_dataset.append(resized_image)
            y_labels.append(label)

    # Converting the data to numpy arrays
    X_dataset = np.array(X_dataset)
    y_labels = np.array(y_labels)

    # Reshaping the input data
    nsamples, nx, ny = X_dataset.shape
    X_dataset = X_dataset.reshape((nsamples, nx * ny))

    # Scaling the input data
    X_scaled = X_dataset / 255.0

    # Splitting the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_labels, test_size=0.2, random_state=42)

    # Training the logistic regression classifier
    clf = LogisticRegression(penalty="none", # No regularization penalty 
                             tol=0.1,        # Model stops if the loss function is less than 0.1 between iterations
                             solver="saga",  # Chosen optimization algorithm
                             multi_class="multinomial").fit(X_train, y_train) # Multi-class task

    # Making predictions based on the testing set
    y_pred = clf.predict(X_test)

    # Generating a classification report
    report = classification_report(y_test,
                                   y_pred,
                                   target_names=folder_names) # Using the previously defined labels

    # Saving the classification report
    folder_path = os.path.join(".", "out")
    file_name = "logistic_reg_classifier.txt"
    file_path = os.path.join(folder_path, file_name)

# "Writing" the classification report
    with open(file_path, "w") as f:
        f.write(report)
    print("Report saved") 

if __name__ == "__main__":
    main()