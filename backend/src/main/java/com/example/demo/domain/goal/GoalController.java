package com.example.demo.domain.goal;

import com.example.demo.domain.user.User;
import com.example.demo.domain.user.UserRepository;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDate;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/goals")
@RequiredArgsConstructor
@CrossOrigin(origins = "*")
@Tag(name = "Goal API", description = "일일 목표 및 할 일 관리 API")
public class GoalController {

    private final GoalRepository goalRepository;
    private final UserRepository userRepository;
    private final TodoRepository todoRepository;

    @GetMapping("/me")
    @Operation(summary = "내 목표 목록 조회", description = "사용자의 전체 일일 목표 및 달성도 목록을 조회합니다.")
    public List<Goal> getMyGoals(@RequestParam(defaultValue = "admin") String username) {
        User user = getOrCreateUser(username);
        return goalRepository.findByUserAndDateBetween(
                user,
                LocalDate.now().minusMonths(3),
                LocalDate.now().plusMonths(1));
    }

    @PostMapping("/save")
    @Operation(summary = "목표 및 할 일 저장", description = "특정 날짜의 목표와 할 일 목록을 저장하거나 수정합니다.")
    public Goal saveGoal(@RequestBody Map<String, Object> payload) {
        String username = (String) payload.getOrDefault("username", "admin");
        User user = getOrCreateUser(username);

        LocalDate date = LocalDate.parse((String) payload.get("date"));
        String mainGoal = (String) payload.get("mainGoal");
        List<Map<String, Object>> todoData = (List<Map<String, Object>>) payload.get("todos");

        Goal goal = goalRepository.findByUserAndDate(user, date)
                .orElse(Goal.builder().user(user).date(date).build());

        goal.setMainGoal(mainGoal);
        goalRepository.save(goal); // ID 확보를 위해 먼저 저장

        // 기존 Todo 삭제 후 재생성 (간단한 구현)
        if (goal.getId() != null) {
            goal.getTodos().clear();
        }

        if (todoData != null) {
            for (Map<String, Object> t : todoData) {
                Todo todo = Todo.builder()
                        .goal(goal)
                        .content((String) t.get("content"))
                        .isCompleted((Boolean) t.get("isCompleted"))
                        .build();
                goal.getTodos().add(todo);
            }
        }

        goal.calculateAchievementRate();
        return goalRepository.save(goal);
    }

    private User getOrCreateUser(String username) {
        return userRepository.findByUsername(username)
                .orElseGet(() -> userRepository.save(User.builder()
                        .username(username)
                        .nickname("주니어 개발자")
                        .password("1234")
                        .build()));
    }
}
