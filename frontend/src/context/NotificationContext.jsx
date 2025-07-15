import { createContext, useState } from 'react'

const NotificationContext = createContext()

const NotificationContextProvider = ({ children }) => {
    const [ notifications, setNotifications ] = useState([])
	const [ unreadCount, setUnreadCount ] = useState(0)

	return (
		<NotificationContext.Provider
			value={{
                notifications, 
                setNotifications,
				unreadCount,
				setUnreadCount
			}}
		>
			{children}
		</NotificationContext.Provider>
	)
}

export { NotificationContext, NotificationContextProvider }
