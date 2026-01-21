import React from 'react';
import SidebarLeft from '../ui/SidebarLeft';
import SidebarRight from '../ui/SidebarRight';
import ChatArea from '../ui/ChatArea';
import '../../styles/MainLayout.css';

const MainLayout = () => {
    return (
        <div className="layout-container">
            {/* Background Gradients for Aesthetic Vibe */}
            <div className="bg-blob bg-blob-top-left" />
            <div className="bg-blob bg-blob-bottom-right" />

            {/* Main Grid Layout */}
            <div className="main-grid">
                <SidebarLeft />
                <ChatArea />
                <SidebarRight />
            </div>
        </div>
    );
};

export default MainLayout;
