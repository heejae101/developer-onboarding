package com.example.demo.ai;

import org.springframework.stereotype.Service;
import org.springframework.web.reactive.socket.WebSocketMessage;
import org.springframework.web.reactive.socket.client.ReactorNettyWebSocketClient;
import org.springframework.web.reactive.socket.client.WebSocketClient;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Sinks;

import java.net.URI;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.util.Map;

@Service
public class AgentWebSocketClient {

    private final WebSocketClient client = new ReactorNettyWebSocketClient();
    private final ObjectMapper objectMapper = new ObjectMapper();

    public Flux<String> chatStream(String message, String threadId, Long userId) {
        URI uri = URI.create("ws://localhost:8000/ws/ai-stream");

        // Create a sink for this request to buffer responses
        Sinks.Many<String> sink = Sinks.many().unicast().onBackpressureBuffer();

        client.execute(uri, session -> {
            try {
                // Prepare request message
                Map<String, Object> payload = Map.of(
                        "message", message,
                        "thread_id", threadId,
                        "user_id", userId);
                String jsonPayload = objectMapper.writeValueAsString(payload);

                // Send message
                return session.send(
                        Flux.just(session.textMessage(jsonPayload))).thenMany(
                                // Receive messages
                                session.receive()
                                        .map(WebSocketMessage::getPayloadAsText)
                                        .doOnNext(sink::tryEmitNext)
                                        .doOnComplete(sink::tryEmitComplete)
                                        .doOnError(sink::tryEmitError))
                        .then();
            } catch (Exception e) {
                sink.tryEmitError(e);
                return session.close();
            }
        }).subscribe(
                null,
                sink::tryEmitError, // Propagate connection errors to the sink
                null);

        return sink.asFlux();
    }
}
