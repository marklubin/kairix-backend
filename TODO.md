# Kairix Backend TODO

## Initial Setup & Testing

1. Local Environment Setup
   - [ ] Install PostgreSQL locally
   - [ ] Create local database: `chatdb`
   - [ ] Set up Poetry environment: `poetry install`
   - [ ] Run migrations: `flask db upgrade`
   - [ ] Run test suite: `poetry run pytest`


## Database Enhancements

### 1. PostgreSQL Vector Support
- [ ] Add pgvector extension to PostgreSQL
- [ ] Update User model with embedding column
- [ ] Update Message model with embedding column
- [ ] Create migration for vector columns

### 2. Embedding Integration
- [ ] Create embedding utility module
- [ ] Implement embedding generation for users
- [ ] Implement embedding generation for messages
- [ ] Add vector similarity search endpoints

### 3. Database Optimization
- [ ] Add appropriate indexes for vector columns
- [ ] Implement database connection pooling
- [ ] Add database health check endpoint
- [ ] Implement query optimization for vector searches

## Testing & Documentation
- [ ] Write integration tests for vector operations
- [ ] Document API endpoints in OpenAPI/Swagger
- [ ] Add performance benchmarks for vector operations
- [ ] Create example queries for vector similarity search



📌 Kairix Backend TODO – Zapier Integration

Zapier Integration Setup

1. Function Configuration System
	•	Create a /config/zapier/ directory to store one JSON file per function.
	•	Define the JSON schema for function definitions.
	•	Implement a function to dynamically load and validate all function configs.
	•	Create an API endpoint to list available Zapier functions.

2. Zapier Webhooks Setup
	•	Set up Zapier Webhook Catcher for function calls.
	•	Define webhook endpoints in Zapier for each integration.
	•	Secure webhook calls with authentication & validation.
	•	Test webhook requests from Kairix to Zapier.

3. Dynamic Function Routing
	•	Implement dispatch_to_zapier() function to send requests based on config.
	•	Ensure request formatting is schema-compliant.
	•	Add logging & error handling for webhook responses.

4. AI Function Calling Registration
	•	Load function schemas from JSON and register with OpenAI Function Calling.
	•	Ensure AI can auto-generate correct API calls.
	•	Implement test cases for AI function execution.

5. Testing & Deployment
	•	Write unit tests for dispatch_to_zapier().
	•	Perform end-to-end tests with AI → Kairix → Zapier → External APIs.
	•	Deploy function configs & test webhook latency.
	•	Document new integration process.


  Zapier Integrations

1. Notion Integration
	•	Create a Zapier action to add a new page to a Notion database.
	•	Define create_notion_page function schema for AI to call.
	•	Map webhook data to Notion API fields (title, content, tags).
	•	Implement a test case for sending structured Notion updates via Zapier.

2. Trello Integration
	•	Set up a Zapier action to create Trello cards from AI-generated tasks.
	•	Define create_trello_card function schema.
	•	Allow users to configure their Trello board and list in Zapier.
	•	Test the flow: AI → Kairix → Zapier → Trello.

3. Gmail Integration
	•	Set up a Zapier action to send emails via Gmail.
	•	Define send_gmail_email function schema.
	•	Allow users to specify recipient, subject, and body dynamically.
	•	Ensure AI-generated emails are properly formatted and secure.

4. Google Calendar Integration
	•	Create a Zapier action to schedule events in Google Calendar.
	•	Define create_calendar_event function schema.
	•	Allow AI to send structured event details (title, time, participants).
	•	Test AI-driven event creation from a natural language command.


 Kairix Backend TODO – ElevenLabs + Twilio Integration

Twilio + ElevenLabs Conversational AI Pipeline

1. Twilio Setup
	•	Purchase & configure a Twilio phone number with voice support.
	•	Set up Twilio webhook to forward calls to ElevenLabs.
	•	Ensure Twilio is correctly routing speech input to ElevenLabs API.

2. ElevenLabs Conversational AI Configuration
	•	Register for ElevenLabs API & enable Conversational AI.
	•	Configure ElevenLabs to act as a processing layer between Twilio & Kairix.
	•	Define webhook routing so ElevenLabs sends transcriptions to Kairix.
	•	Tune ElevenLabs conversation state management for optimal AI flow.

3. Modify Kairix AI Backend to Accept Requests from ElevenLabs
	•	Create an API endpoint (/api/conversation) for ElevenLabs to send transcriptions.
	•	Ensure responses are structured correctly for ElevenLabs’ TTS engine.
	•	Optimize response latency to ensure fast voice interactions.
	•	Implement conversational memory to maintain AI context across turns.

4. Test End-to-End Voice AI Interaction
	•	Test the flow: Call Twilio → ElevenLabs transcribes → Kairix processes → ElevenLabs generates TTS → Response sent back via Twilio.
	•	Monitor & debug latency issues in the pipeline.
	•	Ensure ElevenLabs properly handles long interactions & multi-turn conversations.
	•	Fine-tune TTS quality and voice selection.

5. Deployment & Scaling
	•	Deploy the integration on production servers.
	•	Implement monitoring & logging for AI conversation tracking.
	•	Optimize error handling for edge cases (noisy input, dropped calls, etc.).
	•	Prepare documentation for setting up the Kairix + ElevenLabs + Twilio pipeline.