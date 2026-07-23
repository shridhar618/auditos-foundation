import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";

import { AppShell } from "@/components/layout/AppShell";
import { AuthProvider } from "@/context/AuthContext";
import { ThemeProvider } from "@/context/ThemeContext";
import ComingSoonPage from "@/pages/ComingSoonPage";
import DashboardPage from "@/pages/DashboardPage";
import LoginPage from "@/pages/LoginPage";
import NotFoundPage from "@/pages/NotFoundPage";
import RegisterPage from "@/pages/RegisterPage";
import ProtectedRoute from "@/routes/ProtectedRoute";

const queryClient = new QueryClient({
  defaultOptions: { queries: { retry: 1, refetchOnWindowFocus: false } },
});

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider>
        <BrowserRouter>
          <AuthProvider>
            <Routes>
              <Route path="/login" element={<LoginPage />} />
              <Route path="/register" element={<RegisterPage />} />

              <Route element={<ProtectedRoute />}>
                <Route element={<AppShell />}>
                  <Route index element={<DashboardPage />} />
                  <Route path="/investigations" element={<ComingSoonPage title="Audit Investigations" />} />
                  <Route path="/documents" element={<ComingSoonPage title="Document Center" />} />
                  <Route path="/policies" element={<ComingSoonPage title="Policy Center" />} />
                  <Route path="/ai-agents" element={<ComingSoonPage title="AI Agents" />} />
                  <Route path="/analytics" element={<ComingSoonPage title="Analytics" />} />
                  <Route path="/users" element={<ComingSoonPage title="Users & Roles" />} />
                  <Route path="/settings" element={<ComingSoonPage title="Settings" />} />
                </Route>
              </Route>

              <Route path="/404" element={<NotFoundPage />} />
              <Route path="*" element={<Navigate to="/404" replace />} />
            </Routes>
          </AuthProvider>
        </BrowserRouter>
      </ThemeProvider>
    </QueryClientProvider>
  );
}
