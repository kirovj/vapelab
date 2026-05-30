import { create } from 'zustand';
import client from '../api/client';

interface User {
  id: number;
  username: string;
  email: string;
  is_admin: boolean;
}

interface AuthState {
  user: User | null;
  loading: boolean;
  login: (username: string, password: string) => Promise<void>;
  register: (username: string, email: string, password: string) => Promise<void>;
  logout: () => void;
  fetchUser: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  loading: false,
  login: async (username, password) => {
    const res = await client.post('/auth/login', { username, password });
    const { access_token, refresh_token, user } = res.data.data;
    localStorage.setItem('access_token', access_token);
    localStorage.setItem('refresh_token', refresh_token);
    set({ user });
  },
  register: async (username, email, password) => {
    await client.post('/auth/register', { username, email, password });
  },
  logout: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    set({ user: null });
  },
  fetchUser: async () => {
    try {
      const res = await client.get('/users/me');
      set({ user: res.data.data });
    } catch {
      set({ user: null });
    }
  },
}));
