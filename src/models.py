from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LinearRegression
FEATURES=["vehicle_speed_kmh","obstacle_distance_m","traffic_density","visibility_condition","road_surface_condition","braking_efficiency_pct","sensor_reliability","communication_status","pedestrian_presence","weather_severity","steering_response","decision_urgency"]
NUM=["vehicle_speed_kmh","obstacle_distance_m","braking_efficiency_pct"]
CAT=[c for c in FEATURES if c not in NUM]
def prep(scale=False):
    return ColumnTransformer([("num",StandardScaler() if scale else "passthrough",NUM),("cat",OneHotEncoder(handle_unknown="ignore",sparse_output=False),CAT)])
def decision_tree(seed=42): return Pipeline([("prep",prep(False)),("model",DecisionTreeClassifier(max_depth=6,min_samples_leaf=5,class_weight="balanced",random_state=seed))])
def linear_regression(): return Pipeline([("prep",prep(True)),("model",LinearRegression())])
