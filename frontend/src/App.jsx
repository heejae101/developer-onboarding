import React, { useState, useEffect } from 'react';
import { Header, MainLayout } from './shared/components/layout/Layout';
import GuideCard from './features/study/GuideCard';
import GuideViewer from './features/study/GuideViewer';
import MapView from './features/map/MapView';
import ChatWidget from './features/chat/ChatWidget';
import GoalCalendar from './features/goal/GoalCalendar';
import GoalTracker from './features/goal/GoalTracker';
import { useGoalStore } from './features/goal/goalStore';
import { clsx } from 'clsx';
import { Filter, Zap, BookOpen, HelpCircle, Map as MapIcon, Target } from 'lucide-react';

function App() {
  const [guides, setGuides] = useState([]);
  const [filteredGuides, setFilteredGuides] = useState([]);
  const [selectedGuideId, setSelectedGuideId] = useState(null);
  const [activeCategory, setActiveCategory] = useState('전체');
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(true);

  // Goal 관련 상태
  const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0]);
  const { goals, fetchGoals, saveGoal } = useGoalStore();

  const categories = [
    { name: '전체', icon: <Zap className="w-4 h-4" /> },
    { name: '개발 공부', icon: <BookOpen className="w-4 h-4" /> },
    { name: '스스로 질문', icon: <HelpCircle className="w-4 h-4" /> },
    { name: '지도 예시', icon: <MapIcon className="w-4 h-4" /> },
    { name: '하루 목표', icon: <Target className="w-4 h-4" /> },
  ];

  useEffect(() => {
    fetch('http://localhost:8080/api/guides')
      .then(res => res.json())
      .then(data => {
        setGuides(data);
        setFilteredGuides(data);
        setLoading(false);
      })
      .catch(err => {
        console.error('API Error:', err);
        setLoading(false);
      });
  }, []);

  useEffect(() => {
    let result = guides;

    if (activeCategory !== '전체') {
      result = result.filter(g => g.category === activeCategory);
    }

    if (searchTerm) {
      result = result.filter(g =>
        g.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        g.content.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    setFilteredGuides(result);
  }, [activeCategory, searchTerm, guides]);

  const selectedGuide = guides.find(g => g.id === selectedGuideId);
  const selectedGoal = goals.find(g => g.date === selectedDate);

  const handleSaveGoal = async (date, mainGoal, todos) => {
    await saveGoal(date, mainGoal, todos);
    alert('오늘의 목표가 저장되었습니다! 🎯');
  };

  return (
    <MainLayout
      header={
        <Header
          searchTerm={searchTerm}
          onSearch={setSearchTerm}
        />
      }
    >
      <div className="flex flex-col gap-10">
        {!selectedGuideId && (
          <>
            {/* Hero Section */}
            <div className="bg-primary-600 rounded-[40px] p-12 text-white relative overflow-hidden shadow-2xl shadow-primary-600/30">
              <div className="relative z-10 max-w-2xl">
                <h1 className="text-4xl md:text-5xl font-black mb-6 leading-tight">
                  성장을 위한 기록,<br />그 이상의 가치.
                </h1>
                <p className="text-primary-100 text-lg mb-8 leading-relaxed font-medium">
                  신입 개발자의 온보딩 과정부터 매일의 치열한 고민까지,<br />
                  도메인별로 정리된 실무 지식과 회고를 만나보세요.
                </p>
                <div className="flex gap-4">
                  <button
                    onClick={() => setActiveCategory('하루 목표')}
                    className="bg-white text-primary-600 px-8 py-3 rounded-2xl font-bold hover:bg-slate-100 transition-colors shadow-lg shadow-black/10"
                  >
                    목표 달성하러 가기
                  </button>
                  <button className="bg-primary-500 text-white px-8 py-3 rounded-2xl font-bold hover:bg-primary-400 transition-colors border border-primary-400">
                    둘러보기
                  </button>
                </div>
              </div>
              <div className="absolute right-[-10%] top-[-10%] w-[50%] h-[120%] bg-white/10 rounded-full blur-3xl" />
              <div className="absolute left-[40%] bottom-[-20%] w-[30%] h-[80%] bg-indigo-500/20 rounded-full blur-3xl" />
            </div>

            {/* Category Filter */}
            <section className="flex flex-col gap-6">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div className="p-2 bg-slate-100 rounded-xl">
                    <Filter className="w-5 h-5 text-slate-600" />
                  </div>
                  <h2 className="text-xl font-black text-slate-900 uppercase tracking-tight">도메인 카테고리</h2>
                </div>
                <span className="text-sm font-bold text-slate-400 uppercase tracking-widest">
                  {activeCategory === '하루 목표' ? 'Goal Tracker Active' : `${filteredGuides.length} POSTS FOUND`}
                </span>
              </div>

              <div className="flex flex-wrap gap-3">
                {categories.map((cat) => (
                  <button
                    key={cat.name}
                    onClick={() => setActiveCategory(cat.name)}
                    className={clsx(
                      "flex items-center gap-2.5 px-6 py-3 rounded-2xl font-bold transition-all duration-300 border shadow-sm",
                      activeCategory === cat.name
                        ? "bg-slate-900 border-slate-900 text-white shadow-xl shadow-slate-900/10 scale-105"
                        : "bg-white border-slate-200 text-slate-500 hover:border-primary-500 hover:text-primary-600"
                    )}
                  >
                    {cat.icon}
                    {cat.name}
                  </button>
                ))}
              </div>
            </section>

            {/* Content List Grouped by Domain */}
            <div className="animate-in fade-in slide-in-from-bottom-4 duration-700">
              {(() => {
                switch (activeCategory) {
                  case '지도 예시':
                    return <MapView />;
                  case '하루 목표':
                    return (
                      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 h-full">
                        <div className="lg:col-span-5">
                          <GoalCalendar
                            goals={goals}
                            selectedDate={selectedDate}
                            onSelectDate={setSelectedDate}
                          />
                        </div>
                        <div className="lg:col-span-7">
                          <GoalTracker
                            date={selectedDate}
                            initialGoal={selectedGoal}
                            onSave={handleSaveGoal}
                          />
                        </div>
                      </div>
                    );
                  default:
                    return (
                      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                        {filteredGuides.map((guide) => (
                          <GuideCard
                            key={guide.id}
                            guide={guide}
                            onSelect={setSelectedGuideId}
                          />
                        ))}
                        {filteredGuides.length === 0 && !loading && (
                          <div className="col-span-full py-32 text-center bg-white rounded-[40px] border border-dashed border-slate-200">
                            <p className="text-slate-400 font-bold text-xl uppercase tracking-tighter mb-2">NO RESULTS FOUND</p>
                            <p className="text-slate-500">다른 검색어나 카테고리를 선택해 보세요.</p>
                          </div>
                        )}
                      </div>
                    );
                }
              })()}
            </div>
          </>
        )}

        {selectedGuideId && (
          <GuideViewer
            guide={selectedGuide}
            onBack={() => setSelectedGuideId(null)}
          />
        )}
      </div>

      <ChatWidget />
    </MainLayout>
  );
}

export default App;
