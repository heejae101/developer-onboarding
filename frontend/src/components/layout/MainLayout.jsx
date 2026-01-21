import React from 'react';
import SidebarLeft from '../ui/SidebarLeft';
import SidebarRight from '../ui/SidebarRight';
import ChatArea from '../ui/ChatArea';

const MainLayout = () => {
    return (
        <div className="flex h-screen w-full overflow-hidden font-sans transition-colors duration-300">
            {/* Background Gradients for Aesthetic Vibe */}
            <div className="absolute top-0 left-0 w-96 h-96 bg-primary-900/20 rounded-full blur-[120px] -translate-x-1/2 -translate-y-1/2 pointer-events-none" />
            <div className="absolute bottom-0 right-0 w-[500px] h-[500px] bg-indigo-900/10 rounded-full blur-[150px] translate-x-1/3 translate-y-1/3 pointer-events-none" />

            {/* Main Grid Layout */}
            <div className="relative z-10 flex w-full max-w-[1920px] mx-auto">
                <SidebarLeft />
                <ChatArea />
                <SidebarRight />
            </div>
        </div>
    );
};

export default MainLayout;
