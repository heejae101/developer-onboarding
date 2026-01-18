package com.example.demo.domain.goal;

import com.example.demo.domain.user.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.time.LocalDate;
import java.util.List;
import java.util.Optional;

@Repository
public interface GoalRepository extends JpaRepository<Goal, Long> {
    Optional<Goal> findByUserAndDate(User user, LocalDate date);

    List<Goal> findByUserAndDateBetween(User user, LocalDate startDate, LocalDate endDate);
}
