import React from 'react';
import { BookOpen, Info, Search, ShieldCheck } from 'lucide-react';
import '../../styles/Sidebar.css';

const SidebarRight = () => {
    return (
        <div className="sidebar-container sidebar-right glass-panel hidden lg:flex">
            <div className="flex items-center justify-between px-1">
                <h3 className="text-sm font-bold uppercase tracking-widest flex items-center gap-2 sidebar-logo-text">
                    <BookOpen size={16} className="text-primary-400" />
                    컨텍스트 (Context)
                </h3>
                <button className="p-1.5 rounded-lg hover:bg-[var(--glass-card-hover)] text-[var(--text-muted)] hover:text-[var(--text-main)] transition-colors">
                    <Search size={16} />
                </button>
            </div>

            {/* Rule Card 1 */}
            <div className="glass-card p-4 rounded-xl flex flex-col gap-3 group hover:border-primary-500/30 transition-all">
                <div className="flex items-center gap-2 text-xs font-bold text-primary-400">
                    <ShieldCheck size={14} />
                    <span>핵심 규칙 #1</span>
                </div>
                <p className="text-sm font-medium leading-relaxed" style={{ color: 'var(--text-muted)' }}>
                    모든 백엔드 서비스는 <span className="text-white bg-slate-800 px-1 rounded">Java 17</span>을 사용합니다. JPA 엔티티에는 @Data 사용을 지양하세요.
                </p>
                <div className="h-1 w-full bg-slate-800 rounded-full overflow-hidden mt-1">
                    <div className="h-full w-3/4 bg-primary-500 rounded-full" />
                </div>
                <div className="flex justify-between text-[10px]" style={{ color: 'var(--text-muted)' }}>
                    <span>관련성</span>
                    <span>높음</span>
                </div>
            </div>

            {/* Rule Card 2 */}
            <div className="glass-card p-4 rounded-xl flex flex-col gap-3 group hover:border-primary-500/30 transition-all">
                <div className="flex items-center gap-2 text-xs font-bold text-emerald-400">
                    <Info size={14} />
                    <span>모범 사례 (Best Practice)</span>
                </div>
                <p className="text-sm font-medium leading-relaxed" style={{ color: 'var(--text-muted)' }}>
                    커밋 메시지는 항상 <span className="text-white bg-slate-800 px-1 rounded">feat:</span> 또는 <span className="text-white bg-slate-800 px-1 rounded">fix:</span>와 같은 태그로 시작하세요.
                </p>
                <div className="h-1 w-full bg-slate-800 rounded-full overflow-hidden mt-1">
                    <div className="h-full w-1/2 bg-emerald-500 rounded-full" />
                </div>
                <div className="flex justify-between text-[10px]" style={{ color: 'var(--text-muted)' }}>
                    <span>관련성</span>
                    <span>중간</span>
                </div>
            </div>

            {/* Useful Links / Docs */}
            <div className="mt-auto">
                <h4 className="text-xs font-bold uppercase mb-3 px-1 sidebar-section-title">빠른 참고 문서</h4>
                <div className="flex flex-col gap-1">
                    <DocLink label="아키텍처 개요" />
                    <DocLink label="DB 스키마" />
                    <DocLink label="API 문서 (Swagger)" />
                </div>
            </div>
        </div>
    );
};

const DocLink = ({ label }) => (
    <a href="#" className="block px-3 py-2 rounded-lg text-sm transition-colors truncate doc-link">
        {label}
    </a>
)

export default SidebarRight;
