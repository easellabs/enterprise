import React, { Suspense, lazy } from 'react';
import { Route, Routes } from 'react-router-dom';
import { Navbar } from './components/navbar';
import { Sidebar } from './components/sidebar';
import ErrorBoundary from './components/ErrorBoundary';
import LoadingSpinner from './components/LoadingSpinner';
import ProtectedRoute from './components/ProtectedRoute';

// Lazy load pages for better performance
const LandingPage = lazy(() => import('./pages/LandingPage'));
const UserDashboard = lazy(() => import('./pages/UserDashboard'));
const AdminDashboard = lazy(() => import('./pages/AdminDashboard'));
const LoginPage = lazy(() => import('./pages/authentication/LoginPage'));
const RegisterPage = lazy(() => import('./pages/RegisterPage'));
const RegisterAdminPage = lazy(() => import('./pages/RegisterAdminPage'));

const AppRouter = () => {
  return (
    <ErrorBoundary>
      <div className="relative isolate flex min-h-screen w-full bg-white dark:bg-zinc-900">
        {/* Sidebar (visible on both desktop and mobile with toggle) */}
        <Sidebar />
        <div className="flex flex-1 flex-col">
          {/* Navbar */}
          <Navbar />
          {/* Suspense for Lazy Loading */}
          <Suspense fallback={<LoadingSpinner />}>
            <Routes>
              {/* Public Routes */}
              <Route path="/" element={<LandingPage />} />
              <Route path="/login" element={<LoginPage />} />
              <Route path="/register" element={<RegisterPage />} />

              {/* Protected Routes */}
              <Route
                path="/register-admin"
                element={
                  <ProtectedRoute adminOnly>
                    <RegisterAdminPage />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/user-dashboard"
                element={
                  <ProtectedRoute>
                    <UserDashboard />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/admin-dashboard"
                element={
                  <ProtectedRoute adminOnly>
                    <AdminDashboard />
                  </ProtectedRoute>
                }
              />

              {/* Catch-All Route for 404 Not Found */}
              <Route path="*" element={<div>404 - Page Not Found</div>} />
            </Routes>
          </Suspense>
        </div>
      </div>
    </ErrorBoundary>
  );
};

export default AppRouter;
