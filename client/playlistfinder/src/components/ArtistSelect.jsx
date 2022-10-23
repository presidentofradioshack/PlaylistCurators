import React from 'react'
import { truncate } from '../constants/util'

const ArtistSelect = (props) => {
	return (
		<div className='p-3 w-full'>
			<ul className='flex flex-row'>
				{props.artists.map(artist => (
					<li key={artist.id} className='w-1/5 mx-3'>
						<div onClick={() => props.onSelectArtist(artist.id, artist.name)} className='ease-in-out duration-300 bg-gray-800 text-white font-almanach p-3 rounded-md cursor-pointer hover:bg-gray-700'>
							<img src={artist.images[0] ? artist.images[0].url : ''} alt={`${artist.name}`} className='w-full h-36 object-cover rounded-md mb-5' />

							<p className='mb-2'>{truncate(artist.name, 16)}</p>
							<p className='font-light text-gray-600'>{artist.followers.total} followers</p>
						</div>
					</li>
				))}
			</ul>
		</div>
	)
}

export default ArtistSelect