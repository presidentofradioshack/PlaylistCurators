const Results = (props) => {
	console.log(props)
	return (
		<section className="px-20 font-almanach">
			{(typeof props.results !== 'undefined' && props.results) &&
				<>
					<h1 className="text-3xl text-white font-almanach font-bold mb-5">{`${props.results.length} results`}</h1>
					<div className="w-50">
						<table className="w-full">
							<thead>
								<tr>
									<th className="text-left border-b dark:border-gray-700 font-light text-gray-500 pb-3">Name</th>
									<th className="text-left border-b dark:border-gray-700 font-light text-gray-500 pb-3">Owner</th>
									<th className="text-left border-b dark:border-gray-700 font-light text-gray-500 pb-3">Email</th>
									<th className="text-left border-b dark:border-gray-700 font-light text-gray-500 pb-3">Insta</th>
								</tr>
							</thead>
							<tbody className="dark:text-gray-300">
								{props.results.map(playlist => (
									<tr key={playlist.id}>
										<td className="py-4 dark:border-b dark:border-gray-800">{playlist.name}</td>
										<td className="py-4 dark:border-b dark:border-gray-800">{playlist.owner.display_name}</td>
										<td className="py-4 dark:border-b dark:border-gray-800">{playlist.owner.email}</td>
										<td className="py-4 dark:border-b dark:border-gray-800">{playlist.owner.insta}</td>
									</tr>
								))}
							</tbody>
						</table>
					</div>
				</>
			}
		</section>
	)
}

export default Results