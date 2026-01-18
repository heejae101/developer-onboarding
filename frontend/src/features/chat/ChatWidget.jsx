import React, { useState } from 'react';
import { MessageSquare, X, Send, Bot, User } from 'lucide-react';
import { clsx } from 'clsx';

export default function ChatWidget() {
    const [isOpen, setIsOpen] = useState(false);
    const [messages, setMessages] = useState([
        { id: 1, text: "안녕하세요! '신입 온보딩 & 회고' 플랫폼의 AI 에이전트입니다. 궁금한 점이 있으시면 언제든 물어보세요.", isBot: true }
    ]);
    const [input, setInput] = useState('');

    const handleSend = (e) => {
        e.preventDefault();
        if (!input.trim()) return;

        const newUserMessage = { id: Date.now(), text: input, isBot: false };
        setMessages([...messages, newUserMessage]);
        setInput('');

        // AI 응답 시뮬레이션
        setTimeout(() => {
            const botResponse = {
                id: Date.now() + 1,
                text: `'${input}'에 대해 현재 학습된 데이터를 기반으로 답변을 준비 중입니다. 조만간 실시간 연동이 시작될 예정입니다!`,
                isBot: true
            };
            setMessages(prev => [...prev, botResponse]);
        }, 1000);
    };

    return (
        <div className="fixed bottom-6 right-6 z-50">
            {/* Chat Window */}
            {isOpen && (
                <div className="absolute bottom-16 right-0 w-[400px] h-[600px] bg-white rounded-2xl shadow-2xl border border-slate-200 flex flex-col overflow-hidden animate-in slide-in-from-bottom-4 fade-in duration-300">
                    {/* Header */}
                    <div className="bg-primary-600 p-4 flex items-center justify-between text-white">
                        <div className="flex items-center gap-3">
                            <div className="bg-white/20 p-2 rounded-lg backdrop-blur-sm">
                                <Bot className="w-5 h-5" />
                            </div>
                            <div>
                                <h3 className="font-bold">AI 에이전트</h3>
                                <p className="text-[10px] text-primary-100">온보딩 및 회우 도우미</p>
                            </div>
                        </div>
                        <button onClick={() => setIsOpen(false)} className="hover:bg-white/10 p-1 rounded-full transition-colors">
                            <X className="w-5 h-5" />
                        </button>
                    </div>

                    {/* Messages */}
                    <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-slate-50">
                        {messages.map((msg) => (
                            <div key={msg.id} className={clsx("flex gap-3", msg.isBot ? "justify-start" : "justify-end")}>
                                {msg.isBot && <div className="w-8 h-8 rounded-full bg-primary-100 flex items-center justify-center shrink-0 border border-primary-200"><Bot className="w-4 h-4 text-primary-600" /></div>}
                                <div className={clsx(
                                    "max-w-[80%] p-3 rounded-2xl text-sm leading-relaxed shadow-sm",
                                    msg.isBot ? "bg-white text-slate-800 rounded-tl-none border border-slate-100" : "bg-primary-600 text-white rounded-tr-none"
                                )}>
                                    {msg.text}
                                </div>
                                {!msg.isBot && <div className="w-8 h-8 rounded-full bg-slate-200 flex items-center justify-center shrink-0"><User className="w-4 h-4 text-slate-600" /></div>}
                            </div>
                        ))}
                    </div>

                    {/* Input */}
                    <form onSubmit={handleSend} className="p-4 bg-white border-t border-slate-100 flex gap-2">
                        <input
                            type="text"
                            placeholder="메시지를 입력해 주세요..."
                            className="flex-1 bg-slate-100 border-none rounded-xl px-4 py-2 text-sm focus:ring-2 focus:ring-primary-500 focus:bg-white transition-all"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                        />
                        <button type="submit" className="bg-primary-600 text-white p-2 rounded-xl hover:bg-primary-700 transition-colors shadow-lg shadow-primary-600/20 active:scale-95">
                            <Send className="w-4 h-4" />
                        </button>
                    </form>
                </div>
            )}

            {/* Toggle Button */}
            <button
                onClick={() => setIsOpen(!isOpen)}
                className={clsx(
                    "w-14 h-14 rounded-full flex items-center justify-center shadow-2xl transition-all duration-300 active:scale-90 overflow-hidden group",
                    isOpen ? "bg-white text-slate-900 border border-slate-200" : "bg-primary-600 text-white hover:bg-primary-700 hover:-translate-y-1"
                )}
            >
                {isOpen ? <X className="w-6 h-6" /> : (
                    <>
                        <MessageSquare className="w-6 h-6 absolute group-hover:scale-0 transition-transform duration-300" />
                        <Bot className="w-6 h-6 scale-0 group-hover:scale-100 transition-transform duration-300" />
                    </>
                )}
            </button>
        </div>
    );
}
