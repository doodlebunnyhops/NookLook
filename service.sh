#!/bin/bash

# Bot Service Management Script

SERVICE_NAME="Bot"
SERVICE_FILE="/Path/To/NookLook/bot.service"
SYSTEMD_PATH="/etc/systemd/system/${SERVICE_NAME}.service"

case "$1" in
    install)
        echo "Installing Bot systemd service..."
        sudo cp "$SERVICE_FILE" "$SYSTEMD_PATH"
        sudo systemctl daemon-reload
        sudo systemctl enable "$SERVICE_NAME"
        echo "Service installed and enabled!"
        echo "Use './service.sh start' to start the service"
        ;;
    start)
        echo "Starting Bot service..."
        sudo systemctl start "$SERVICE_NAME"
        sudo systemctl status "$SERVICE_NAME"
        ;;
    stop)
        echo "Stopping Bot service..."
        sudo systemctl stop "$SERVICE_NAME"
        ;;
    restart)
        echo "Restarting Bot service..."
        sudo systemctl restart "$SERVICE_NAME"
        sudo systemctl status "$SERVICE_NAME"
        ;;
    status)
        sudo systemctl status "$SERVICE_NAME"
        ;;
    logs)
        sudo journalctl -u "$SERVICE_NAME" -f
        ;;
    uninstall)
        echo "Uninstalling NookLook service..."
        sudo systemctl stop "$SERVICE_NAME"
        sudo systemctl disable "$SERVICE_NAME"
        sudo rm "$SYSTEMD_PATH"
        sudo systemctl daemon-reload
        echo "Service uninstalled!"
        ;;
    *)
        echo "Usage: $0 {install|start|stop|restart|status|logs|uninstall}"
        echo ""
        echo "Commands:"
        echo "  install   - Install and enable the systemd service"
        echo "  start     - Start the service"
        echo "  stop      - Stop the service"
        echo "  restart   - Restart the service"
        echo "  status    - Show service status"
        echo "  logs      - Follow service logs"
        echo "  uninstall - Remove the service"
        exit 1
        ;;
esac