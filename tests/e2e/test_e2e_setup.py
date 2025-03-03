euewekll no cimport pytest
from app import create_app, db
from app.models import User, Agent

@pytest.fixture
def e2e_app():
    """Create and configure a test Flask application instance for E2E tests."""
    app = create_app()
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def e2e_client(e2e_app):
    """Create a test client for E2E tests."""
    return e2e_app.test_client()

@pytest.fixture
def seed_test_data(e2e_app):
    """Seed the database with test data for E2E tests."""
    with e2e_app.app_context():
        # Create test user
        user = User(name='E2E Test User', email='e2e@test.com')
        db.session.add(user)
        
        # Create test agent
        agent = Agent(
            provider='OpenAI',
            system_message='You are a helpful assistant',
            name='E2E Test Agent'
        )
        db.session.add(agent)
        
        db.session.commit()
        
        return {
            'user_id': str(user.id),
            'agent_id': str(agent.id)
        }
