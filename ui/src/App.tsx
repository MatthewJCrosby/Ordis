import { Outlet } from '@tanstack/react-router';

export default function App() {
  return (
    <div className="min-h-screen flex flex-col">
      <header className="bg-blue-600 text-white p-4">
        <h1 className="text-2xl font-bold">Ordis</h1>
      </header>

      <main className="flex-1 p-4">
        <Outlet />
      </main>

      <footer className="bg-gray-100 p-4 text-sm text-center">
        &copy; 2025 Ordis Inc.
      </footer>
    </div>
  );
}
