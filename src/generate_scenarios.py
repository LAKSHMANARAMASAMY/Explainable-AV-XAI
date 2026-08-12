import numpy as np
import pandas as pd

CATEGORIES=["Sudden Obstacle","Ethical Decision-Making","Complex Traffic","Adverse Weather","Mechanical Failure"]

def generate_scenarios(seed=42, per_category=90):
    rng=np.random.default_rng(seed); rows=[]
    for cat in CATEGORIES:
        for _ in range(per_category):
            speed=rng.uniform(20,120); obstacle=rng.uniform(5,50); braking=rng.uniform(50,100)
            traffic=rng.choice(["Low","Medium","High"],p=[.25,.45,.30])
            visibility=rng.choice(["Clear","Rain","Fog"],p=[.60,.22,.18])
            surface=rng.choice(["Dry","Wet","Slippery"],p=[.62,.25,.13])
            sensor=rng.choice(["Normal","Degraded","Failed"],p=[.72,.22,.06])
            comm=rng.choice(["Connected","Delayed","Disrupted"],p=[.75,.18,.07])
            ped=rng.choice(["None","Low","High"],p=[.40,.35,.25])
            weather=rng.choice(["Mild","Moderate","Severe"],p=[.60,.28,.12])
            steering=rng.choice(["Normal","Reduced","Faulty"],p=[.75,.20,.05])
            urgency=rng.choice(["Low","Medium","High"],p=[.30,.42,.28])
            if cat=="Sudden Obstacle": obstacle=rng.uniform(5,25); urgency="High"
            if cat=="Complex Traffic": traffic=rng.choice(["Medium","High"],p=[.25,.75])
            if cat=="Adverse Weather": visibility=rng.choice(["Rain","Fog"]); surface=rng.choice(["Wet","Slippery"]); weather="Severe"
            if cat=="Mechanical Failure": braking=rng.uniform(50,82); sensor=rng.choice(["Degraded","Failed"]); steering=rng.choice(["Reduced","Faulty"])
            risk=(2 if obstacle<12 else 1 if obstacle<22 else 0)+(2 if speed>90 else 1 if speed>65 else 0)
            risk+={"Low":0,"Medium":1,"High":2}[traffic]+{"Clear":0,"Rain":1,"Fog":2}[visibility]
            risk+={"Dry":0,"Wet":1,"Slippery":2}[surface]+{"Normal":0,"Degraded":1,"Failed":3}[sensor]
            risk+={"Connected":0,"Delayed":1,"Disrupted":2}[comm]+{"None":0,"Low":1,"High":2}[ped]
            risk+={"Mild":0,"Moderate":1,"Severe":2}[weather]+{"Normal":0,"Reduced":1,"Faulty":3}[steering]
            risk+={"Low":0,"Medium":1,"High":2}[urgency]+(2 if braking<65 else 1 if braking<78 else 0)
            action="Brake" if risk>=12 else "Avoid/Lane Change" if risk>=8 else "Continue"
            road={"Dry":1.0,"Wet":1.25,"Slippery":1.55}[surface]
            stop=(speed/3.6)**2/(2*7.5)*road*(100/max(braking,1))+rng.normal(0,1.5)
            rows.append([cat,speed,obstacle,traffic,visibility,surface,braking,sensor,comm,ped,weather,steering,urgency,action,max(stop,.5)])
    cols=["scenario_category","vehicle_speed_kmh","obstacle_distance_m","traffic_density","visibility_condition","road_surface_condition","braking_efficiency_pct","sensor_reliability","communication_status","pedestrian_presence","weather_severity","steering_response","decision_urgency","decision_action","stopping_distance_m"]
    return pd.DataFrame(rows,columns=cols)

if __name__=="__main__":
    generate_scenarios().to_csv("data/synthetic_scenarios_reference.csv",index=False)
