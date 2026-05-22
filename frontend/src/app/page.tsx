'use client';

import React, { useState } from 'react';

type Citation = {
  doc_id: string;
  doc_title: string;
  url: string;
  text_snippet: string;
  relevance_score: number;
};

type RetrievalStats = {
  total_docs_queried: number;
  docs_after_filtering: number;
  docs_after_reranking: number;
  vector_search_ms: number;
  rerank_time_ms: number;
  llm_generation_ms: number;
  total_latency_ms: number;
};

type AgentResponse = {
  success: boolean;
  answer: string | null;
  confidence?: number;
  citations?: Citation[];
  retrieval_stats?: RetrievalStats;
  error?: string | null;
  suggestion?: string | null;
};

type Message = {
  role: 'user' | 'agent';
  content: string;
  responseDetails?: AgentResponse;
};

export default function Home() {
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [selectedAgent, setSelectedAgent] = useState('pluriversal_architect');
  const [isLoading, setIsLoading] = useState(false);

  const agents = [
    { id: 'pluriversal_architect', name: 'Pluriversal Architect Agent' },
    { id: 'ptst_specialist', name: 'PTST Specialist (Twist-Structured)' },
    { id: 'kcpm_oracle', name: 'KCPM Oracle (Kuramoto-Cortical)' }
  ];

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    const userMessage: Message = { role: 'user', content: query };
    setMessages((prev) => [...prev, userMessage]);
    setQuery('');
    setIsLoading(true);

    try {
      const res = await fetch('/api/agent', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: userMessage.content,
          user_id: 'guest_user_123',
          document_collection: 'knowledge_base',
          agent_type: selectedAgent
        })
      });

      const data: AgentResponse = await res.json();

      const agentMessage: Message = {
        role: 'agent',
        content: data.answer || data.error || 'Unknown error occurred.',
        responseDetails: data
      };

      setMessages((prev) => [...prev, agentMessage]);
    } catch (error) {
      console.error(error);
      const errorMessage: Message = {
        role: 'agent',
        content: 'Failed to communicate with the agent.'
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex h-screen bg-gray-100 font-sans text-gray-900">
      {/* Sidebar */}
      <aside className="w-64 bg-slate-800 text-white p-6 flex flex-col shadow-lg">
        <h1 className="text-xl font-bold mb-8 text-cyan-400 tracking-wider">Multi-Agent UI</h1>

        <div className="mb-6">
          <label className="block text-sm font-medium mb-2 text-slate-300">Select Agent</label>
          <div className="space-y-2">
            {agents.map((agent) => (
              <label
                key={agent.id}
                className={`flex items-center p-3 rounded-md cursor-pointer transition-colors border border-transparent ${selectedAgent === agent.id ? 'bg-slate-700 border-cyan-500 text-cyan-300 shadow-inner' : 'hover:bg-slate-700'}`}
              >
                <input
                  type="radio"
                  name="agent"
                  value={agent.id}
                  checked={selectedAgent === agent.id}
                  onChange={(e) => setSelectedAgent(e.target.value)}
                  className="sr-only"
                />
                <span className="text-sm">{agent.name}</span>
              </label>
            ))}
          </div>
        </div>

        <div className="mt-auto">
          <div className="text-xs text-slate-400 bg-slate-900 p-4 rounded-md shadow-inner">
            <p className="font-semibold mb-1 text-slate-300">Agent Configuration</p>
            <p>Role: Reflector + ToolUser</p>
            <p>Timeout: 8s</p>
            <p>Model: gpt-4o:2025-01</p>
          </div>
        </div>
      </aside>

      {/* Main Chat Area */}
      <main className="flex-1 flex flex-col bg-white">
        {/* Header */}
        <header className="border-b px-8 py-4 flex justify-between items-center bg-white shadow-sm z-10">
          <h2 className="text-xl font-semibold text-slate-800">
            {agents.find(a => a.id === selectedAgent)?.name} Interface
          </h2>
          <span className="bg-cyan-100 text-cyan-800 text-xs px-2 py-1 rounded-full font-medium border border-cyan-200">
            Active Context: Repository Docs
          </span>
        </header>

        {/* Chat History */}
        <div className="flex-1 p-8 overflow-y-auto space-y-8 bg-gray-50">
          {messages.length === 0 ? (
            <div className="h-full flex flex-col items-center justify-center text-gray-400">
              <svg className="w-16 h-16 mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" /></svg>
              <p className="text-lg font-medium">Ask a question to the Pluriversal Core</p>
              <p className="text-sm mt-2 text-gray-500">Try asking about Continuous Concept-Token Attention or TDA routing.</p>
            </div>
          ) : (
            messages.map((msg, idx) => (
              <div key={idx} className={`flex flex-col ${msg.role === 'user' ? 'items-end' : 'items-start'}`}>
                <div className={`max-w-[80%] rounded-2xl p-4 shadow-sm ${msg.role === 'user' ? 'bg-cyan-600 text-white rounded-br-none' : 'bg-white border border-gray-200 text-gray-800 rounded-bl-none'}`}>
                  <p className="text-sm leading-relaxed whitespace-pre-wrap">{msg.content}</p>
                </div>

                {msg.role === 'agent' && msg.responseDetails && msg.responseDetails.success && (
                  <div className="mt-3 max-w-[80%] flex flex-col gap-3 w-full">

                    {/* Citations */}
                    {msg.responseDetails.citations && msg.responseDetails.citations.length > 0 && (
                      <div className="bg-amber-50 border border-amber-200 rounded-lg p-4 w-full shadow-sm">
                        <h4 className="text-xs font-bold text-amber-800 mb-2 uppercase tracking-wider flex items-center">
                          <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
                          Citations
                        </h4>
                        <div className="space-y-3">
                          {msg.responseDetails.citations.map((cite, cIdx) => (
                            <div key={cIdx} className="bg-white p-3 rounded border border-amber-100 shadow-sm text-sm">
                              <p className="font-semibold text-slate-800 mb-1">{cite.doc_title}</p>
                              <p className="text-slate-600 italic mb-2">&quot;{cite.text_snippet}&quot;</p>
                              <div className="flex justify-between items-center text-xs">
                                <span className="text-cyan-600 font-mono bg-cyan-50 px-2 py-1 rounded">Score: {(cite.relevance_score * 100).toFixed(1)}%</span>
                                <span className="text-gray-400 font-mono truncate max-w-[200px]" title={cite.doc_id}>{cite.doc_id}</span>
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Stats */}
                    {msg.responseDetails.retrieval_stats && (
                      <div className="bg-slate-50 border border-slate-200 rounded-lg p-4 w-full shadow-sm text-xs text-slate-600 font-mono">
                        <div className="flex justify-between items-center mb-2 pb-2 border-b border-slate-200">
                          <span className="font-bold text-slate-700 uppercase tracking-wider">Retrieval Analytics</span>
                          {msg.responseDetails.confidence && (
                            <span className="bg-green-100 text-green-800 px-2 py-1 rounded font-bold">
                              Confidence: {(msg.responseDetails.confidence * 100).toFixed(1)}%
                            </span>
                          )}
                        </div>
                        <div className="grid grid-cols-2 gap-x-4 gap-y-2">
                          <div className="flex justify-between"><span>Queried:</span> <span className="font-bold">{msg.responseDetails.retrieval_stats.total_docs_queried}</span></div>
                          <div className="flex justify-between"><span>Vector MS:</span> <span className="font-bold">{msg.responseDetails.retrieval_stats.vector_search_ms}ms</span></div>
                          <div className="flex justify-between"><span>Filtered:</span> <span className="font-bold">{msg.responseDetails.retrieval_stats.docs_after_filtering}</span></div>
                          <div className="flex justify-between"><span>Rerank MS:</span> <span className="font-bold">{msg.responseDetails.retrieval_stats.rerank_time_ms}ms</span></div>
                          <div className="flex justify-between"><span>Reranked:</span> <span className="font-bold">{msg.responseDetails.retrieval_stats.docs_after_reranking}</span></div>
                          <div className="flex justify-between"><span>Gen MS:</span> <span className="font-bold">{msg.responseDetails.retrieval_stats.llm_generation_ms}ms</span></div>
                          <div className="col-span-2 flex justify-between mt-1 pt-1 border-t border-slate-200">
                            <span className="font-bold text-slate-700">Total Latency:</span>
                            <span className="font-bold text-cyan-600">{msg.responseDetails.retrieval_stats.total_latency_ms}ms</span>
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>
            ))
          )}
          {isLoading && (
            <div className="flex items-start">
              <div className="bg-white border border-gray-200 text-gray-800 rounded-2xl rounded-bl-none p-4 shadow-sm flex items-center space-x-2">
                <div className="w-2 h-2 bg-cyan-500 rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-cyan-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                <div className="w-2 h-2 bg-cyan-500 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
                <span className="text-sm ml-2 text-gray-500">Synthesizing...</span>
              </div>
            </div>
          )}
        </div>

        {/* Input Area */}
        <div className="p-6 bg-white border-t">
          <form onSubmit={handleSubmit} className="flex gap-4 max-w-4xl mx-auto">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Ask about paraconsistent architectures, TDA routing, or continuous reasoning..."
              className="flex-1 p-4 bg-gray-50 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-cyan-500 focus:bg-white transition-all shadow-sm text-sm"
              disabled={isLoading}
            />
            <button
              type="submit"
              disabled={isLoading || !query.trim()}
              className="bg-cyan-600 hover:bg-cyan-700 text-white px-8 py-4 rounded-xl font-medium transition-colors shadow-sm disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center min-w-[120px]"
            >
              {isLoading ? 'Thinking...' : 'Ask Agent'}
            </button>
          </form>
          <div className="text-center mt-3 text-xs text-gray-400">
            This interface strictly adheres to the DCCDSchemaGuard constraint and hybrid Reflector+ToolUser configuration.
          </div>
        </div>
      </main>
    </div>
  );
}
