from flask import Flask, Response, request, jsonify
from flask_cors import CORS
from lib.bedrock import BedrockAgent
import json

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://localhost:3000", "https://vct-esports-manager.vercel.app/", "https://vct-esports-manager-9lukhztz2-albertcho-utexasedus-projects.vercel.app/"]}})

# Initialize Bedrock client and agent
bedrock_agent = BedrockAgent()

@app.route('/query_agent', methods=['GET'])
def query_agent():
    prompt = request.args.get('prompt')
    session_id = request.args.get('session_id', None)

    def stream_agent_wrapper():
        for i, (chunk, ret_session_id) in enumerate(bedrock_agent.invoke_agent(session_id, prompt)):
            yield json.dumps({
                "chunk_id": i,
                "session_id": ret_session_id,
                "response": chunk
            }) + '\n'

    return Response(stream_agent_wrapper(), content_type='application/json')

if __name__ == '__main__':
    app.run(debug=True)
