import client from './client';

export interface BrandItem {
  id: number;
  name: string;
  country: string;
  logo_url: string | null;
  description: string | null;
  juice_count: number;
  created_at: string;
}

export interface BrandListData {
  items: BrandItem[];
  total: number;
  page: number;
  size: number;
}

export const getBrands = (params: { page?: number; size?: number; country?: string }) =>
  client.get<{ code: number; data: BrandListData }>('/brands', { params });

export const getBrand = (id: number) =>
  client.get<{ code: number; data: BrandItem }>(`/brands/${id}`);
