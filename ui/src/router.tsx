import {
  createRootRoute,
  createRoute,
  createRouter,
} from '@tanstack/react-router';
import { Outlet } from '@tanstack/react-router'; 
import App from './App';

import HomePage from './pages/home/HomePage';
import CustomersListPage from './pages/customer/CustomerListPage';
import CustomerDetailPage from './pages/customer/CustomerDetailPage';


const rooteRoute = createRootRoute({
    component: App,
});

const indexRoute = createRoute({
    getParentRoute: () => rooteRoute,
    path: '/',
    component: HomePage

})

const customersRoute = createRoute({
    getParentRoute: () => rooteRoute,
    path: '/customers',
    component: CustomersListPage
})

const customerDetailRoute = createRoute({
    getParentRoute: () => customersRoute,
    path: '$customerId', 
    component: CustomerDetailPage
})

const routeTree = rooteRoute.addChildren([
    indexRoute,
    customersRoute.addChildren([customerDetailRoute])
])

export const router = createRouter({routeTree})

declare module '@tanstack/react-router' {
    interface Register {
        router: typeof router;
    }
}
