const SearchInput = (props) => {
	return (
		<div className='w-3/4 my-10 mx-auto'>
			<input className='w-full rounded-md' type="text" placeholder={props.placeholder} onChange={props.onChange} />
		</div>
	)
}

export default SearchInput