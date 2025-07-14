import API_DOMAIN from '../constants/api'


class BaseWebsocket {
    WEBSOCKET_ENDPOINT = "/ws"
    

    constructor(token) {
        this.websocket = null
        this.WEBSOCKET_PATH = `ws://${API_DOMAIN}${this.WEBSOCKET_ENDPOINT}?token=${token}`
    }

    connect(token) {
        this.websocket = new WebSocket(this.WEBSOCKET_PATH)

        this.websocket.onmessage = (event) => this.handleJSON(event)

        this.websocket.onclose = () => {

        }
        this.websocket.onerror = (error) => {
            this.ws?.close()
        }
    }

    handleJSON(event) {
        const data = JSON.parse(event.data)
        if (data.type == "ping") {
            this.ws?.send(JSON.stringify({type: "pong"}))
        }
    }

    disconnect() {
        this.ws?.close()
    }

}


export default BaseWebsocket
