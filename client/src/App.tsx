import React, { useState } from 'react'
import { Loader2, Send, Network } from 'lucide-react'
import ProfileForm from './components/ProfileForm'
import ResultCard from './components/ResultCard'
import HeroSection from './components/HeroSection'

interface ProfileData {
	name: string
	headline: string
	posts: string[]
}

interface GeneratedMessage {
	connection_message: string
	profile_data: ProfileData
}

function App() {
	const [isLoading, setIsLoading] = useState(false)
	const [result, setResult] = useState<GeneratedMessage | null>(null)
	const [error, setError] = useState<string | null>(null)

	const handleSubmit = async (formData: {
		username: string
		password: string
		profile_url: string
	}) => {
		setIsLoading(true)
		setError(null)

		try {
			const response = await fetch('http://127.0.0.1:5000/create_message', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify(formData)
			})

			const data = await response.json()

			if (response.ok) {
				setResult(data)
			} else {
				setError(data.details || 'Failed to generate message')
			}
		} catch (err) {
			setError('Unable to connect to the server')
		} finally {
			setIsLoading(false)
		}
	}

	return (
		<div className='min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50'>
			<div className='max-w-6xl mx-auto px-4 py-12'>
				<div className='text-center mb-8'>
					<div className='flex items-center justify-center gap-3 mb-4'>
						<div className='relative'>
							<Network className='w-12 h-12 text-blue-600' />
						</div>
						<h2 className='text-4xl font-bold text-gray-900'>LinkedNote</h2>
					</div>
				</div>

				<HeroSection />

				<div className='grid md:grid-cols-2 gap-8 max-w-4xl mx-auto'>
					<div className='bg-white rounded-xl shadow-lg p-6'>
						<ProfileForm onSubmit={handleSubmit} isLoading={isLoading} />
					</div>

					<div className='bg-white rounded-xl shadow-lg p-6'>
						{isLoading ? (
							<div className='flex flex-col items-center justify-center h-full'>
								<Loader2 className='w-12 h-12 text-blue-600 animate-spin' />
								<p className='mt-4 text-gray-600'>
									Generating your personalized note...
								</p>
							</div>
						) : error ? (
							<div className='text-center text-red-600 p-4'>
								<p className='font-medium'>{error}</p>
							</div>
						) : result ? (
							<ResultCard result={result} />
						) : (
							<div className='flex flex-col items-center justify-center h-full text-gray-500'>
								<Send className='w-12 h-12 mb-4' />
								<p>Your generated message will appear here</p>
							</div>
						)}
					</div>
				</div>
			</div>
		</div>
	)
}

export default App
