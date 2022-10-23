import { ProgressBar } from 'react-loader-spinner'

const Loading = () => {
  return (
	<div className='w-full h-full'>
		<ProgressBar 
			height={80}
			width={80}
			ariaLabel='progress-bar-loading'
			borderColor='#1DB954'
			barColor='#1DB954'
			wrapperClass='mx-auto'
		/>
		
	</div>
  )
}

export default Loading