import os
from flask import Blueprint, request, jsonify, session
from .models import db, HealthMetric, User
from functools import wraps
from openai import OpenAI

health_metric = Blueprint('health_metric', __name__)

def get_openai_client():
    api_key = os.getenv("NEBIUS_API_KEY")
    if not api_key:
        return None
    base_url = os.getenv("NEBIUS_BASE_URL", "https://api.tokenfactory.nebius.com/v1/")
    return OpenAI(
        base_url=base_url,
        api_key=api_key,
    )

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({"error": "Login required"}), 401
        user = db.session.get(User, session['user_id'])
        if not user:
            session.pop('user_id', None)
            return jsonify({"error": "Session invalid"}), 401
        return f(*args, **kwargs)
    return decorated_function

def parse_int(val):
    if val is None or val == "":
        return None
    try:
        return int(val)
    except (ValueError, TypeError):
        return None

@health_metric.route('/api/health-metrics', methods=['POST'])
@login_required
def add_health_metric():
    try:
        data = request.get_json(silent=True) or request.form or {}
        user_id = session['user_id']
        
        heart_rate = parse_int(data.get('heart_rate'))
        blood_pressure_systolic = parse_int(data.get('blood_pressure_systolic'))
        blood_pressure_diastolic = parse_int(data.get('blood_pressure_diastolic'))
        calorie_count = parse_int(data.get('calorie_count'))

        if heart_rate is None and blood_pressure_systolic is None and blood_pressure_diastolic is None and calorie_count is None:
            return jsonify({"error": "At least one health metric must be provided"}), 400

        new_metric = HealthMetric(
            user_id=user_id,
            heart_rate=heart_rate,
            blood_pressure_systolic=blood_pressure_systolic,
            blood_pressure_diastolic=blood_pressure_diastolic,
            calorie_count=calorie_count
        )
        
        db.session.add(new_metric)
        db.session.commit()
        
        return jsonify({
            "message": "Health metric added successfully",
            "metric_id": new_metric.id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@health_metric.route('/api/health-metrics', methods=['GET'])
@login_required
def get_health_metrics():
    try:
        user_id = session['user_id']
        metrics = HealthMetric.query.filter_by(user_id=user_id).order_by(HealthMetric.timestamp.desc()).all()
        
        return jsonify({
            "metrics": [{
                "id": metric.id,
                "heart_rate": metric.heart_rate,
                "blood_pressure_systolic": metric.blood_pressure_systolic,
                "blood_pressure_diastolic": metric.blood_pressure_diastolic,
                "calorie_count": metric.calorie_count,
                "timestamp": metric.timestamp.isoformat() if metric.timestamp else None
            } for metric in metrics]
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@health_metric.route('/api/health-tips', methods=['GET'])
@login_required
def get_health_tips():
    try:
        user_id = session['user_id']
        latest_metric = HealthMetric.query.filter_by(user_id=user_id).order_by(HealthMetric.timestamp.desc()).first()
        
        if not latest_metric:
            return jsonify({"message": "No health metrics found"}), 404
            
        client = get_openai_client()
        if not client:
            return jsonify({
                "health_tips": "AI Health Assistant Notice: NEBIUS_API_KEY environment variable is not configured. Please configure your API key to enable AI health tips.",
                "metrics": {
                    "heart_rate": latest_metric.heart_rate if latest_metric.heart_rate is not None else "N/A",
                    "blood_pressure": f"{latest_metric.blood_pressure_systolic or 'N/A'}/{latest_metric.blood_pressure_diastolic or 'N/A'}",
                    "calorie_count": latest_metric.calorie_count if latest_metric.calorie_count is not None else "N/A"
                }
            }), 200

        prompt = f"""
        Based on the following health metrics:
        Heart Rate: {latest_metric.heart_rate or 'N/A'} BPM
        Blood Pressure: {latest_metric.blood_pressure_systolic or 'N/A'}/{latest_metric.blood_pressure_diastolic or 'N/A'} mmHg
        Calorie Count: {latest_metric.calorie_count or 'N/A'} kcal

        Provide personalized health tips and recommendations for improving wellness.
        """

        completion = client.chat.completions.create(
            model="meta-llama/Llama-3.3-70B-Instruct",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )

        health_tips = completion.choices[0].message.content
        
        return jsonify({
            "health_tips": health_tips,
            "metrics": {
                "heart_rate": latest_metric.heart_rate if latest_metric.heart_rate is not None else "N/A",
                "blood_pressure": f"{latest_metric.blood_pressure_systolic or 'N/A'}/{latest_metric.blood_pressure_diastolic or 'N/A'}",
                "calorie_count": latest_metric.calorie_count if latest_metric.calorie_count is not None else "N/A"
            }
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@health_metric.route('/api/health-metrics/<int:metric_id>', methods=['DELETE'])
@login_required
def delete_health_metric(metric_id):
    try:
        user_id = session['user_id']
        metric = HealthMetric.query.filter_by(id=metric_id, user_id=user_id).first()
        
        if not metric:
            return jsonify({"error": "Health metric not found"}), 404
        
        db.session.delete(metric)
        db.session.commit()
        
        return jsonify({"message": "Health metric deleted successfully"}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@health_metric.route('/api/health-metrics/<int:metric_id>', methods=['PUT'])
@login_required
def update_health_metric(metric_id):
    try:
        user_id = session['user_id']
        metric = HealthMetric.query.filter_by(id=metric_id, user_id=user_id).first()
        
        if not metric:
            return jsonify({"error": "Health metric not found"}), 404
        
        data = request.get_json(silent=True) or request.form or {}
        if 'heart_rate' in data:
            metric.heart_rate = parse_int(data['heart_rate'])
        if 'blood_pressure_systolic' in data:
            metric.blood_pressure_systolic = parse_int(data['blood_pressure_systolic'])
        if 'blood_pressure_diastolic' in data:
            metric.blood_pressure_diastolic = parse_int(data['blood_pressure_diastolic'])
        if 'calorie_count' in data:
            metric.calorie_count = parse_int(data['calorie_count'])
        
        db.session.commit()
        
        return jsonify({"message": "Health metric updated successfully"}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@health_metric.route('/api/health-metrics/<int:metric_id>', methods=['GET'])
@login_required
def get_health_metric(metric_id):
    try:
        user_id = session['user_id']
        metric = HealthMetric.query.filter_by(id=metric_id, user_id=user_id).first()
        
        if not metric:
            return jsonify({"error": "Health metric not found"}), 404
        
        return jsonify({
            "id": metric.id,
            "heart_rate": metric.heart_rate,
            "blood_pressure_systolic": metric.blood_pressure_systolic,
            "blood_pressure_diastolic": metric.blood_pressure_diastolic,
            "calorie_count": metric.calorie_count,
            "timestamp": metric.timestamp.isoformat() if metric.timestamp else None
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@health_metric.route('/api/health-metrics/summary', methods=['GET'])
@login_required
def get_health_metrics_summary():
    try:
        user_id = session['user_id']
        metrics = HealthMetric.query.filter_by(user_id=user_id).all()
        
        if not metrics:
            return jsonify({"message": "No health metrics found"}), 404
        
        heart_rates = [m.heart_rate for m in metrics if m.heart_rate is not None]
        bp_systolics = [m.blood_pressure_systolic for m in metrics if m.blood_pressure_systolic is not None]
        bp_diastolics = [m.blood_pressure_diastolic for m in metrics if m.blood_pressure_diastolic is not None]
        calories = [m.calorie_count for m in metrics if m.calorie_count is not None]

        heart_rate_avg = round(sum(heart_rates) / len(heart_rates), 1) if heart_rates else 0
        bp_systolic_avg = round(sum(bp_systolics) / len(bp_systolics), 1) if bp_systolics else 0
        bp_diastolic_avg = round(sum(bp_diastolics) / len(bp_diastolics), 1) if bp_diastolics else 0
        calorie_count_avg = round(sum(calories) / len(calories), 1) if calories else 0
        
        return jsonify({
            "heart_rate_avg": heart_rate_avg,
            "blood_pressure_systolic_avg": bp_systolic_avg,
            "blood_pressure_diastolic_avg": bp_diastolic_avg,
            "calorie_count_avg": calorie_count_avg
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@health_metric.route('/api/health-metrics/summary', methods=['DELETE'])
@login_required
def delete_health_metrics():
    try:
        user_id = session['user_id']
        metrics = HealthMetric.query.filter_by(user_id=user_id).all()
        
        if not metrics:
            return jsonify({"message": "No health metrics found"}), 404
        
        for metric in metrics:
            db.session.delete(metric)
        
        db.session.commit()
        
        return jsonify({"message": "All health metrics deleted successfully"}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500