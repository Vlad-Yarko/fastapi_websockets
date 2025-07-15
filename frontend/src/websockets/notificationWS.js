import BaseWebsocket from "../utils/baseWS";


class NotificationWebsocket extends BaseWebsocket {

    constructor(token, setNotifications) {
        super(token, '/ws/notifications')

        this.setNotifications = setNotifications
    }

    handleJSON(event) {
        const data = JSON.parse(event.data)
        super.handleJSON(event, data)
        if (data.type === "notification") {
            this.setNotifications(prevNotifications => [data, ...prevNotifications])
        }
    }
}


export default NotificationWebsocket
