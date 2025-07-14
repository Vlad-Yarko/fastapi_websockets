import BaseWebsocket from "../utils/baseWS";


class NotificationWebsocket extends BaseWebsocket {
    WEBSOCKET_ENDPOINT = "/ws/notifications"

    constructor(token, setNotifications) {
        super(token)

        this.setNotifications = setNotifications
    }

    handleJSON(event) {
        super.handleJSON(event)

        const data = JSON.parse(event.data)
        if (data.type === "notification") {
            this.setNotifications({shortMessage: data.shortMessage})
        }
    }
}


export default NotificationWebsocket
