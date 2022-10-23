import React, { useState } from 'react'
import Results from './Results'
import Loading from './Loading'
import GenreMultiSelect from './GenreMultiSelect'
import SearchInput from './SearchInput'
import { useRef } from 'react'
import ArtistSelect from './ArtistSelect'
import TrackSelect from './TrackSelect'
import SelectedItem from './SelectedItem'

const Home = () => {
	const [state, setState] = useState({ 
		artists: [],
		keyword: '',
		results: [],
		loading: false,
		artistSearch: '',
		selectedGenres: [],
		selectedArtists: [],
		trackSearch: '',
		selectedTracks: [],
		tracks: [],
	});
	const { keyword, results, loading, artistSearch, artists, selectedGenres, selectedArtists, selectedTracks, tracks } = state;

	const timerId = useRef();

	const handleSelect = (selectedGenres) => setState({
		...state,
		selectedGenres,
	});

	const onSelectArtist = (id, name) => {
		if (selectedArtists.findIndex(artist => artist.id === id) != -1) {
			return setState({
				...state,
				selectedArtists: selectedArtists.filter(artist => artist.id !== id)
			})
		}

		if (selectedArtists.length < 5) {
			setState({
				...state,
				selectedArtists: [...selectedArtists, {id, name}]
			});
		}
	}

	const onSelectTrack = (id, name) => {
		if (selectedTracks.findIndex(track => track.id === id) != -1) {
			return setState({
				...state,
				selectedTracks: selectedTracks.filter(track => track.id !== id)
			})
		}

		if (selectedTracks.length < 5) {
			setState({
				...state,
				selectedTracks: [...selectedTracks, {id, name}]
			});
		}
	}

	const handleKeywordChange = (e) => setState({
		...state,
		keyword: e.target.value,
	});

	const handleArtistSearchChange = (e) => {
		clearInterval(timerId.current);

		setState({
			...state,
			artistSearch: e.target.value,
		});

		if (e.target.value) {
			timerId.current = setTimeout(() => {
				fetch(`/api/search?${new URLSearchParams({
					'query': `artist:${e.target.value}`,
					'type': 'artist',
					'limit': 5,
				})}`)
				.then(response => response.json())
				.then(data => {
					setState({
						...state,
						artists: data,
					});
				});
			}, 2000);
		}	
	}

	const handleTrackSearchChange = (e) => {
		clearInterval(timerId.current);

		setState({
			...state,
			trackSearch: e.target.value,
		});

		if (e.target.value) {
			timerId.current = setTimeout(() => {
				fetch(`/api/search?${new URLSearchParams({
					'query': `track:${e.target.value}`,
					'type': 'track',
					'limit': 5,
				})}`)
				.then(response => response.json())
				.then(data => {
					setState({
						...state,
						tracks: data,
					});
				});
			}, 2000);
		}	
	}
	
	const renderSelectedArtists = () => selectedArtists ? <SelectedItem items={selectedArtists} onSelectItem={onSelectArtist} /> : null;
	const renderArtistsSelect = () => artists ? <ArtistSelect artists={artists} onSelectArtist={onSelectArtist} /> : null;
	const renderTracksSelect = () => tracks ? <TrackSelect tracks={tracks} onSelectTrack={onSelectTrack} /> : null;
	const renderSelectedTracks = () => selectedTracks ? <SelectedItem items={selectedTracks} onSelectItem={onSelectTrack} /> : null;
	const renderResults = () => {
		if (loading)
			return <Loading />
		
		if (results)
			return <Results results={results} />
	}

	const handleSubmit = (e) => {
		e.preventDefault();
		
		setState({
			...state,
			loading: true,
		});

		const genres = selectedGenres.map(genre => genre.value);
		const artistIds = selectedArtists.map(artist => artist.id);
		const trackIds = selectedTracks.map(track => track.id);

		fetch(`/api/recommendations?${new URLSearchParams({
			keyword: keyword,
			genres: genres,
			artists: artistIds,
			tracks: trackIds,
		})}`).then(response => response.json())
			.then(data => {
				console.log(data);
				setState({
					...state,
					results: data,
					loading: false,
				})
			})
	}

  return (
	<div className='w-full min-h-full'>
		<section className='py-20'>
			<div className='text-center'>
				<h1 className='text-5xl font-bold text-white mt-20 mb-5'>Find Spotify playlist curators</h1>
				<p className='text-xl font-light text-gray-400'>Discover a community of curators who can help you promote your music</p>
			</div>
			<form onSubmit={handleSubmit} className='w-1/2 mx-auto pb-3'>
				<SearchInput placeholder='Keyword' onChange={handleKeywordChange} />
				<GenreMultiSelect selected={selectedGenres} onChange={handleSelect} />
				<SearchInput placeholder='Artist' onChange={handleArtistSearchChange} />
				{renderSelectedArtists()}
				{renderArtistsSelect()}
				<SearchInput placeholder='Track title' onChange={handleTrackSearchChange} />
				{renderSelectedTracks()}
				{renderTracksSelect()}
				<div className='text-center mt-10'>
					<button className='bg-spotify-green px-4 py-2 rounded-md text-white w-24' type='submit'>Submit</button>
				</div>
			</form>
		</section>
		{renderResults()}
	</div>
  )
}

export default Home