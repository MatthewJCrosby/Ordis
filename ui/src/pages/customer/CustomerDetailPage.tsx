import { useParams } from '@tanstack/react-router';

export default function CustomerDetailPage() {
  const { customerId } = useParams({ from: '/customers/$customerId' });

  return <div className="p-4"> Customer Detail: {customerId}</div>;
}
