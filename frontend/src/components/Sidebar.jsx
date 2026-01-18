import React from 'react';
import { Book, Map as MapIcon, ChevronRight } from 'lucide-react';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

function cn(...inputs) {
    return twMerge(clsx(inputs));
}

export default function Sidebar({ guides, selectedId, onSelect, activeTab, onTabChange }) {
    return (
        <div className="w-64 h-screen bg-slate-900 text-slate-300 flex flex-col border-r border-slate-800">
            <div className="p-6">
                <h1 className="text-xl font-bold text-white flex items-center gap-2">
                    <Book className="w-6 h-6 text-primary-400" />
                    임시팀장 가이드
                </h1>
            </div>

            <nav className="flex-1 overflow-y-auto px-4 space-y-2">
                <div className="pb-4">
                    <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2 px-2">Main</p>
                    <button
                        onClick={() => onTabChange('map')}
                        className={cn(
                            "w-full flex items-center gap-3 px-3 py-2 rounded-lg transition-colors",
                            activeTab === 'map' ? "bg-primary-600 text-white" : "hover:bg-slate-800"
                        )}
                    >
                        <MapIcon className="w-5 h-5" />
                        현장 지도 보기
                    </button>
                </div>

                <div>
                    <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2 px-2">Guide Documents</p>
                    <div className="space-y-1">
                        {guides.map((guide) => (
                            <button
                                key={guide.id}
                                onClick={() => onSelect(guide.id)}
                                className={cn(
                                    "w-full flex items-center justify-between px-3 py-2 rounded-lg transition-colors text-sm text-left",
                                    selectedId === guide.id && activeTab === 'guide' ? "bg-slate-800 text-white" : "hover:bg-slate-800"
                                )}
                            >
                                <span className="truncate">{guide.title}</span>
                                <ChevronRight className={cn("w-4 h-4 transition-transform", selectedId === guide.id ? "rotate-90" : "")} />
                            </button>
                        ))}
                    </div>
                </div>
            </nav>

            <div className="p-4 border-t border-slate-800 text-xs text-slate-500 text-center">
                &copy; 2026 임시팀장 가이드
            </div>
        </div>
    );
}
