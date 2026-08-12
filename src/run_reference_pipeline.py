from pathlib import Path
import sys,time,pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,mean_absolute_error,r2_score
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(Path(__file__).parent))
from generate_scenarios import generate_scenarios
from models import FEATURES,decision_tree,linear_regression
from explainability import feature_importance
OUT=ROOT/"results"; OUT.mkdir(exist_ok=True)
df=generate_scenarios(); df.to_csv(ROOT/"data"/"synthetic_scenarios_reference.csv",index=False)
X=df[FEATURES]; y=df.decision_action
Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.25,random_state=42,stratify=y)
clf=decision_tree(); clf.fit(Xtr,ytr); t=time.perf_counter(); pred=clf.predict(Xte); latency=(time.perf_counter()-t)*1000
summary={"decision_tree_accuracy":accuracy_score(yte,pred),"batch_latency_ms":latency}
Xtr2,Xte2,ytr2,yte2=train_test_split(X,df.stopping_distance_m,test_size=.25,random_state=42)
reg=linear_regression(); reg.fit(Xtr2,ytr2); p2=reg.predict(Xte2); summary.update({"linear_regression_MAE_m":mean_absolute_error(yte2,p2),"linear_regression_R2":r2_score(yte2,p2)})
pd.DataFrame([summary]).to_csv(OUT/"reference_pipeline_summary.csv",index=False)
feature_importance(clf).rename("importance").to_csv(OUT/"decision_tree_feature_importance.csv")
print(pd.DataFrame([summary]).to_string(index=False));
