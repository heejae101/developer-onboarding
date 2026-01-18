import React from 'react';
import { clsx } from 'clsx';
import { ChevronLeft, ChevronRight, CheckCircle2 } from 'lucide-react';

export default function GoalCalendar({ goals, selectedDate, onSelectDate }) {
    const today = new Date();
    const [viewDate, setViewDate] = React.useState(new Date(selectedDate));

    const daysInMonth = (year, month) => new Date(year, month + 1, 0).getDate();
    const firstDayOfMonth = (year, month) => new Date(year, month, 1).getDay();

    const year = viewDate.getFullYear();
    const month = viewDate.getMonth();

    const days = [];
    const firstDay = firstDayOfMonth(year, month);
    const totalDays = daysInMonth(year, month);

    // Padding for start of month
    for (let i = 0; i < firstDay; i++) {
        days.push(null);
    }

    for (let i = 1; i <= totalDays; i++) {
        days.push(new Date(year, month, i));
    }

    const getGoalForDate = (date) => {
        if (!date) return null;
        const dateStr = date.toISOString().split('T')[0];
        return goals.find(g => g.date === dateStr);
    };

    const nextMonth = () => setViewDate(new Date(year, month + 1, 1));
    const prevMonth = () => setViewDate(new Date(year, month - 1, 1));

    return (
        <div className="bg-white rounded-[40px] p-8 shadow-sm border border-slate-100 ring-1 ring-slate-200/50">
            <div className="flex items-center justify-between mb-8">
                <h3 className="text-2xl font-black text-slate-900 tracking-tight">
                    {year}년 {month + 1}월
                </h3>
                <div className="flex gap-2">
                    <button onClick={prevMonth} className="p-2 hover:bg-slate-100 rounded-xl transition-colors">
                        <ChevronLeft className="w-5 h-5 text-slate-400" />
                    </button>
                    <button onClick={nextMonth} className="p-2 hover:bg-slate-100 rounded-xl transition-colors">
                        <ChevronRight className="w-5 h-5 text-slate-400" />
                    </button>
                </div>
            </div>

            <div className="grid grid-cols-7 gap-2 mb-2">
                {['일', '월', '화', '수', '목', '금', '토'].map(d => (
                    <div key={d} className="text-center text-[10px] font-black text-slate-400 uppercase tracking-widest py-2">
                        {d}
                    </div>
                ))}
            </div>

            <div className="grid grid-cols-7 gap-3">
                {days.map((date, i) => {
                    if (!date) return <div key={`empty-${i}`} className="h-16" />;

                    const goal = getGoalForDate(date);
                    const isSelected = date.toISOString().split('T')[0] === selectedDate;
                    const isToday = date.toDateString() === today.toDateString();

                    return (
                        <button
                            key={i}
                            onClick={() => onSelectDate(date.toISOString().split('T')[0])}
                            className={clsx(
                                "h-16 rounded-2xl flex flex-col items-center justify-center relative transition-all duration-300 group overflow-hidden",
                                isSelected
                                    ? "bg-primary-600 text-white shadow-lg shadow-primary-600/30 scale-105"
                                    : "bg-slate-50 text-slate-600 hover:bg-white hover:shadow-xl hover:shadow-slate-200/50 border border-transparent hover:border-slate-200"
                            )}
                        >
                            <span className={clsx(
                                "text-sm font-bold z-10",
                                isToday && !isSelected && "text-primary-600"
                            )}>
                                {date.getDate()}
                            </span>

                            {goal && goal.achievementRate > 0 && (
                                <div className="mt-1 flex gap-0.5 z-10">
                                    {[...Array(Math.ceil(goal.achievementRate / 25))].map((_, idx) => (
                                        <div key={idx} className={clsx("w-1 h-1 rounded-full", isSelected ? "bg-white" : "bg-primary-500")} />
                                    ))}
                                </div>
                            )}

                            {isToday && (
                                <div className="absolute top-1 right-2 w-1.5 h-1.5 bg-primary-500 rounded-full" />
                            )}

                            {goal && goal.achievementRate === 100 && (
                                <div className="absolute -bottom-1 -right-1 opacity-20 group-hover:opacity-100 transition-opacity">
                                    <CheckCircle2 className={clsx("w-6 h-6", isSelected ? "text-white" : "text-green-500")} />
                                </div>
                            )}
                        </button>
                    );
                })}
            </div>
        </div>
    );
}
