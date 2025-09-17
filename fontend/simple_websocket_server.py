#!/usr/bin/env python3
"""
Simple WebSocket Server Test for LLM Ensemble
"""

import asyncio
import json
import logging
import uuid
import websockets

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Store connected clients
connected_clients = {}

async def handle_client(websocket):
    """Handle a client connection"""
    client_id = str(uuid.uuid4())
    connected_clients[client_id] = websocket
    logger.info(f"Client {client_id} connected")
    
    try:
        # Send welcome message
        await websocket.send(json.dumps({
            "type": "connection_confirmed",
            "client_id": client_id,
            "message": "Successfully connected to LLM Ensemble WebSocket server"
        }))
        
        # Listen for messages
        async for message in websocket:
            data = json.loads(message)
            logger.info(f"Received from {client_id}: {data}")
            
            if data.get("type") == "start_analysis":
                # Simulate analysis
                await websocket.send(json.dumps({
                    "type": "analysis_started", 
                    "query": data.get("query", "")
                }))
                
                # Send some progress updates
                for i in range(1, 6):
                    await asyncio.sleep(1)
                    await websocket.send(json.dumps({
                        "type": "agent_response",
                        "agent_id": f"agent_{i}",
                        "agent_name": f"Agent {i}",
                        "response": f"Analysis result {i} for: {data.get('query', '')}",
                        "confidence": 0.8 + (i * 0.04)
                    }))
                
                # Send completion
                await websocket.send(json.dumps({
                    "type": "analysis_complete",
                    "final_response": f"Complete analysis for: {data.get('query', '')}",
                    "consensus_confidence": 0.95
                }))
            
    except websockets.exceptions.ConnectionClosed:
        logger.info(f"Client {client_id} disconnected")
    except Exception as e:
        logger.error(f"Error handling client {client_id}: {e}")
    finally:
        if client_id in connected_clients:
            del connected_clients[client_id]

async def main():
    """Start the server"""
    host = "localhost"
    port = 8001
    
    logger.info(f"Starting WebSocket server on {host}:{port}")
    
    async with websockets.serve(handle_client, host, port):
        logger.info("WebSocket server started successfully")
        logger.info(f"Frontend can connect to: ws://{host}:{port}")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    print("Starting Simple LLM Ensemble WebSocket Server")
    print("Frontend will connect to: ws://localhost:8001")
    print(" Use Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer stopped by user")
