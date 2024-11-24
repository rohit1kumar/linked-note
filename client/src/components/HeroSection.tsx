import React from 'react'
import { MessageSquare, Sparkles, Zap, Clock } from 'lucide-react'

const features = [
	{
		icon: <Sparkles className='w-6 h-6' />,
		title: 'AI-Powered',
		description: 'Smart messages tailored to each profile'
	},
	{
		icon: <MessageSquare className='w-6 h-6' />,
		title: 'Personalized',
		description: 'Based on recent posts and activities'
	},
	{
		icon: <Zap className='w-6 h-6' />,
		title: 'Instant',
		description: 'Generate notes within seconds'
	},
	{
		icon: <Clock className='w-6 h-6' />,
		title: 'Time-Saving',
		description: 'Automate your networking efforts'
	}
]

function HeroSection() {
	return (
		<div className='text-center mb-16'>
			<h1 className='text-5xl font-bold text-gray-900 mb-6'>
				Connect Smarter with{' '}
				<span className='text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-indigo-600'>
					LinkedNote
				</span>
			</h1>
			<p className='text-xl text-gray-600 mb-12 max-w-2xl mx-auto'>
				Generate personalized LinkedIn connection requests powered by AI. Stand
				out from the crowd and increase your acceptance rate.
			</p>

			<div className='grid md:grid-cols-4 gap-8 max-w-4xl mx-auto'>
				{features.map((feature, index) => (
					<div
						key={index}
						className='bg-white rounded-xl p-6 shadow-md hover:shadow-lg transition-shadow'
					>
						<div className='text-blue-600 mb-4 flex justify-center'>
							{feature.icon}
						</div>
						<h3 className='font-semibold text-gray-900 mb-2'>
							{feature.title}
						</h3>
						<p className='text-gray-600 text-sm'>{feature.description}</p>
					</div>
				))}
			</div>
		</div>
	)
}

export default HeroSection
