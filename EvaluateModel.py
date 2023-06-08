import numpy as np
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score

def evaluate_predictions(true_labels, pred_labels):
    # Compute the confusion matrix
    cm = confusion_matrix(true_labels, pred_labels)

    # Compute the TP, TN, FP, and FN values
    tp = np.diag(cm)
    tn = np.diag(cm)[::-1]
    fp = np.sum(cm, axis=0) - tp
    fn = np.sum(cm, axis=1) - tp

    # Compute the evaluation metrics as percentages
    accuracy = accuracy_score(true_labels, pred_labels) * 100
    precision = precision_score(true_labels, pred_labels, average='weighted', zero_division=0) * 100
    recall = recall_score(true_labels, pred_labels, average='weighted') * 100
    f1 = f1_score(true_labels, pred_labels, average='weighted') * 100
    
    # Format the scores into percentages and round them off to 2 decimal places
    accuracy_str = '{:.2f}%'.format(accuracy)
    precision_str = '{:.2f}%'.format(precision)
    recall_str = '{:.2f}%'.format(recall)
    f1_str = '{:.2f}%'.format(f1)

    # Return the confusion matrix and evaluation metrics as percentages
    return cm, tp, tn, fp, fn, accuracy_str, precision_str, recall_str, f1_str

