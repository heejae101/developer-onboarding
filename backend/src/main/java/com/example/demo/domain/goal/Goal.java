package com.example.demo.domain.goal;

import com.example.demo.domain.user.User;
import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;

@Entity
@Table(name = "goals")
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class Goal {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne
    @JoinColumn(name = "user_id")
    private User user;

    private LocalDate date;

    private String mainGoal; // 오늘의 주요 목표

    private int achievementRate; // 0 ~ 100

    @OneToMany(mappedBy = "goal", cascade = CascadeType.ALL, orphanRemoval = true)
    @Builder.Default
    private List<Todo> todos = new ArrayList<>();

    public void calculateAchievementRate() {
        if (todos.isEmpty()) {
            achievementRate = 0;
            return;
        }
        long completedCount = todos.stream().filter(Todo::isCompleted).count();
        achievementRate = (int) ((completedCount * 100) / todos.size());
    }
}
