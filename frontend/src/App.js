import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { Navbar } from './components/navbar';
import { SidebarLayout } from './components/sidebar-layout';
import Home from './pages/Home';
import Login from './pages/authentication/Login';
import Register from './pages/authentication/Register';
import LandingPage from './pages/LandingPage';

function App() {
  return (
    <Router>
      <div className="bg-gray-100 min-h-screen flex flex-col">
        <Navbar
          brand={{ title: 'ClimateTech Platform', href: '/' }}
          links={[
            { title: 'Product', href: '#' },
            { title: 'Features', href: '#' },
            { title: 'Company', href: '#' },
          ]}
          cta={{ title: 'Get Started', href: '/register', variant: 'primary' }}
        />
        <main className="flex-grow">
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/home" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
          </Routes>
        </main>
        <SidebarLayout
          navigation={{
            solutions: [
              { title: 'Marketing', href: '#' },
              { title: 'Analytics', href: '#' },
              { title: 'Commerce', href: '#' },
              { title: 'Insights', href: '#' },
            ],
            support: [
              { title: 'Pricing', href: '#' },
              { title: 'Documentation', href: '#' },
              { title: 'Guides', href: '#' },
              { title: 'API Status', href: '#' },
            ],
            company: [
              { title: 'About', href: '#' },
              { title: 'Blog', href: '#' },
              { title: 'Jobs', href: '#' },
              { title: 'Press', href: '#' },
              { title: 'Partners', href: '#' },
            ],
            legal: [
              { title: 'Claim', href: '#' },
              { title: 'Privacy', href: '#' },
              { title: 'Terms', href: '#' },
            ],
          }}
        />
      </div>
    </Router>
  );
}

export default App;