import pytest
from app import create_app
from src.models import db, User, HealthMetric

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SECRET_KEY": "test_secret_key",
        "WTF_CSRF_ENABLED": False,
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Your Personal" in response.data
    assert b"AI Health Companion" in response.data


def test_user_registration_success(client):
    response = client.post('/register', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123'
    }, follow_redirects=False)

    assert response.status_code == 302
    assert '/login' in response.headers['Location']

    with client.application.app_context():
        user = User.query.filter_by(username='testuser').first()
        assert user is not None
        assert user.email == 'test@example.com'

def test_user_registration_duplicate_username(client):
    client.post('/register', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123'
    })

    response = client.post('/register', data={
        'username': 'testuser',
        'email': 'other@example.com',
        'password': 'password123'
    })

    assert response.status_code == 400
    assert b"Username already taken" in response.data

def test_user_login_success(client):
    client.post('/register', data={
        'username': 'loginuser',
        'email': 'login@example.com',
        'password': 'password123'
    })

    response = client.post('/login', data={
        'username': 'loginuser',
        'password': 'password123'
    }, follow_redirects=False)

    assert response.status_code == 302
    assert '/' in response.headers['Location']

def test_user_login_invalid_password(client):
    client.post('/register', data={
        'username': 'loginuser',
        'email': 'login@example.com',
        'password': 'password123'
    })

    response = client.post('/login', data={
        'username': 'loginuser',
        'password': 'wrongpassword'
    })

    assert response.status_code == 400
    assert b"Invalid username or password" in response.data

def test_health_metrics_crud_and_null_averages(client):
    # Register and login
    client.post('/register', data={
        'username': 'metricuser',
        'email': 'metric@example.com',
        'password': 'password123'
    })
    client.post('/login', data={'username': 'metricuser', 'password': 'password123'})

    # 1. Add complete metric
    resp = client.post('/api/health-metrics', json={
        'heart_rate': 75,
        'blood_pressure_systolic': 120,
        'blood_pressure_diastolic': 80,
        'calorie_count': 2000
    })
    assert resp.status_code == 201
    metric_id_1 = resp.json['metric_id']

    # 2. Add partial metric with None/missing fields
    resp = client.post('/api/health-metrics', json={
        'heart_rate': 85,
        'calorie_count': 1800
        # blood pressure fields omitted/None
    })
    assert resp.status_code == 201

    # 3. Fetch summary (verify NO TypeError when averaging metrics with missing/null values)
    summary_resp = client.get('/api/health-metrics/summary')
    assert summary_resp.status_code == 200
    data = summary_resp.json
    assert data['heart_rate_avg'] == 80.0  # (75 + 85) / 2
    assert data['blood_pressure_systolic_avg'] == 120.0  # single metric
    assert data['calorie_count_avg'] == 1900.0  # (2000 + 1800) / 2

    # 4. Fetch metrics list
    list_resp = client.get('/api/health-metrics')
    assert list_resp.status_code == 200
    assert len(list_resp.json['metrics']) == 2

    # 5. Delete metric
    del_resp = client.delete(f'/api/health-metrics/{metric_id_1}')
    assert del_resp.status_code == 200

    # 6. Delete all summary
    del_all_resp = client.delete('/api/health-metrics/summary')
    assert del_all_resp.status_code == 200

def test_profile_page_with_null_metrics(client):
    client.post('/register', data={
        'username': 'profileuser',
        'email': 'profile@example.com',
        'password': 'password123'
    })
    client.post('/login', data={'username': 'profileuser', 'password': 'password123'})

    # Insert metric with None values directly into DB
    with client.application.app_context():
        user = User.query.filter_by(username='profileuser').first()
        m = HealthMetric(user_id=user.id, heart_rate=80, blood_pressure_systolic=None, blood_pressure_diastolic=None, calorie_count=2100)
        db.session.add(m)
        db.session.commit()

    response = client.get('/profile')
    assert response.status_code == 200
    assert b"profileuser" in response.data
    # Verify JS rendering does NOT output "None" syntax error
    assert b'"blood_pressure_systolic": null' in response.data

def test_process_image_no_input(client):
    client.post('/register', data={
        'username': 'visionuser',
        'email': 'vision@example.com',
        'password': 'password123'
    })
    client.post('/login', data={'username': 'visionuser', 'password': 'password123'})

    response = client.post('/process', data={})
    assert response.status_code == 400
    assert response.json['error'] == "No valid image provided"

def test_settings_page(client):
    client.post('/register', data={
        'username': 'settingsuser',
        'email': 'settings@example.com',
        'password': 'password123'
    })
    client.post('/login', data={'username': 'settingsuser', 'password': 'password123'})

    response = client.get('/settings')
    assert response.status_code == 200
    assert b"Account &amp; App Settings" in response.data or b"Account & App Settings" in response.data
    assert b"settingsuser" in response.data

