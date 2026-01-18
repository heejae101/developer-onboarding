import { useState, useEffect } from 'react';

export function useGoalStore(username = 'admin') {
    const [goals, setGoals] = useState([]);
    const [loading, setLoading] = useState(false);

    const fetchGoals = async () => {
        setLoading(true);
        try {
            const res = await fetch(`http://localhost:8080/api/goals/me?username=${username}`);
            const data = await res.json();
            setGoals(data);
        } catch (err) {
            console.error('Failed to fetch goals:', err);
        } finally {
            setLoading(false);
        }
    };

    const saveGoal = async (date, mainGoal, todos) => {
        try {
            const res = await fetch('http://localhost:8080/api/goals/save', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, date, mainGoal, todos })
            });
            const data = await res.json();
            // Update local state
            setGoals(prev => {
                const index = prev.findIndex(g => g.date === date);
                if (index > -1) {
                    const newGoals = [...prev];
                    newGoals[index] = data;
                    return newGoals;
                }
                return [...prev, data];
            });
            return data;
        } catch (err) {
            console.error('Failed to save goal:', err);
            throw err;
        }
    };

    useEffect(() => {
        fetchGoals();
    }, [username]);

    return { goals, loading, fetchGoals, saveGoal };
}
