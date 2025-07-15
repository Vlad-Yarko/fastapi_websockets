import { useContext, useEffect } from 'react'

import { NotificationContext } from '../../../context/NotificationContext'
import NotificationWebsocket from '../../../websockets/notificationWS'

// import './Home.css'


function Home() {
    const { notifications, setNotifications, unreadCount, setUnreadCount } = useContext(NotificationContext)

    useEffect(() => {
        const websocket = new NotificationWebsocket(
					'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3IiwiaWF0IjoxNzUyNTgyMDIyLCJleHAiOjE3NTI1ODI5MjJ9.HHU3ZRlRikAZ5RCRSX8Nexr0K8_Lg2Mj9bTrq273yKWg_ZrS-L0dZEgV_7cRqDQvFV1wzBAi4k-mfZvEsKinVRA9BipIKwfJqMo_Y5P8UY7gxRDnirdIXIdTiUE53liLKlkktGtCf1IbcEFVoy5MA8bXMe0cMdvK0ZSEQBA4cV2PwbAiY5glOjrMtLsoymYvAuXnxkZJ8nMtRJihr4VnSpsK726F1l71Yz-W_c-8ggc9azpIKfFAvHm8pnVtLt7u98tommVz6sfSJZ87-EVNtCqgT9tpGVoFv27Fn_XL4POm-xg68h7DyFqHUn7w3Ezw-eJa9d-MWjdKt-ufhhMOxQ',
					setNotifications
				)
        websocket.connect()

        return () => {
            websocket?.disconnect()
        }
    }, [])

    useEffect(() => {
        if (notifications.length >= 1) {
            setUnreadCount(count => count + 1)
        }
    }, [notifications])

    return (
			<>
				<div className='min-h-screen bg-gray-100'>
					<nav className='bg-white shadow-lg'>
						<div className='max-w-6xl mx-auto px-4'>
							<div className='flex justify-between items-center h-16'>
								<div className='text-xl font-semibold'>Notification Demo</div>
								<div className='relative'>
									<button
										id='notificationBell'
										className='relative p-2 hover:bg-gray-100 rounded-full'
									>
										<i className='fas fa-bell text-gray-600 text-xl'></i>
										<span
											id='notificationCount'
											className='absolute -top-1 -right-1 bg-red-500 text-white rounded-full w-5 h-5 flex items-center justify-center text-xs'
										>
											{unreadCount}
										</span>
									</button>
									<div
										id='notificationPanel'
										className='absolute right-0 mt-2 w-80 bg-white rounded-lg shadow-lg'
									>
										<div className='p-4'>
											<h3 className='text-lg font-semibold mb-2'>
												Notifications
											</h3>
											<div id='notificationList' className='space-y-2'>
												{notifications.length >= 1
													? notifications.map(element => (
															<div key={element.id} className='p-2 hover:bg-gray-50 rounded'>
																{element.shortMessage}
															</div>
                                                    ))
													: null}
											</div>
										</div>
									</div>
								</div>
							</div>
						</div>
					</nav>
					<div className='max-w-6xl mx-auto px-4 py-8'>
						<h1 className='text-2xl font-bold mb-4'>
							Welcome to the Notification System
						</h1>
						<p>
							Try sending a notification to see it appear in the bell above!
						</p>
					</div>
				</div>
			</>
		)
}


export default Home
