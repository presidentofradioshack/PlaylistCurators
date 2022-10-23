import { Routes, Route } from 'react-router-dom'

import Home from './components/Home'

function App() {
	return (
		<div className='w-full min-h-full'>
			<Routes>
				<Route path='/' element={<Home />} />
			</Routes>
		</div>	
	)
}

export default App
