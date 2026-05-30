import client from './client';

// 品牌管理
export const adminCreateBrand = (data: { name: string; country: string; logo_url?: string; description?: string }) =>
  client.post('/admin/brands/create', data);
export const adminUpdateBrand = (id: number, data: Record<string, unknown>) =>
  client.post(`/admin/brands/${id}/update`, data);
export const adminDeleteBrand = (id: number) =>
  client.post(`/admin/brands/${id}/delete`);

// 烟油管理
export const adminCreateJuice = (data: Record<string, unknown>) =>
  client.post('/admin/juices/create', data);
export const adminUpdateJuice = (id: number, data: Record<string, unknown>) =>
  client.post(`/admin/juices/${id}/update`, data);
export const adminDeleteJuice = (id: number) =>
  client.post(`/admin/juices/${id}/delete`);

// 用户管理
export const adminGetUsers = () =>
  client.get<{ code: number; data: { id: number; username: string; email: string; is_admin: boolean; is_active: boolean; created_at: string }[] }>('/admin/users');

export const adminToggleUserActive = (id: number) =>
  client.post(`/admin/users/${id}/toggle-active`);

// 获取标签列表
export const getTags = () =>
  client.get<{ code: number; data: { id: number; name: string }[] }>('/tags');
