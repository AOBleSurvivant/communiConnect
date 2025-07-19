import React from 'react';
import NotificationsList from '../components/NotificationsList';

const Notifications = () => {
  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4">
        <NotificationsList />
      </div>
    </div>
  );
};

export default Notifications; 