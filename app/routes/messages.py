from flask import Blueprint, request, jsonify
from app.models import db, Message

messages_bp = Blueprint('messages', __name__, url_prefix='/api/messages')

# ✅ Get all messages for a conversation
@messages_bp.route('/<string:conversation_id>', methods=['GET'])
def get_messages(conversation_id):
    messages = Message.query.filter_by(conversation_id=conversation_id).all()
    return jsonify([{
        "id": msg.id,
        "conversation_id": msg.conversation_id,
        "role": msg.role,
        "content": msg.content,
        "created_at": msg.created_at
    } for msg in messages]), 200

# ✅ Create a new message
@messages_bp.route('/', methods=['POST'])
def create_message():
    data = request.json
    if not data.get("conversation_id") or not data.get("role") or not data.get("content"):
        return jsonify({"error": "conversation_id, role, and content are required"}), 400

    new_message = Message(
        conversation_id=data["conversation_id"],
        role=data["role"],
        content=data["content"]
    )
    db.session.add(new_message)
    db.session.commit()

    return jsonify({
        "id": new_message.id,
        "conversation_id": new_message.conversation_id,
        "role": new_message.role,
        "content": new_message.content,
        "created_at": new_message.created_at
    }), 201