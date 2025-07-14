import { useContext, useEffect } from 'react'

import { NotificationContext } from '../../../context/NotificationContext'

// import './Home.css'


function Home() {
    const { notifications, setNotifications } = useContext(NotificationContext)

    useEffect(() => {
        const websocket = NotificationWebsocket(
            '',
            setNotifications
        )
        websocket.connect()
        
        return () => {
            websocket?.disconnect()
        }
    }, [])

    return (
            <div className="min-h-screen bg-gray-100">
                <nav className="bg-white shadow-lg">
                    <div className="max-w-6xl mx-auto px-4">
                        <div className="flex justify-between items-center h-16">
                            <div className="text-xl font-semibold">Notification Demo</div>
                            <div className="relative">
                                <button id="notificationBell" className="relative p-2 hover:bg-gray-100 rounded-full">
                                    <i className="fas fa-bell text-gray-600 text-xl"></i>
                                    <span id="notificationCount" className="hidden absolute -top-1 -right-1 bg-red-500 text-white rounded-full w-5 h-5 flex items-center justify-center text-xs">
                                        0
                                    </span>
                                </button>
                                <div id="notificationPanel" className="hidden absolute right-0 mt-2 w-80 bg-white rounded-lg shadow-lg">
                                    <div className="p-4">
                                        <h3 className="text-lg font-semibold mb-2">Notifications</h3>
                                        <ul id="notificationList" className="space-y-2">
                                            {notifications.length >= 1 ?
                                            notifications.map(element => <li key={element.id}>{element.shortMessage}</li>) :
                                            null}                                       
                                        </ul>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </nav>
                <div className="max-w-6xl mx-auto px-4 py-8">
                    <h1 className="text-2xl font-bold mb-4">Welcome to the Notification System</h1>
                    <p>Try sending a notification to see it appear in the bell above!</p>
                </div>
            </div>
    )
}


export default Home
