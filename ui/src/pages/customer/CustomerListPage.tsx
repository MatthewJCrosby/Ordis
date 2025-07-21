import { useQuery } from '@tanstack/react-query';
import { request } from 'graphql-request';
import { DataTable } from '../../components/DataTable';
import type { ColumnDef } from '@tanstack/react-table';

type Customer = {
  id: string;
  name: string;
  email: string;
};

type CustomersResponse = {
  customers: Customer[];
};

const query = `
  query {
    customers {
      id
      name
      email
    }
  }
`;

export default function CustomersPage() {
  const { data, isLoading, error } = useQuery<Customer[]>({
    queryKey: ['customers'],
    queryFn: async () => {
      const res = await request<CustomersResponse>('http://localhost:5000/graphql', query);
      return res.customers;
    },
  });

  const columns: ColumnDef<Customer>[] = [
    { accessorKey: 'id', header: 'ID', enableSorting: true },
    { accessorKey: 'name', header: 'Name', enableSorting: true },
    { accessorKey: 'email', header: 'Email', enableSorting: true },
  ];

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error loading customers.</div>;

  return (
    <div className="max-w-4xl mx-auto">
      <h2 className="text-xl font-bold mb-4">Customers</h2>
      <DataTable data={data ?? []} columns={columns} />
    </div>
  );
}
