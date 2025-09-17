import { ConnectionStatus } from '../types';
import './Header.css';

interface HeaderProps {
  connectionStatus: ConnectionStatus;
}

const Header = ({ connectionStatus }: HeaderProps) => {
  const getStatusColor = () => {
    switch (connectionStatus) {
      case 'Connected':
        return 'var(--success)';
      case 'Connecting':
        return 'var(--warning)';
      case 'Disconnected':
      case 'Error':
        return 'var(--error)';
      default:
        return 'var(--text-muted)';
    }
  };

  return (
    <header className="header">
      <div className="header-content">
        <div className="logo-section">
          <div className="logo">
            <span className="logo-icon">🧠</span>
            <h1 className="logo-text">LLM Ensemble</h1>
          </div>
          <p className="tagline">Multi-Perspective AI Analysis</p>
        </div>
        
        <div className="status-section">
          <div className="connection-status">
            <div 
              className={`status-indicator ${connectionStatus.toLowerCase()}`}
              style={{ backgroundColor: getStatusColor() }}
            />
            <span className="status-text">{connectionStatus}</span>
          </div>
          
          <div className="models-info">
            <div className="model-badge claude">Claude</div>
            <div className="model-badge gpt">GPT</div>
            <div className="model-badge grok">Grok</div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
