from flask import Blueprint, request, jsonify
from app.models import db, Conversation

conversations_bp = Blueprint('conversations', __name__, url_prefix='/api/conversations')

# ✅ Get all conversations
@conversations_bp.route('/', methods=['GET'])
def get_conversations():
    conversations = Conversation.query.all()
    return jsonify([{
        "id": conv.id,
        "user_id": conv.user_id,
        "agent_id": conv.agent_id,
        "started_at": conv.started_at,
        "last_active_at": conv.last_active_at
    } for conv in conversations]), 200

# ✅ Get a single conversation by ID
@conversations_bp.route('/<string:conversation_id>', methods=['GET'])
def get_conversation(conversation_id):
    conversation = Conversation.query.get(conversation_id)
    if not conversation:
        return jsonify({"error": "Conversation not found"}), 404
    return jsonify({
        "id": conversation.id,
        "user_id": conversation.user_id,
        "agent_id": conversation.agent_id,
        "started_at": conversation.started_at,
        "last_active_at": conversation.last_active_at
    }), 200

# ✅ Create a new conversation
@conversations_bp.route('/', methods=['POST'])
def create_conversation():
    data = request.json
    if not data.get("user_id") or not data.get("agent_id"):
        return jsonify({"error": "user_id and agent_id are required"}), 400

    new_conversation = Conversation(
        user_id=data["user_id"],
        agent_id=data["agent_id"]
    )
    db.session.add(new_conversation)
    db.session.commit()

    return jsonify({
        "id": new_conversation.id,
        "user_id": new_conversation.user_id,
        "agent_id": new_conversation.agent_id,
        "started_at": new_conversation.started_at,
        "last_active_at": new_conversation.last_active_at
    }), 201

# ✅ Delete a conversation
@conversations_bp.route('/<string:conversation_id>', methods=['DELETE'])
def delete_conversation(conversation_id):
    conversation = Conversation.query.get(conversation_id)
    if not conversation:
        return jsonify({"error": "Conversation not found"}), 404

    db.session.delete(conversation)
    db.session.commit()
    return jsonify({"message": "Conversation deleted successfully"}), 200