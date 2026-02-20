#ifndef PING_PROTOCOL_H
#define PING_PROTOCOL_H

#include <stdint.h>

typedef struct PingRequest {
    uint32_t id;
    char body[32];
} PingRequest;

typedef struct PingResponse {
    uint32_t id;
    uint8_t ok;
} PingResponse;

#endif
