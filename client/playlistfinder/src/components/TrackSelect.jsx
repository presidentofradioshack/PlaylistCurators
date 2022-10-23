import React from 'react'
import { truncate } from '../constants/util'

const TrackSelect = (props) => {
	return (
		<div className='p-3 w-full'>
			<ul className='flex flex-row'>
				{props.tracks.map(track => (
					<li key={track.id} className='w-1/5 mx-3'>
						<div onClick={() => props.onSelectTrack(track.id, track.name)} className='ease-in-out duration-300 bg-gray-800 text-white font-almanach p-3 rounded-md cursor-pointer hover:bg-gray-700'>
							<img src={track.album.images[0] ? track.album.images[0].url : ''} alt={`${track.name}`} className='w-full h-36 object-cover rounded-md mb-5' />

							<p className='mb-2'>{truncate(track.name, 17)}</p>
							<p className='text-gray-600'>{truncate(track.artists[0].name, 16)}</p>
						</div>
					</li>
				))}
			</ul>
		</div>
	)
}

export default TrackSelect