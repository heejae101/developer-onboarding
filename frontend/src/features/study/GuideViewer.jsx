import React from 'react';
import ReactMarkdown from 'react-markdown';
import { ChevronLeft, Share2, Clock, ThumbsUp } from 'lucide-react';

export default function GuideViewer({ guide, onBack }) {
    if (!guide) return null;

    return (
        <div className="max-w-4xl mx-auto animate-in fade-in slide-in-from-right-4 duration-500">
            {/* Toolbar */}
            <div className="flex items-center justify-between mb-8 pb-6 border-b border-slate-200">
                <button
                    onClick={onBack}
                    className="flex items-center gap-2 text-sm font-semibold text-slate-500 hover:text-primary-600 transition-colors bg-white px-4 py-2 rounded-xl border border-slate-200 shadow-sm"
                >
                    <ChevronLeft className="w-4 h-4" />
                    다시 목록으로
                </button>
                <div className="flex items-center gap-3">
                    <button className="p-2 rounded-xl text-slate-400 hover:bg-slate-100 transition-colors">
                        <Share2 className="w-5 h-5" />
                    </button>
                    <button className="flex items-center gap-2 bg-primary-600 text-white px-5 py-2 rounded-xl hover:bg-primary-700 transition-colors shadow-lg shadow-primary-600/20 active:scale-95">
                        <ThumbsUp className="w-4 h-4" />
                        <span className="text-sm font-bold">도움됐어요</span>
                    </button>
                </div>
            </div>

            {/* Content Area */}
            <article className="bg-white rounded-[40px] shadow-sm border border-slate-100 overflow-hidden min-h-[70vh]">
                {/* Hero Header */}
                <div className="bg-slate-900 p-12 text-white">
                    <div className="flex items-center gap-3 mb-6">
                        <span className="px-3 py-1 bg-primary-500 text-[10px] font-bold uppercase tracking-widest rounded-full">
                            {guide.category}
                        </span>
                        <div className="flex items-center gap-2 text-slate-400 text-xs">
                            <Clock className="w-3 h-3" />
                            <span>최근 업데이트: {new Date(guide.updatedAt).toLocaleDateString()}</span>
                        </div>
                    </div>
                    <h1 className="text-4xl md:text-5xl font-black mb-4 leading-tight">
                        {guide.title}
                    </h1>
                </div>

                {/* Markdown Body */}
                <div className="p-12 md:px-20 py-16">
                    <div className="prose prose-slate prose-lg max-w-none 
                        prose-headings:font-black prose-headings:text-slate-900
                        prose-p:text-slate-600 prose-p:leading-relaxed
                        prose-strong:text-slate-900 prose-strong:font-bold
                        prose-code:text-primary-600 prose-code:bg-primary-50 prose-code:px-1.5 prose-code:py-0.5 prose-code:rounded prose-code:before:content-none prose-code:after:content-none
                        prose-pre:bg-slate-900 prose-pre:rounded-2xl prose-pre:p-6
                        prose-img:rounded-3xl prose-img:shadow-xl
                        prose-blockquote:border-l-4 prose-blockquote:border-primary-500 prose-blockquote:bg-slate-50 prose-blockquote:py-2 prose-blockquote:px-8 prose-blockquote:rounded-r-2xl prose-blockquote:text-slate-700 prose-blockquote:italic"
                    >
                        <ReactMarkdown>{guide.content}</ReactMarkdown>
                    </div>
                </div>
            </article>

            {/* Footer Navigation (Optional) */}
            <div className="mt-12 flex justify-center pb-20">
                <p className="text-slate-400 text-sm italic">"기록은 기억보다 위대하다. 오늘도 성장하는 나를 응원합니다."</p>
            </div>
        </div>
    );
}
