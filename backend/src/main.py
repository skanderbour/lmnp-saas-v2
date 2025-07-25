import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS
from src.models.user import db
from src.routes.user import user_bp
from src.routes.lmnp_routes import lmnp_bp
from src.routes.agents_routes import agents_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'lmnp-expert-2024-secure-key-#FGSgvasgf$5$WGT'

# Configuration CORS pour permettre les requêtes depuis le frontend
CORS(app, origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:3000"])

# Enregistrement des blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(lmnp_bp, url_prefix='/api')
app.register_blueprint(agents_bp, url_prefix='/api')

# Configuration base de données
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Route de santé pour vérifier que l'API fonctionne
@app.route('/api/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'LMNP Expert Backend',
        'version': '2.0.0',
        'agents_ia': 'operational'
    })

# Initialisation de la base de données
with app.app_context():
    db.create_all()
    print("✅ Base de données LMNP initialisée")

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    """Servir les fichiers statiques du frontend"""
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return jsonify({
                'message': 'LMNP Expert Backend API',
                'version': '2.0.0',
                'endpoints': [
                    '/api/health',
                    '/api/users',
                    '/api/declarations',
                    '/api/biens',
                    '/api/calculs',
                    '/api/agents'
                ]
            })

if __name__ == '__main__':
    print("🚀 Démarrage LMNP Expert Backend v2.0")
    print("📊 Agents IA : Produit, Développeur, Fiscal")
    print("🔗 CORS activé pour frontend React")
    print("🌐 Serveur : http://0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)

