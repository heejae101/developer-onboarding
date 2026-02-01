import { useState, useEffect } from 'react';
import {
    Settings,
    RefreshCw,
    Zap,
    Star,
    UserCheck,
    FileText,
    Activity,
    Save,
    RotateCcw,
    Sliders
} from 'lucide-react';
import './AdminSettings.css';

const API_BASE = 'http://localhost:8000/api/v1';

export default function AdminSettings() {
    const [settings, setSettings] = useState(null);
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [graphVisualization, setGraphVisualization] = useState(null);

    useEffect(() => {
        fetchSettings();
    }, []);

    const fetchSettings = async () => {
        try {
            const response = await fetch(`${API_BASE}/admin/graph-settings`);
            const data = await response.json();
            setSettings(data);
            fetchVisualization();
        } catch (error) {
            console.error('Failed to fetch settings:', error);
        } finally {
            setLoading(false);
        }
    };

    const fetchVisualization = async () => {
        try {
            const response = await fetch(`${API_BASE}/admin/graph-visualization`);
            const data = await response.json();
            setGraphVisualization(data);
        } catch (error) {
            console.error('Failed to fetch visualization:', error);
        }
    };

    const saveSettings = async () => {
        setSaving(true);
        try {
            const response = await fetch(`${API_BASE}/admin/graph-settings`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(settings),
            });
            if (response.ok) {
                await fetchVisualization();
                alert('설정이 저장되었습니다!');
            }
        } catch (error) {
            console.error('Failed to save settings:', error);
            alert('저장 실패');
        } finally {
            setSaving(false);
        }
    };

    const resetSettings = async () => {
        if (!confirm('설정을 기본값으로 초기화하시겠습니까?')) return;

        try {
            const response = await fetch(`${API_BASE}/admin/graph-settings/reset`, {
                method: 'POST',
            });
            const data = await response.json();
            setSettings(data);
            fetchVisualization();
        } catch (error) {
            console.error('Failed to reset settings:', error);
        }
    };

    const handleToggle = (key) => {
        setSettings(prev => ({ ...prev, [key]: !prev[key] }));
    };

    const handleNumber = (key, value) => {
        setSettings(prev => ({ ...prev, [key]: parseFloat(value) }));
    };

    if (loading) {
        return <div className="admin-loading">로딩 중...</div>;
    }

    return (
        <div className="admin-settings">
            <header className="admin-header">
                <h1>
                    <Sliders className="header-icon" />
                    <span>에이전트 그래프 설정</span>
                </h1>
                <p>LangGraph 패턴을 ON/OFF하여 에이전트 동작 방식을 조정합니다.</p>
            </header>

            <div className="admin-content">
                <div className="settings-grid">

                    {/* Self-RAG Pattern */}
                    <div className={`setting-card ${settings.enable_self_rag ? 'active' : ''}`}>
                        <div className="card-header">
                            <div className="card-title">
                                <RefreshCw className="card-icon" />
                                <h3>Self-RAG</h3>
                            </div>
                            <label className="toggle">
                                <input
                                    type="checkbox"
                                    checked={settings.enable_self_rag}
                                    onChange={() => handleToggle('enable_self_rag')}
                                />
                                <span className="slider"></span>
                            </label>
                        </div>
                        <p className="card-description">
                            검색 결과의 관련성을 평가하고, 부족하면 재검색합니다.
                        </p>
                        {settings.enable_self_rag && (
                            <div className="card-options">
                                <div className="option-row">
                                    <label>최대 재검색 횟수</label>
                                    <input
                                        type="number"
                                        min="1"
                                        max="5"
                                        value={settings.max_search_retries}
                                        onChange={(e) => handleNumber('max_search_retries', e.target.value)}
                                    />
                                </div>
                                <div className="option-row">
                                    <label>관련성 임계값</label>
                                    <input
                                        type="range"
                                        min="0"
                                        max="1"
                                        step="0.1"
                                        value={settings.relevance_threshold}
                                        onChange={(e) => handleNumber('relevance_threshold', e.target.value)}
                                    />
                                    <span>{settings.relevance_threshold}</span>
                                </div>
                            </div>
                        )}
                    </div>

                    {/* Parallel Search Pattern */}
                    <div className={`setting-card ${settings.enable_parallel_search ? 'active' : ''}`}>
                        <div className="card-header">
                            <div className="card-title">
                                <Zap className="card-icon" />
                                <h3>병렬 검색</h3>
                            </div>
                            <label className="toggle">
                                <input
                                    type="checkbox"
                                    checked={settings.enable_parallel_search}
                                    onChange={() => handleToggle('enable_parallel_search')}
                                />
                                <span className="slider"></span>
                            </label>
                        </div>
                        <p className="card-description">
                            RAG + 파일 검색을 동시에 실행하여 더 풍부한 컨텍스트를 확보합니다.
                        </p>
                    </div>

                    {/* Answer Grading Pattern */}
                    <div className={`setting-card ${settings.enable_answer_grading ? 'active' : ''}`}>
                        <div className="card-header">
                            <div className="card-title">
                                <Star className="card-icon" />
                                <h3>답변 품질 평가</h3>
                            </div>
                            <label className="toggle">
                                <input
                                    type="checkbox"
                                    checked={settings.enable_answer_grading}
                                    onChange={() => handleToggle('enable_answer_grading')}
                                />
                                <span className="slider"></span>
                            </label>
                        </div>
                        <p className="card-description">
                            생성된 답변의 품질을 평가하고, 낮으면 개선합니다.
                        </p>
                        {settings.enable_answer_grading && (
                            <div className="card-options">
                                <div className="option-row">
                                    <label>최소 품질 점수</label>
                                    <input
                                        type="range"
                                        min="0"
                                        max="1"
                                        step="0.1"
                                        value={settings.min_answer_score}
                                        onChange={(e) => handleNumber('min_answer_score', e.target.value)}
                                    />
                                    <span>{settings.min_answer_score}</span>
                                </div>
                                <div className="option-row">
                                    <label>최대 개선 횟수</label>
                                    <input
                                        type="number"
                                        min="1"
                                        max="5"
                                        value={settings.max_refine_attempts}
                                        onChange={(e) => handleNumber('max_refine_attempts', e.target.value)}
                                    />
                                </div>
                            </div>
                        )}
                    </div>

                    {/* Human-in-the-loop Pattern */}
                    <div className={`setting-card ${settings.enable_human_approval ? 'active' : ''}`}>
                        <div className="card-header">
                            <div className="card-title">
                                <UserCheck className="card-icon" />
                                <h3>사용자 확인</h3>
                            </div>
                            <label className="toggle">
                                <input
                                    type="checkbox"
                                    checked={settings.enable_human_approval}
                                    onChange={() => handleToggle('enable_human_approval')}
                                />
                                <span className="slider"></span>
                            </label>
                        </div>
                        <p className="card-description">
                            중요한 결정에서 사용자 승인을 요청합니다.
                        </p>
                    </div>

                    {/* Step Logging */}
                    <div className={`setting-card ${settings.enable_step_logging ? 'active' : ''}`}>
                        <div className="card-header">
                            <div className="card-title">
                                <FileText className="card-icon" />
                                <h3>스텝 로깅</h3>
                            </div>
                            <label className="toggle">
                                <input
                                    type="checkbox"
                                    checked={settings.enable_step_logging}
                                    onChange={() => handleToggle('enable_step_logging')}
                                />
                                <span className="slider"></span>
                            </label>
                        </div>
                        <p className="card-description">
                            각 노드 실행 시 로그를 출력합니다.
                        </p>
                    </div>
                </div>

                {/* Graph Visualization */}
                {graphVisualization && (
                    <div className="graph-visualization">
                        <h2>
                            <Activity className="inline-icon" />
                            <span>현재 그래프 구조</span>
                        </h2>
                        <div className="active-patterns">
                            {Object.entries(graphVisualization.active_patterns).map(([key, value]) => (
                                <span key={key} className={`pattern-badge ${value ? 'on' : 'off'}`}>
                                    {key.replace('_', ' ')}: {value ? 'ON' : 'OFF'}
                                </span>
                            ))}
                        </div>
                        <pre className="mermaid-code">{graphVisualization.mermaid}</pre>
                    </div>
                )}

                {/* Action Buttons */}
                <div className="action-buttons">
                    <button
                        className="btn btn-primary flex items-center gap-2 justify-center"
                        onClick={saveSettings}
                        disabled={saving}
                    >
                        <Save size={18} />
                        <span>Settings Saved</span>
                    </button>
                    <button
                        className="btn btn-secondary flex items-center gap-2 justify-center"
                        onClick={resetSettings}
                    >
                        <RotateCcw size={18} />
                        <span>Reset Defaults</span>
                    </button>
                </div>
            </div>
        </div>
    );
}
