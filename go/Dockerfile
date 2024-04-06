# Multi-stage build
# 1. Build stage
FROM golang:1.22.1 AS builder

WORKDIR /app

# Copy go mod and sum files
COPY go.mod go.sum ./

# Download dependencies
RUN go mod download

# Copy the source code into the container
COPY . .

# Build the Go app
RUN CGO_ENABLED=0 GOOS=linux go build -o app .

# 2. Production stage
FROM alpine:latest

WORKDIR /root/

# Copy the built executable from the builder stage
COPY --from=builder /app/app .

# Expose the port
EXPOSE 5555

# Command to run the executable
CMD ["./app"]
