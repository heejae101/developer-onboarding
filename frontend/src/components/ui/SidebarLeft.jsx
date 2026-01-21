import React from 'react';
import { Calendar, CheckCircle2, Circle, LayoutDashboard, Settings, Moon, Sun } from 'lucide-react';
import { useTheme } from '../../context/ThemeContext';
import '../../styles/Sidebar.css';

const SidebarLeft = () => {
    const { theme, toggleTheme } = useTheme();

    const tasks = [
        { id: 1, title: '온보딩 가이드 확인', completed: true },
        { id: 2, title: 'Java 17 설치', completed: true },
        { id: 3, title: 'IDE 설정 완료', completed: false },
        { id: 4, title: '첫 빌드 실행', completed: false },
    ];

    return (
        <div className="sidebar-container sidebar-left glass-panel">
            {/* Header / Logo */}
            <div className="flex items-center justify-between px-2">
                <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-primary-500 to-indigo-600 flex items-center justify-center shadow-lg shadow-primary-500/20">
                        <span className="text-white font-bold text-lg">A</span>
                    </div>
                    <h1 className="text-lg font-bold tracking-tight sidebar-logo-text">Aura 온보딩</h1>
                </div>

                <button
                    onClick={toggleTheme}
                    className="p-2 rounded-lg hover:bg-white/10 transition-colors sidebar-icon-muted"
                    title={theme === 'dark' ? "라이트 모드로 변경" : "다크 모드로 변경"}
                >
                    {theme === 'dark' ? <Sun size={18} /> : <Moon size={18} />}
                </button>
            </div>

            {/* Navigation */}
            <nav className="flex flex-col gap-1">
                <NavItem icon={<LayoutDashboard size={18} />} label="Dashboard" active />
                <NavItem icon={<Calendar size={18} />} label="Calendar" />
                <NavItem icon={<Settings size={18} />} label="Settings" />
            </nav>

            <div className="h-px bg-white/5 my-1" />

            {/* Daily Calendar Widget */}
            <div className="flex flex-col gap-3">
                <div className="flex items-center justify-between sidebar-section-title">
                    <span>Today, Oct 26</span>
                </div>
                <div className="glass-card rounded-xl p-4 flex flex-col items-center justify-center h-28 bg-gradient-to-br from-slate-800/30 to-slate-900/30">
                    <span className="text-4xl font-bold text-white mb-1">26</span>
                    <span className="text-sm text-primary-400 font-medium">9:00 AM Standup</span>
                </div>
            </div>

            {/* Task Progress */}
            <div className="flex flex-col gap-3 flex-1 overflow-hidden">
                <div className="flex items-center justify-between sidebar-section-title">
                    <span>Task Progress (50%)</span>
                </div>

                <div className="flex flex-col gap-2 overflow-y-auto pr-1 custom-scrollbar">
                    {tasks.map((task) => (
                        <div key={task.id} className="group flex items-center gap-3 p-3 rounded-lg hover:bg-white/5 transition-colors cursor-pointer">
                            {task.completed ? (
                                <CheckCircle2 size={18} className="text-primary-400 shrink-0" />
                            ) : (
                                <Circle size={18} className="text-slate-600 group-hover:text-primary-400/50 shrink-0 transition-colors" />
                            )}
                            <span className={`text-sm truncate ${task.completed ? 'text-slate-400 line-through' : 'text-slate-200'}`}>
                                {task.title}
                            </span>
                        </div>
                    ))}
                </div>
            </div>

            {/* Profile Snippet */}
            <div className="mt-auto pt-4 border-t border-white/5 flex items-center gap-3 px-1">
                <div className="w-8 h-8 rounded-full bg-slate-700 overflow-hidden ring-2 ring-white/10">
                    <img src="https://ui-avatars.com/api/?name=New+Dev&background=random" alt="Profile" />
                </div>
                <div className="flex flex-col">
                    <span className="text-xs font-bold text-slate-200">New Developer</span>
                    <span className="text-[10px] text-slate-400">Junior Engineer</span>
                </div>
            </div>
        </div>
    );
};

const NavItem = ({ icon, label, active }) => (
    <button className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all ${active ? 'bg-primary-500/10 text-primary-400' : 'sidebar-nav-item'}`}>
        {icon}
        {label}
    </button>
);

export default SidebarLeft;
