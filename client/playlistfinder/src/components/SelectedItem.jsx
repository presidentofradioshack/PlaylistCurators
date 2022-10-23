import React from 'react'

const SelectedItem = (props) => {
	return (
		<div>
			<ul className='my-6 flex flex-row justify-center'>
				{props.items.map(item => (
					<li key={item.id}>
						<p onClick={() => props.onSelectItem(item.id, item.name)} className='border border-gray-600 rounded-md px-4 py-2 text-gray-600 hover:bg-gray-800 hover:text-white cursor-pointer mx-5'>{item.name}</p>
					</li>
				))}
			</ul>
		</div>
	)
}

export default SelectedItem