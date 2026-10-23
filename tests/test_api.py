VALID={"age":52,"systolic":138,"diastolic":86,"glucose":126.5,"bmi":29.4}

def test_health(client):
    r=client.get('/health'); assert r.status_code==200; assert r.json()['status']=='ok'

def test_successful_prediction(client):
    r=client.post('/predict',json=VALID); assert r.status_code==200; b=r.json(); assert b['predicted_class'] in [0,1]; assert 0<=b['probability_class_1']<=1

def test_success_is_logged(client):
    client.post('/predict',json=VALID); logs=client.get('/audit?limit=10').json(); assert logs[0]['status']=='success'

def test_invalid_type_logged(client):
    r=client.post('/predict',json={**VALID,'age':'bad'}); assert r.status_code==400; assert client.get('/audit').json()[0]['status']=='failed'

def test_out_of_range_logged(client):
    r=client.post('/predict',json={**VALID,'systolic':500}); assert r.status_code==400; assert client.get('/audit').json()[0]['status']=='failed'

def test_missing_field_logged(client):
    bad=VALID.copy(); bad.pop('glucose'); r=client.post('/predict',json=bad); assert r.status_code==400; assert client.get('/audit').json()[0]['status']=='failed'

def test_audit_limit(client):
    client.post('/predict',json=VALID); client.post('/predict',json=VALID); r=client.get('/audit?limit=1'); assert len(r.json())==1
