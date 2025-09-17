import { useState } from 'react';
import { QueryInputData } from '../types';
import './QueryInput.css';

interface QueryInputProps {
  onStartAnalysis: (data: QueryInputData) => void;
  disabled: boolean;
}

const QueryInput = ({ onStartAnalysis, disabled }: QueryInputProps) => {
  const [query, setQuery] = useState('');
  const [universalCot, setUniversalCot] = useState('');
  const [showAdvanced, setShowAdvanced] = useState(false);
  const [perspectiveCots, setPerspectiveCots] = useState({
    economic: '',
    environmental: '',
    technological: ''
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      onStartAnalysis({
        query: query.trim(),
        universalCot: universalCot.trim(),
        perspectiveCots
      });
    }
  };

  const handlePerspectiveCotChange = (perspective: keyof typeof perspectiveCots, value: string) => {
    setPerspectiveCots(prev => ({
      ...prev,
      [perspective]: value
    }));
  };

  const exampleQueries = [
    "What are the benefits and challenges of implementing renewable energy on a global scale?",
    "How can artificial intelligence transform healthcare delivery?",
    "What are the implications of space exploration for humanity?",
    "How should governments regulate cryptocurrency and digital assets?"
  ];

  const loadExample = (example: string) => {
    setQuery(example);
    setUniversalCot("be concise, focus on evidence-based analysis, avoid speculation");
    setPerspectiveCots({
      economic: "analyze costs, market impacts, and economic implications over the next 10 years",
      environmental: "consider environmental effects, sustainability, and ecological impact",
      technological: "evaluate technical feasibility, innovation potential, and limitations"
    });
  };

  return (
    <div className="query-input-container">
      <div className="query-header">
        <h2>Multi-Perspective Analysis</h2>
        <p>Enter your query to get comprehensive analysis from economic, environmental, and technological perspectives</p>
      </div>

      <form onSubmit={handleSubmit} className="query-form">
        {/* Main Query Input */}
        <div className="input-group">
          <label htmlFor="query" className="input-label">
            Your Query
            <span className="required">*</span>
          </label>
          <textarea
            id="query"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Enter your question or topic for multi-perspective analysis..."
            className="query-textarea"
            rows={3}
            disabled={disabled}
            required
          />
        </div>

        {/* Example Queries */}
        <div className="examples-section">
          <p className="examples-label">Quick Examples:</p>
          <div className="examples-grid">
            {exampleQueries.map((example, index) => (
              <button
                key={index}
                type="button"
                className="example-button"
                onClick={() => loadExample(example)}
                disabled={disabled}
              >
                {example}
              </button>
            ))}
          </div>
        </div>

        {/* Universal Chain of Thought */}
        <div className="input-group">
          <label htmlFor="universal-cot" className="input-label">
            Universal Chain of Thought
            <span className="optional">optional</span>
          </label>
          <textarea
            id="universal-cot"
            value={universalCot}
            onChange={(e) => setUniversalCot(e.target.value)}
            placeholder="General guidance for all AI models (e.g., 'be concise, focus on facts, avoid speculation')"
            className="cot-textarea"
            rows={2}
            disabled={disabled}
          />
        </div>

        {/* Advanced Settings Toggle */}
        <div className="advanced-toggle">
          <button
            type="button"
            className="toggle-button"
            onClick={() => setShowAdvanced(!showAdvanced)}
            disabled={disabled}
          >
            <span className={`toggle-icon ${showAdvanced ? 'expanded' : ''}`}>▼</span>
            Perspective-Specific Chain of Thought
          </button>
        </div>

        {/* Perspective-Specific CoTs */}
        {showAdvanced && (
          <div className="advanced-section slide-up">
            <div className="perspective-cots">
              <div className="input-group">
                <label htmlFor="economic-cot" className="input-label economic">
                  <span className="perspective-icon">💰</span>
                  Economic Perspective CoT
                </label>
                <textarea
                  id="economic-cot"
                  value={perspectiveCots.economic}
                  onChange={(e) => handlePerspectiveCotChange('economic', e.target.value)}
                  placeholder="Specific guidance for economic analysis (costs, markets, investments...)"
                  className="cot-textarea economic"
                  rows={2}
                  disabled={disabled}
                />
              </div>

              <div className="input-group">
                <label htmlFor="environmental-cot" className="input-label environmental">
                  <span className="perspective-icon">🌱</span>
                  Environmental Perspective CoT
                </label>
                <textarea
                  id="environmental-cot"
                  value={perspectiveCots.environmental}
                  onChange={(e) => handlePerspectiveCotChange('environmental', e.target.value)}
                  placeholder="Specific guidance for environmental analysis (sustainability, climate, ecology...)"
                  className="cot-textarea environmental"
                  rows={2}
                  disabled={disabled}
                />
              </div>

              <div className="input-group">
                <label htmlFor="technological-cot" className="input-label technological">
                  <span className="perspective-icon">🔧</span>
                  Technological Perspective CoT
                </label>
                <textarea
                  id="technological-cot"
                  value={perspectiveCots.technological}
                  onChange={(e) => handlePerspectiveCotChange('technological', e.target.value)}
                  placeholder="Specific guidance for technological analysis (innovation, feasibility, limitations...)"
                  className="cot-textarea technological"
                  rows={2}
                  disabled={disabled}
                />
              </div>
            </div>
          </div>
        )}

        {/* Submit Button */}
        <div className="submit-section">
          <button
            type="submit"
            className="submit-button"
            disabled={disabled || !query.trim()}
          >
            {disabled ? (
              <>
                <div className="spinner" />
                Analyzing...
              </>
            ) : (
              <>
                <span className="submit-icon">🚀</span>
                Start Multi-Perspective Analysis
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
};

export default QueryInput;
