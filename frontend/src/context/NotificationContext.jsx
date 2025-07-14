import { createContext, useState } from 'react'

const NotificationContext = createContext()

const NotificationContextProvider = ({ children }) => {
    const [ notifications, setNotifications ] = useState([])

	return (
		<NotificationContext.Provider
			value={{
                notifications, 
                setNotifications
			}}
		>
			{children}
		</NotificationContext.Provider>
	)
}

export { NotificationContext, NotificationContextProvider }
