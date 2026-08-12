import pandas as pd
def feature_importance(pipe):
    names=pipe.named_steps["prep"].get_feature_names_out(); vals=pipe.named_steps["model"].feature_importances_
    return pd.Series(vals,index=names).sort_values(ascending=False)
def shap_values(pipe,X,max_rows=50):
    import shap
    Xt=pipe.named_steps["prep"].transform(X.iloc[:max_rows]); model=pipe.named_steps["model"]
    return pipe.named_steps["prep"].get_feature_names_out(), shap.TreeExplainer(model).shap_values(Xt)
def lime_explanation(pipe,X_train,row,num_features=8):
    from lime.lime_tabular import LimeTabularExplainer
    prep=pipe.named_steps["prep"]; model=pipe.named_steps["model"]; Xt=prep.transform(X_train); xr=prep.transform(row.to_frame().T)[0]
    ex=LimeTabularExplainer(Xt,feature_names=list(prep.get_feature_names_out()),class_names=list(model.classes_),mode="classification",random_state=42)
    return ex.explain_instance(xr,model.predict_proba,num_features=num_features)
