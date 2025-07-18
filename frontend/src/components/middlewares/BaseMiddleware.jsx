import { Outlet } from 'react-router-dom'

import { NotificationContextProvider } from '../../context/NotificationContext'


function BaseMiddleware() {
	return (
		<NotificationContextProvider>
			<Outlet />
		</NotificationContextProvider>
	)
}


export default BaseMiddleware
