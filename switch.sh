#!/bin/bash
set -e

BLUE_URL="http://localhost:8001"
GREEN_URL="http://localhost:8002"

check_health() {
    local url=$1
    local version=$2
    local response
    response=$(curl -s "$url/health" 2>/dev/null)
    local status
    status=$(echo "$response" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('status',''))" 2>/dev/null)
    if [ "$status" = "ok" ]; then
        echo "Health OK: $url ($version)"
        return 0
    else
        echo "Health FAILED: $url"
        return 1
    fi
}

switch_to_green() {
    echo "Checking green health before switching..."
    if ! check_health "$GREEN_URL" "v1.1.0"; then
        echo "Green is not healthy. Rollback to blue."
        switch_to_blue
        exit 1
    fi
    echo "Switching traffic to green..."
    docker compose -f docker-compose.green.yml up -d nginx
    echo "Traffic now on green (v1.1.0)"
}

switch_to_blue() {
    echo "Rolling back to blue (v1.0.0)..."
    docker compose -f docker-compose.blue.yml up -d nginx
    echo "Traffic now on blue (v1.0.0)"
}

case "${1:-}" in
    green)
        switch_to_green
        ;;
    blue|rollback)
        switch_to_blue
        ;;
    status)
        check_health "$BLUE_URL" "v1.0.0" || true
        check_health "$GREEN_URL" "v1.1.0" || true
        ;;
    *)
        echo "Usage: $0 {green|blue|rollback|status}"
        exit 1
        ;;
esac
