from sklearn.metrics import classification_report

def evaluate_model(trainer, test_dataset):
    preds = trainer.predict(test_dataset)
    preds = preds.predictions.argmax(-1)
    true_labels = test_dataset["labels"]
    print(classification_report(true_labels, preds))
