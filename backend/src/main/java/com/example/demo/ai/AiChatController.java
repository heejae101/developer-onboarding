package com.example.demo.ai;

import lombok.RequiredArgsConstructor;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Flux;

import java.util.Map;
import java.util.UUID;

@RestController
@RequestMapping("/api/ai")
@RequiredArgsConstructor
@CrossOrigin(origins = "*") // Allow frontend access
public class AiChatController {

    private final AgentWebSocketClient agentClient;

    @PostMapping(value = "/chat", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
    public Flux<String> chat(@RequestBody Map<String, String> request) {
        String message = request.get("message");
        String threadId = request.getOrDefault("thread_id", UUID.randomUUID().toString());
        // Simple User ID assumption (implement real auth later)
        Long userId = 1L;

        return agentClient.chatStream(message, threadId, userId);
    }
}
