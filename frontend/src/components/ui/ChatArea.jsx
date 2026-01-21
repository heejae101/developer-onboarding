import React, { useState, useRef, useEffect } from 'react';
import { Send, Sparkles, Code2, Paperclip, Mic, StopCircle } from 'lucide-react';
import { streamChat } from '../../api/ai';
import '../../styles/ChatArea.css';

const ChatArea = () => {
    const [messages, setMessages] = useState([
        { id: 1, role: 'ai', content: "안녕하세요! Aura 온보딩 가이드입니다. 오늘 프로젝트와 관련해서 도와드릴까요?", timestamp: '오전 9:00' }
    ]);
    const [inputValue, setInputValue] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef(null);
    const abortControllerRef = useRef(null);

    // Auto-scroll to bottom
    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSend = async () => {
        if (!inputValue.trim() || isLoading) return;

        const userMessage = inputValue;
        setInputValue("");

        // 1. Add user message
        const userMsgObj = {
            id: Date.now(),
            role: 'user',
            content: userMessage,
            timestamp: new Date().toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit' })
        };

        setMessages(prev => [...prev, userMsgObj]);
        setIsLoading(true);

        // 2. Add placeholder AI message
        const aiMsgId = Date.now() + 1;
        setMessages(prev => [...prev, {
            id: aiMsgId,
            role: 'ai',
            content: "", // Start empty
            timestamp: new Date().toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit' })
        }]);

        // 3. Start Stream
        abortControllerRef.current = new AbortController();

        // Helper to update specific message content
        const updateAiMessage = (chunk) => {
            let displayedContent = chunk;
            try {
                // Try to parse JSON chunk if it looks like one
                if (chunk.trim().startsWith('{') && chunk.trim().endsWith('}')) {
                    const parsed = JSON.parse(chunk);

                    if (parsed.type === 'complete' || parsed.type === 'error') {
                        // Stop the stream if completed or error
                        if (abortControllerRef.current) {
                            abortControllerRef.current.abort();
                        }
                        setIsLoading(false);
                    }

                    if (parsed.content) {
                        displayedContent = parsed.content;
                    }
                }
            } catch (e) {
                // Not JSON, use as is
            }

            setMessages(prev => prev.map(msg =>
                msg.id === aiMsgId
                    ? { ...msg, content: msg.content + displayedContent }
                    : msg
            ));
        };

        await streamChat({
            message: userMessage,
            threadId: "default-thread", // User UUID can be added here later
            controller: abortControllerRef.current,
            onMessage: (chunk) => {
                // Remove quotes if raw string comes quoted from some backends
                // But usually SSE sends raw text data
                updateAiMessage(chunk);
            },
            onError: (err) => {
                console.error("Chat error:", err);
                setMessages(prev => prev.map(msg =>
                    msg.id === aiMsgId
                        ? { ...msg, content: msg.content + "\n⚠️ [Error] 응답 중 오류가 발생했습니다." }
                        : msg
                ));
                setIsLoading(false);
            },
            onComplete: () => {
                setIsLoading(false);
            }
        });
    };

    const handleStop = () => {
        if (abortControllerRef.current) {
            abortControllerRef.current.abort();
            setIsLoading(false);
        }
    };

    return (
        <div className="chat-area-container">
            {/* Top Bar */}
            <div className="h-16 flex items-center px-8 border-b border-white/5 shrink-0">
                <h2 className="text-sm font-semibold flex items-center gap-2">
                    <Sparkles size={16} className="text-primary-400" />
                    AI 에이전트 (With Kanana Safeguard)
                </h2>
                <div className="ml-auto flex items-center gap-4 text-xs text-slate-500">
                    <span className="px-2 py-1 rounded bg-slate-800/50 border border-slate-700">모델: sonnet3.5</span>
                </div>
            </div>

            {/* Chat Messages */}
            <div className="chat-messages-container custom-scrollbar">
                {messages.map((msg) => (
                    <div key={msg.id} className={`flex gap-4 ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}>
                        {/* Avatar */}
                        <div className={`w-9 h-9 rounded-full flex items-center justify-center shrink-0 border border-white/10 ${msg.role === 'ai' ? 'bg-gradient-to-br from-indigo-500 to-primary-600 shadow-lg shadow-indigo-500/20' : 'bg-slate-700'}`}>
                            {msg.role === 'ai' ? <Sparkles size={18} className="text-white" /> : <span className="text-xs font-bold text-white">나</span>}
                        </div>

                        {/* Bubble */}
                        <div className={`flex flex-col gap-1 max-w-[70%] ${msg.role === 'user' ? 'items-end' : 'items-start'}`}>
                            <div className={`rounded-2xl px-5 py-3 text-sm leading-relaxed shadow-sm whitespace-pre-wrap ${msg.role === 'ai' ? 'glass-card rounded-tl-none' : 'bg-primary-600 text-white rounded-tr-none shadow-primary-500/10'}`}>
                                {msg.content}
                                {msg.role === 'ai' && isLoading && msg.id === messages[messages.length - 1].id && (
                                    <span className="inline-block w-2 h-4 ml-1 align-middle bg-primary-400 animate-pulse">|</span>
                                )}
                            </div>
                            <span className="text-[10px] text-slate-500 px-1">{msg.timestamp}</span>
                        </div>
                    </div>
                ))}
                <div ref={messagesEndRef} />
            </div>

            {/* Input Area (Fixed/Absolute) */}
            <div className="chat-input-wrapper">
                <div className="glass-input rounded-2xl p-2 flex flex-col focus-within:ring-2 focus-within:ring-primary-500/30 transition-shadow shadow-xl backdrop-blur-xl">
                    <textarea
                        className="w-full bg-transparent border-none placeholder:text-slate-500 text-sm resize-none focus:ring-0 p-3 min-h-[60px]"
                        placeholder="프로젝트 룰이나 코드에 대해 무엇이든 물어보세요..."
                        value={inputValue}
                        onChange={(e) => setInputValue(e.target.value)}
                        onKeyDown={(e) => {
                            if (e.key === 'Enter' && !e.shiftKey) {
                                if (e.nativeEvent.isComposing) return;
                                e.preventDefault();
                                handleSend();
                            }
                        }}
                        disabled={isLoading}
                    />
                    <div className="flex items-center justify-between px-2 pb-1">
                        <div className="flex items-center gap-2">
                            <button className="p-2 rounded-lg hover:bg-white/10 text-slate-400 hover:text-primary-300 transition-colors">
                                <Code2 size={18} />
                            </button>
                            <button className="p-2 rounded-lg hover:bg-white/10 text-slate-400 hover:text-primary-300 transition-colors">
                                <Paperclip size={18} />
                            </button>
                        </div>

                        {isLoading ? (
                            <button onClick={handleStop} className="p-2 rounded-xl bg-red-500/80 hover:bg-red-500 text-white shadow-lg transition-all active:scale-95">
                                <StopCircle size={18} />
                            </button>
                        ) : (
                            <button onClick={handleSend} disabled={!inputValue.trim()} className="p-2 rounded-xl bg-primary-600 hover:bg-primary-500 text-white shadow-lg shadow-primary-600/20 transition-all active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed">
                                <Send size={18} />
                            </button>
                        )}
                    </div>
                </div>
                <p className="text-center text-[10px] text-slate-600 mt-3">AI 에이전트는 실수를 할 수 있습니다. 중요한 로직은 반드시 검증하세요.</p>
            </div>
        </div>
    );
};

export default ChatArea;
