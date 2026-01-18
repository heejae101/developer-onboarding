import React from 'react';
import { Calendar, Tag, ArrowRight, User } from 'lucide-react';
import { clsx } from 'clsx';

export default function GuideCard({ guide, onSelect }) {
    const getCategoryColor = (category) => {
        switch (category) {
            case '개발 공부': return 'bg-blue-50 text-blue-600 border-blue-100 ring-blue-500/20';
            case '스스로 질문': return 'bg-purple-50 text-purple-600 border-purple-100 ring-purple-500/20';
            case '지도 예시': return 'bg-green-50 text-green-600 border-green-100 ring-green-500/20';
            case '하루 목표': return 'bg-orange-50 text-orange-600 border-orange-100 ring-orange-500/20';
            default: return 'bg-slate-50 text-slate-600 border-slate-100 ring-slate-500/20';
        }
    };

    return (
        <article
            onClick={() => onSelect(guide.id)}
            className="group cursor-pointer bg-white rounded-3xl border border-slate-200 p-6 transition-all duration-300 hover:shadow-2xl hover:shadow-primary-600/10 hover:-translate-y-2 border-b-4 border-b-transparent hover:border-b-primary-500"
        >
            <div className="flex flex-col h-full">
                <div className="flex items-center justify-between mb-4">
                    <span className={clsx(
                        "px-3 py-1 rounded-full text-[10px] font-bold uppercase tracking-wider border ring-1 ring-inset",
                        getCategoryColor(guide.category)
                    )}>
                        {guide.category || '기타'}
                    </span>
                    <div className="flex items-center gap-1.5 text-slate-400">
                        <Calendar className="w-3.5 h-3.5" />
                        <span className="text-[10px] font-medium">{new Date(guide.updatedAt).toLocaleDateString()}</span>
                    </div>
                </div>

                <h3 className="text-xl font-bold text-slate-900 group-hover:text-primary-600 transition-colors mb-3 line-clamp-2 leading-tight">
                    {guide.title}
                </h3>

                <p className="text-sm text-slate-500 line-clamp-3 mb-6 flex-1 leading-relaxed">
                    {guide.content ? guide.content.substring(0, 150).replace(/[#*`]/g, '') : "내용이 없습니다."}...
                </p>

                <div className="flex items-center justify-between pt-6 border-t border-slate-50">
                    <div className="flex items-center gap-2">
                        <div className="w-6 h-6 rounded-full bg-slate-100 flex items-center justify-center border border-slate-200">
                            <User className="w-3 h-3 text-slate-500" />
                        </div>
                        <span className="text-xs font-semibold text-slate-700">Chae Huijae</span>
                    </div>
                    <div className="text-primary-600 opacity-0 group-hover:opacity-100 transition-all duration-300 translate-x-4 group-hover:translate-x-0">
                        <ArrowRight className="w-5 h-5" />
                    </div>
                </div>
            </div>
        </article>
    );
}
