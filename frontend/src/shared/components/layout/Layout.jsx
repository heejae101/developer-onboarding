import React from 'react';
import { Search, Book, Github, MessageSquare, Terminal } from 'lucide-react';

export function Header({ onSearch, searchTerm }) {
    return (
        <header className="sticky top-0 z-40 w-full border-b border-slate-200 bg-white/80 backdrop-blur-md">
            <div className="container mx-auto flex h-16 items-center justify-between px-6">
                <div className="flex items-center gap-2">
                    <div className="bg-primary-600 p-1.5 rounded-lg">
                        <Terminal className="w-5 h-5 text-white" />
                    </div>
                    <span className="text-2xl font-black tracking-tighter bg-clip-text text-transparent bg-gradient-to-r from-primary-600 via-indigo-600 to-violet-600">
                        Log:On
                    </span>
                    <span className="hidden md:inline-block h-4 w-px bg-slate-200 mx-2" />
                    <span className="hidden md:inline-block text-xs font-bold text-slate-400 uppercase tracking-widest">
                        Growth & Onboarding
                    </span>
                </div>

                <div className="flex-1 max-w-md mx-12">
                    <div className="relative group">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400 group-focus-within:text-primary-500 transition-colors" />
                        <input
                            type="text"
                            placeholder="무엇을 찾고 계신가요? (제목, 내용 검색)"
                            className="w-full bg-slate-100 border-transparent focus:bg-white focus:border-primary-500 focus:ring-4 focus:ring-primary-500/10 rounded-full py-2 pl-10 pr-4 transition-all duration-200 text-sm"
                            value={searchTerm}
                            onChange={(e) => onSearch(e.target.value)}
                        />
                    </div>
                </div>

                <nav className="flex items-center gap-6 text-sm font-medium text-slate-600">
                    <a href="#" className="hover:text-primary-600 transition-colors">프로젝트</a>
                    <a href="#" className="hover:text-primary-600 transition-colors">회고록</a>
                    <a href="https://github.com" target="_blank" className="bg-slate-900 text-white p-2 rounded-full hover:bg-slate-800 transition-colors">
                        <Github className="w-4 h-4" />
                    </a>
                </nav>
            </div>
        </header>
    );
}

export function Footer() {
    return (
        <footer className="w-full border-t border-slate-200 bg-slate-50 py-12">
            <div className="container mx-auto px-6">
                <div className="flex flex-col md:flex-row justify-between items-center gap-8">
                    <div className="flex flex-col gap-2">
                        <span className="text-lg font-black text-slate-900 tracking-tighter">Log:On</span>
                        <p className="text-sm text-slate-500 max-w-sm text-center md:text-left font-medium">
                            기록(Log)을 통해 성장의 스위치를 켜는(On) 공간.<br />
                            주니어 개발자의 온보딩과 회고를 위한 플랫폼입니다.
                        </p>
                    </div>
                    <div className="flex gap-12">
                        <div className="flex flex-col gap-3">
                            <span className="text-sm font-semibold text-slate-900 uppercase">Links</span>
                            <a href="#" className="text-sm text-slate-600 hover:text-primary-600 transition-colors">개발 공부</a>
                            <a href="#" className="text-sm text-slate-600 hover:text-primary-600 transition-colors">지도 예시</a>
                        </div>
                        <div className="flex flex-col gap-3">
                            <span className="text-sm font-semibold text-slate-900 uppercase">Support</span>
                            <a href="#" className="text-sm text-slate-600 hover:text-primary-600 transition-colors">AI 도움닫기</a>
                            <a href="#" className="text-sm text-slate-600 hover:text-primary-600 transition-colors">문의하기</a>
                        </div>
                    </div>
                </div>
                <div className="mt-12 pt-8 border-t border-slate-200 text-center text-xs text-slate-400">
                    &copy; 2026 Chae Huijae. All rights reserved. Built with React & Spring Boot.
                </div>
            </div>
        </footer>
    );
}

export function MainLayout({ children, header }) {
    return (
        <div className="min-h-screen flex flex-col bg-slate-50 selection:bg-primary-100 selection:text-primary-900">
            {header}
            <main className="flex-1 container mx-auto px-6 py-8">
                {children}
            </main>
            <Footer />
        </div>
    );
}
