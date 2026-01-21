import React, { useState } from 'react';
import { Send, Sparkles, Code2, Paperclip, Mic } from 'lucide-react';

const ChatArea = () => {
    const [messages, setMessages] = useState([
        { id: 1, role: 'ai', content: "안녕하세요! Aura 온보딩 가이드입니다. 오늘 프로젝트와 관련해서 도와드릴까요?", timestamp: '오전 9:00' },
        { id: 2, role: 'user', content: "이 프로젝트 백엔드 패키지 구조가 궁금해요.", timestamp: '오전 9:01' },
        { id: 3, role: 'ai', content: "네, 알려드릴게요. 저희 백엔드는 도메인 주도 설계를 따르고 있습니다. 메인 컨트롤러는 `src/main/java/com/example/demo/domain` 아래에서 찾으실 수 있습니다. 예시로 `GoalController`를 보여드릴까요?", timestamp: '오전 9:01' }
    ]);
    const [inputValue, setInputValue] = useState("");

    const handleSend = () => {
        if (!inputValue.trim()) return;
        setMessages([...messages, { id: Date.now(), role: 'user', content: inputValue, timestamp: new Date().toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit' }) }]);
        setInputValue("");
        // Simulate AI thinking and response
        setTimeout(() => {
            setMessages(prev => [...prev, { id: Date.now() + 1, role: 'ai', content: "프로젝트 룰과 대조하여 분석 중입니다... (시뮬레이션)", timestamp: new Date().toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit' }) }]);
        }, 1000);
    };

    return (
        <div className="flex-1 flex flex-col h-full relative z-10">
            {/* Top Bar (Optional Title or Context) */}
            <div className="h-16 flex items-center px-8 border-b border-white/5">
                <h2 className="text-sm font-semibold flex items-center gap-2">
                    <Sparkles size={16} className="text-primary-400" />
                    AI 에이전트 활성화
                </h2>
                <div className="ml-auto flex items-center gap-4 text-xs text-slate-500">
                    <span className="px-2 py-1 rounded bg-slate-800/50 border border-slate-700">모델: GPT-4o-Hybrid</span>
                </div>
            </div>

            {/* Chat Messages */}
            <div className="flex-1 overflow-y-auto px-8 py-6 flex flex-col gap-6 custom-scrollbar">
                {messages.map((msg) => (
                    <div key={msg.id} className={`flex gap-4 ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}>
                        {/* Avatar */}
                        <div className={`w-9 h-9 rounded-full flex items-center justify-center shrink-0 border border-white/10 ${msg.role === 'ai' ? 'bg-gradient-to-br from-indigo-500 to-primary-600 shadow-lg shadow-indigo-500/20' : 'bg-slate-700'}`}>
                            {msg.role === 'ai' ? <Sparkles size={18} className="text-white" /> : <span className="text-xs font-bold text-white">나</span>}
                        </div>

                        {/* Bubble */}
                        <div className={`flex flex-col gap-1 max-w-[70%] ${msg.role === 'user' ? 'items-end' : 'items-start'}`}>
                            <div className={`rounded-2xl px-5 py-3 text-sm leading-relaxed shadow-sm ${msg.role === 'ai' ? 'glass-card rounded-tl-none' : 'bg-primary-600 text-white rounded-tr-none shadow-primary-500/10'}`}>
                                {msg.content}
                            </div>
                            <span className="text-[10px] text-slate-500 px-1">{msg.timestamp}</span>
                        </div>
                    </div>
                ))}
            </div>

            {/* Input Area */}
            <div className="p-6 pb-8">
                <div className="glass-input rounded-2xl p-2 flex flex-col focus-within:ring-2 focus-within:ring-primary-500/30 transition-shadow shadow-lg">
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
                        <button onClick={handleSend} className="p-2 rounded-xl bg-primary-600 hover:bg-primary-500 text-white shadow-lg shadow-primary-600/20 transition-all active:scale-95">
                            <Send size={18} />
                        </button>
                    </div>
                </div>
                <p className="text-center text-[10px] text-slate-600 mt-3">AI 에이전트는 실수를 할 수 있습니다. 중요한 로직은 반드시 검증하세요.</p>
            </div>
        </div>
    );
};

export default ChatArea;
