import client from './client';

export interface UserProfile {
  id: number;
  username: string;
  email: string;
  is_admin: boolean;
}

/** 获取当前用户信息 */
export const getMyProfile = () =>
  client.get<{ code: number; data: UserProfile }>('/users/me');

/** 更新当前用户资料 */
export const updateProfile = (data: { username?: string; email?: string }) =>
  client.post('/users/me/update', data);
