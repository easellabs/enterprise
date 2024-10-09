import { Sidebar } from '../components/sidebar';
import { Navbar } from '../components/navbar';
import { Table } from '../components/table';

function DashboardLayout({ children }) {
  return (
    <div className="flex h-screen">
      <Sidebar />
      <div className="flex-1 flex flex-col">
        <Navbar />
        <main className="p-4">
          <Table />
          {children}
        </main>
      </div>
    </div>
  );
}

export default DashboardLayout;
