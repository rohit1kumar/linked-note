import React, { useState } from 'react'
import { Copy, CheckCircle, ChevronDown, ChevronUp } from 'lucide-react'

interface ProfileData {
	name: string
	headline: string
	posts: string[]
}

interface GeneratedMessage {
	connection_message: string
	profile_data: ProfileData
}

interface ResultCardProps {
	result: GeneratedMessage
}

function ResultCard({ result }: ResultCardProps) {
	const [copied, setCopied] = useState(false)
	const [showAllPosts, setShowAllPosts] = useState(false)

	const copyToClipboard = async () => {
		await navigator.clipboard.writeText(result.connection_message)
		setCopied(true)
		setTimeout(() => setCopied(false), 2000)
	}

	const displayPosts = showAllPosts
		? result.profile_data.posts
		: result.profile_data.posts.slice(0, 2)

	const truncatePost = (post: string) => {
		return post.length > 150 ? `${post.substring(0, 150)}...` : post
	}

	return (
		<div className='space-y-6'>
			<h2 className='text-xl font-semibold text-gray-900'>Generated Message</h2>

			<div className='relative bg-gray-50 rounded-lg p-4'>
				<p className='text-gray-700 whitespace-pre-wrap'>
					{result.connection_message}
				</p>
				<button
					onClick={copyToClipboard}
					className='absolute top-2 right-2 p-2 text-gray-500 hover:text-blue-600 transition-colors'
					title='Copy message'
				>
					{copied ? (
						<CheckCircle className='w-5 h-5 text-green-500' />
					) : (
						<Copy className='w-5 h-5' />
					)}
				</button>
			</div>

			<div className='space-y-4'>
				<h3 className='text-lg font-medium text-gray-900'>
					Profile Information
				</h3>
				<div className='bg-gray-50 rounded-lg p-4'>
					<dl className='space-y-2'>
						<div>
							<dt className='text-sm font-medium text-gray-500'>Name</dt>
							<dd className='text-gray-900'>{result.profile_data.name}</dd>
						</div>
						<div>
							<dt className='text-sm font-medium text-gray-500'>Headline</dt>
							<dd className='text-gray-900'>{result.profile_data.headline}</dd>
						</div>
					</dl>
				</div>
			</div>

			{result.profile_data.posts.length > 0 && (
				<div className='space-y-4'>
					<h3 className='text-lg font-medium text-gray-900'>Recent Activity</h3>
					<ul className='space-y-2'>
						{displayPosts.map((post, index) => (
							<li
								key={index}
								className='bg-gray-50 rounded-lg p-3 text-gray-700 text-sm'
							>
								{truncatePost(post)}
							</li>
						))}
					</ul>
					{result.profile_data.posts.length > 2 && (
						<button
							onClick={() => setShowAllPosts(!showAllPosts)}
							className='flex items-center gap-2 text-sm text-blue-600 hover:text-blue-700 transition-colors mx-auto'
						>
							{showAllPosts ? (
								<>
									Show Less <ChevronUp className='w-4 h-4' />
								</>
							) : (
								<>
									Show More <ChevronDown className='w-4 h-4' />
								</>
							)}
						</button>
					)}
				</div>
			)}
		</div>
	)
}

export default ResultCard
