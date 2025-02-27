from flask import Blueprint, request, jsonify
from app.models import db, Agent

agents_bp = Blueprint('agents', __name__, url_prefix='/api/agents')

# ✅ Get all agents
@agents_bp.route('/', methods=['GET'])
def get_agents():
    agents = Agent.query.all()
    return jsonify([{
        "id": agent.id,
        "provider": agent.provider,
        "system_message": agent.system_message,
        "settings": agent.settings
    } for agent in agents]), 200

# ✅ Get a single agent by ID
@agents_bp.route('/<string:agent_id>', methods=['GET'])
def get_agent(agent_id):
    agent = Agent.query.get(agent_id)
    if not agent:
        return jsonify({"error": "Agent not found"}), 404
    return jsonify({
        "id": agent.id,
        "provider": agent.provider,
        "system_message": agent.system_message,
        "settings": agent.settings
    }), 200

# ✅ Create a new agent
@agents_bp.route('/', methods=['POST'])
def create_agent():
    data = request.json
    if not data.get("provider"):
        return jsonify({"error": "Provider is required"}), 400

    new_agent = Agent(
        provider=data["provider"],
        system_message=data.get("system_message", ""),
        settings=data.get("settings", {})
    )
    db.session.add(new_agent)
    db.session.commit()

    return jsonify({
        "id": new_agent.id,
        "provider": new_agent.provider,
        "system_message": new_agent.system_message,
        "settings": new_agent.settings
    }), 201

# ✅ Update an existing agent
@agents_bp.route('/<string:agent_id>', methods=['PUT'])
def update_agent(agent_id):
    agent = Agent.query.get(agent_id)
    if not agent:
        return jsonify({"error": "Agent not found"}), 404

    data = request.json
    if "provider" in data:
        agent.provider = data["provider"]
    if "system_message" in data:
        agent.system_message = data["system_message"]
    if "settings" in data:
        agent.settings = data["settings"]

    db.session.commit()
    return jsonify({
        "id": agent.id,
        "provider": agent.provider,
        "system_message": agent.system_message,
        "settings": agent.settings
    }), 200

# ✅ Delete an agent
@agents_bp.route('/<string:agent_id>', methods=['DELETE'])
def delete_agent(agent_id):
    agent = Agent.query.get(agent_id)
    if not agent:
        return jsonify({"error": "Agent not found"}), 404

    db.session.delete(agent)
    db.session.commit()
    return jsonify({"message": "Agent deleted successfully"}), 200