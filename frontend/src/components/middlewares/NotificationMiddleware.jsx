import { Outlet } from 'react-router-dom'


function BaseMiddleware() {

	return (
		<NotificationContextProvider>
			<Outlet />
		</NotificationContextProvider>
	)
}

export default BaseMiddleware
