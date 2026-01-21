/**
 * AI API Client
 * Handles communication with the AI Agent backend
 */
import { fetchEventSource } from '@microsoft/fetch-event-source';

// Base URL for API - should be configured via env vars in production
const API_BASE_URL = 'http://localhost:8080/api/ai';

/**
 * Stream chat response from AI Agent
 * @param {Object} params Request parameters
 * @param {string} params.message User's message
 * @param {string} params.threadId Thread ID for conversation context
 * @param {Function} params.onMessage Callback for receiving message tokens
 * @param {Function} params.onError Callback for handling errors
 * @param {Function} params.onComplete Callback when stream completes
 * @param {AbortController} params.controller AbortController for cancelling request
 */
export const streamChat = async ({
    message,
    threadId,
    onMessage,
    onError,
    onComplete,
    controller
}) => {
    try {
        await fetchEventSource(`${API_BASE_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message,
                thread_id: threadId
            }),
            signal: controller?.signal,

            async onopen(response) {
                if (response.ok) {
                    return; // Connection established
                } else if (response.status >= 400 && response.status < 500 && response.status !== 429) {
                    // Client-side errors (except rate limit) are fatal
                    throw new Error(`Client error: ${response.status}`);
                } else {
                    // Server-side errors can be retried (default behavior)
                    // But for chat, we might want to fail fast
                    throw new Error(`Server error: ${response.status}`);
                }
            },

            onmessage(msg) {
                // If the server sends a message
                if (msg.event === 'close') {
                    onComplete?.();
                } else {
                    // msg.data contains the text token
                    try {
                        // Sometimes data might be JSON if structured
                        const data = msg.data;
                        onMessage(data);
                    } catch (e) {
                        onMessage(msg.data);
                    }
                }
            },

            onclose() {
                onComplete?.();
            },

            onerror(err) {
                onError?.(err);
                throw err; // Configuring retry behavior or rethrowing
            }
        });
    } catch (err) {
        if (err.name !== 'AbortError') {
            onError?.(err);
        }
    }
};
