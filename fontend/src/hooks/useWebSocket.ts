import { useState, useEffect, useRef, useCallback } from 'react';
import { ConnectionStatus } from '../types';

export interface UseWebSocketReturn {
  sendMessage: (message: any) => void;
  lastMessage: MessageEvent | null;
  connectionStatus: ConnectionStatus;
  disconnect: () => void;
  reconnect: () => void;
}

export const useWebSocket = (url: string): UseWebSocketReturn => {
  const [connectionStatus, setConnectionStatus] = useState<ConnectionStatus>('Disconnected');
  const [lastMessage, setLastMessage] = useState<MessageEvent | null>(null);
  const ws = useRef<WebSocket | null>(null);
  const reconnectTimeoutRef = useRef<number | null>(null);
  const reconnectAttempts = useRef(0);
  const maxReconnectAttempts = 5;

  const connect = useCallback(() => {
    try {
      setConnectionStatus('Connecting');
      ws.current = new WebSocket(url);

      ws.current.onopen = () => {
        setConnectionStatus('Connected');
        reconnectAttempts.current = 0;
        console.log('WebSocket connected');
      };

      ws.current.onmessage = (event) => {
        setLastMessage(event);
      };

      ws.current.onclose = (event) => {
        setConnectionStatus('Disconnected');
        console.log('WebSocket disconnected:', event.code, event.reason);

        // Attempt to reconnect if it wasn't a manual close
        if (event.code !== 1000 && reconnectAttempts.current < maxReconnectAttempts) {
          const timeout = Math.min(1000 * Math.pow(2, reconnectAttempts.current), 10000);
          reconnectTimeoutRef.current = setTimeout(() => {
            reconnectAttempts.current++;
            console.log(`Reconnection attempt ${reconnectAttempts.current}/${maxReconnectAttempts}`);
            connect();
          }, timeout);
        }
      };

      ws.current.onerror = (error) => {
        setConnectionStatus('Error');
        console.error('WebSocket error:', error);
      };
    } catch (error) {
      setConnectionStatus('Error');
      console.error('Failed to create WebSocket connection:', error);
    }
  }, [url]);

  const disconnect = useCallback(() => {
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current);
      reconnectTimeoutRef.current = null;
    }
    
    if (ws.current) {
      ws.current.close(1000, 'Manual disconnect');
      ws.current = null;
    }
    setConnectionStatus('Disconnected');
  }, []);

  const reconnect = useCallback(() => {
    disconnect();
    reconnectAttempts.current = 0;
    connect();
  }, [disconnect, connect]);

  const sendMessage = useCallback((message: any) => {
    if (ws.current && ws.current.readyState === WebSocket.OPEN) {
      try {
        ws.current.send(JSON.stringify(message));
      } catch (error) {
        console.error('Failed to send WebSocket message:', error);
      }
    } else {
      console.warn('WebSocket is not connected. Cannot send message:', message);
    }
  }, []);

  useEffect(() => {
    connect();

    return () => {
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }
      if (ws.current) {
        ws.current.close(1000, 'Component unmounting');
      }
    };
  }, [connect]);

  return {
    sendMessage,
    lastMessage,
    connectionStatus,
    disconnect,
    reconnect
  };
};
