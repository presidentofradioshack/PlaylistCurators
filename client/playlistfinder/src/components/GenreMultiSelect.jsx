import React, { useState } from 'react'
import Select from 'react-select'
import Genres from '../constants/genre-seeds.json'

const GenreMultiSelect = (props) => {
	return (
		<div className='w-3/4 my-10 mx-auto'>
			<Select 
				isMulti
				value={props.selected}
				onChange={(e) => props.onChange(e)}
				options={Genres}
				isOptionDisabled={() => props.selected.length > 4}
			/>
		</div>
	)
}

export default GenreMultiSelect