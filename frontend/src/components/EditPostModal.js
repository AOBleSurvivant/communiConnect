import React, { useState } from 'react';
import { postsAPI } from '../services/postsAPI';
import toast from 'react-hot-toast';

const EditPostModal = ({ post, isOpen, onClose, onUpdate }) => {
  const [editContent, setEditContent] = useState(post?.content || '');
  const [editTitle, setEditTitle] = useState(post?.title || '');
  const [editPostType, setEditPostType] = useState(post?.post_type || 'info');
  const [isSaving, setIsSaving] = useState(false);

  const postTypeOptions = [
    { value: 'info', label: 'Information' },
    { value: 'event', label: 'Événement' },
    { value: 'help', label: 'Demande d\'aide' },
    { value: 'announcement', label: 'Annonce' },
    { value: 'discussion', label: 'Discussion' }
  ];

  const handleSave = async () => {
    if (!editContent.trim() || !post?.id) return;
    
    setIsSaving(true);
    try {
      await postsAPI.updatePost(post.id, {
        content: editContent,
        title: editTitle,
        post_type: editPostType
      });
      
      toast.success('Post modifié avec succès !');
      onClose();
      onUpdate?.();
    } catch (error) {
      console.error('Erreur lors de la modification:', error);
      if (error.response?.data?.detail) {
        toast.error(error.response.data.detail);
      } else {
        toast.error('Erreur lors de la modification du post');
      }
    } finally {
      setIsSaving(false);
    }
  };

  const handleCancel = () => {
    setEditContent(post?.content || '');
    setEditTitle(post?.title || '');
    setEditPostType(post?.post_type || 'info');
    onClose();
  };

  if (!isOpen || !post) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 w-full max-w-md mx-4 max-h-[90vh] overflow-y-auto">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-semibold">Modifier le post</h3>
          <button
            onClick={handleCancel}
            className="text-gray-500 hover:text-gray-700"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <form onSubmit={(e) => { e.preventDefault(); handleSave(); }}>
          <div className="space-y-4">
            {/* Type de post */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Type de post
              </label>
              <select
                value={editPostType}
                onChange={(e) => setEditPostType(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                {postTypeOptions.map(option => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            </div>

            {/* Titre */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Titre (optionnel)
              </label>
              <input
                type="text"
                value={editTitle}
                onChange={(e) => setEditTitle(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Titre du post..."
              />
            </div>

            {/* Contenu */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Contenu *
              </label>
              <textarea
                value={editContent}
                onChange={(e) => setEditContent(e.target.value)}
                rows={4}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Contenu du post..."
                required
              />
            </div>

            {/* Message d'information */}
            <div className="bg-blue-50 border border-blue-200 rounded-md p-3">
              <p className="text-sm text-blue-700">
                ⏰ Vous pouvez modifier votre post pendant les 30 premières minutes après sa publication.
              </p>
            </div>

            {/* Boutons */}
            <div className="flex space-x-3">
              <button
                type="button"
                onClick={handleCancel}
                className="flex-1 px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 transition-colors"
              >
                Annuler
              </button>
              <button
                type="submit"
                disabled={isSaving || !editContent.trim()}
                className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                {isSaving ? 'Modification...' : 'Modifier'}
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
};

export default EditPostModal; 