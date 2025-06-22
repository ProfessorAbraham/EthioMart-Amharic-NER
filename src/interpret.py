import shap
from lime.lime_text import LimeTextExplainer

def explain_with_lime(model, tokenizer, text):
    explainer = LimeTextExplainer(class_names=["O", "B-LOC", "I-LOC", "B-PRICE", "I-PRICE", "B-Product", "I-Product"])
    exp = explainer.explain_instance(text, lambda x: model.predict(x).logits, num_features=6)
    exp.show_in_notebook()

def explain_with_shap(model, inputs):
    explainer = shap.Explainer(model)
    shap_values = explainer(inputs)
    shap.plots.bar(shap_values[0])
