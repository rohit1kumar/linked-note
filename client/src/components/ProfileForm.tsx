import React from 'react';
import { Send } from 'lucide-react';

interface ProfileFormProps {
  onSubmit: (data: { username: string; password: string; profile_url: string }) => void;
  isLoading: boolean;
}

function ProfileForm({ onSubmit, isLoading }: ProfileFormProps) {
  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    onSubmit({
      username: formData.get('username') as string,
      password: formData.get('password') as string,
      profile_url: formData.get('profile_url') as string,
    });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <h2 className="text-xl font-semibold text-gray-900 mb-6">Profile Details</h2>
      
      <div>
        <label htmlFor="username" className="block text-sm font-medium text-gray-700 mb-1">
          LinkedIn Username
        </label>
        <input
          type="text"
          id="username"
          name="username"
          required
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
          placeholder="Enter your LinkedIn username"
        />
      </div>

      <div>
        <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
          LinkedIn Password
        </label>
        <input
          type="password"
          id="password"
          name="password"
          required
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
          placeholder="Enter your LinkedIn password"
        />
      </div>

      <div>
        <label htmlFor="profile_url" className="block text-sm font-medium text-gray-700 mb-1">
          Target Profile URL
        </label>
        <input
          type="url"
          id="profile_url"
          name="profile_url"
          required
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
          placeholder="https://www.linkedin.com/in/username"
        />
      </div>

      <button
        type="submit"
        disabled={isLoading}
        className="w-full flex items-center justify-center gap-2 bg-blue-600 hover:bg-blue-700 text-white font-medium py-2.5 px-4 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <Send className="w-5 h-5" />
        {isLoading ? 'Generating...' : 'Generate Message'}
      </button>
    </form>
  );
}

export default ProfileForm;