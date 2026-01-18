import React, { useState, useEffect } from 'react';
import { Plus, Trash2, Check, Target, Circle, CheckCircle2 } from 'lucide-react';
import { clsx } from 'clsx';

export default function GoalTracker({ date, initialGoal, onSave }) {
    const [mainGoal, setMainGoal] = useState(initialGoal?.mainGoal || '');
    const [todos, setTodos] = useState(initialGoal?.todos || []);
    const [newTodo, setNewTodo] = useState('');

    useEffect(() => {
        setMainGoal(initialGoal?.mainGoal || '');
        setTodos(initialGoal?.todos || []);
    }, [initialGoal, date]);

    const handleAddTodo = (e) => {
        e.preventDefault();
        if (!newTodo.trim()) return;
        setTodos([...todos, { content: newTodo, isCompleted: false }]);
        setNewTodo('');
    };

    const toggleTodo = (index) => {
        const newTodos = [...todos];
        newTodos[index].isCompleted = !newTodos[index].isCompleted;
        setTodos(newTodos);
    };

    const removeTodo = (index) => {
        setTodos(todos.filter((_, i) => i !== index));
    };

    const handleSave = () => {
        onSave(date, mainGoal, todos);
    };

    return (
        <div className="bg-white rounded-[40px] p-8 shadow-sm border border-slate-100 ring-1 ring-slate-200/50 flex flex-col gap-8 h-full animate-in slide-in-from-right-4 duration-500">
            <div className="flex items-center justify-between">
                <div>
                    <h3 className="text-2xl font-black text-slate-900 tracking-tight mb-1">{date}</h3>
                    <p className="text-xs font-bold text-slate-400 uppercase tracking-widest">Daily Goals & Checklist</p>
                </div>
                <button
                    onClick={handleSave}
                    className="bg-primary-600 text-white px-6 py-3 rounded-2xl font-bold hover:bg-primary-700 transition-all shadow-lg shadow-primary-600/20 active:scale-95"
                >
                    저장하기
                </button>
            </div>

            <div className="space-y-6">
                {/* Main Goal Section */}
                <div className="space-y-3">
                    <label className="flex items-center gap-2 text-sm font-black text-slate-700 uppercase">
                        <Target className="w-4 h-4 text-primary-500" />
                        오늘의 핵심 목표
                    </label>
                    <input
                        type="text"
                        placeholder="오늘 꼭 이루고 싶은 한 가지를 적어보세요."
                        className="w-full bg-slate-50 border-none rounded-2xl px-5 py-4 text-base focus:ring-4 focus:ring-primary-500/10 focus:bg-white transition-all font-medium text-slate-800"
                        value={mainGoal}
                        onChange={(e) => setMainGoal(e.target.value)}
                    />
                </div>

                {/* Todo List Section */}
                <div className="space-y-4">
                    <label className="flex items-center gap-2 text-sm font-black text-slate-700 uppercase">
                        <Plus className="w-4 h-4 text-primary-500" />
                        세부 할 일 목록
                    </label>

                    <form onSubmit={handleAddTodo} className="flex gap-2">
                        <input
                            type="text"
                            placeholder="할 일을 입력하고 Enter를 누르세요."
                            className="flex-1 bg-slate-50 border-none rounded-2xl px-5 py-3 text-sm focus:ring-4 focus:ring-primary-500/10 focus:bg-white transition-all"
                            value={newTodo}
                            onChange={(e) => setNewTodo(e.target.value)}
                        />
                    </form>

                    <div className="space-y-2 mt-2 max-h-[300px] overflow-y-auto pr-2 custom-scrollbar">
                        {todos.map((todo, index) => (
                            <div
                                key={index}
                                className={clsx(
                                    "group flex items-center justify-between p-4 rounded-2xl border transition-all duration-300",
                                    todo.isCompleted
                                        ? "bg-slate-50 border-transparent opacity-60"
                                        : "bg-white border-slate-100 hover:border-slate-300"
                                )}
                            >
                                <div
                                    className="flex items-center gap-3 flex-1 cursor-pointer"
                                    onClick={() => toggleTodo(index)}
                                >
                                    {todo.isCompleted ? (
                                        <CheckCircle2 className="w-5 h-5 text-green-500 shrink-0" />
                                    ) : (
                                        <Circle className="w-5 h-5 text-slate-300 group-hover:text-primary-400 shrink-0 transition-colors" />
                                    )}
                                    <span className={clsx(
                                        "text-sm font-medium transition-all",
                                        todo.isCompleted ? "text-slate-400 line-through" : "text-slate-700"
                                    )}>
                                        {todo.content}
                                    </span>
                                </div>
                                <button
                                    onClick={() => removeTodo(index)}
                                    className="p-1.5 text-slate-300 hover:text-rose-500 bg-transparent hover:bg-rose-50 rounded-lg opacity-0 group-hover:opacity-100 transition-all"
                                >
                                    <Trash2 className="w-4 h-4" />
                                </button>
                            </div>
                        ))}
                        {todos.length === 0 && (
                            <div className="py-12 text-center bg-slate-50/50 rounded-3xl border border-dashed border-slate-200">
                                <p className="text-slate-400 text-sm font-bold uppercase tracking-tight">지정된 할 일이 없습니다.</p>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}
