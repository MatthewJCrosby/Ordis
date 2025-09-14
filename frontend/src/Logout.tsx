import { useEffect, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "./AuthContext";

function getCookie(name: string) {
  return document.cookie
    .split('; ')
    .find(row => row.startsWith(name + '='))
    ?.split('=')[1];
}

export default function Logout() {
  const navigate = useNavigate();
  const hasRun = useRef(false);
  const { setUser } = useAuth();

  useEffect(() => {
    if (hasRun.current) return;
    hasRun.current = true;
    async function doLogout() {
      try {
        const csrfToken = getCookie('csrf_access_token');
        await fetch('http://localhost:5000/auth/logout', {
          method: 'POST',
          credentials: 'include',
          headers: {
            'X-CSRF-TOKEN': csrfToken || '',
          },
        });
      } catch (err) {
        // handle error if needed
      }
      localStorage.removeItem('user');
      setUser(null);
      navigate('/login');
    }
    doLogout();
  }, [navigate]);

  return <p>Logging out...</p>;
}