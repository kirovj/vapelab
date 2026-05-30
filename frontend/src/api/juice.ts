import client from './client';

export interface TagItem {
  id: number;
  name: string;
}

export interface JuiceItem {
  id: number;
  brand_id: number;
  brand_name: string;
  name: string;
  flavor_profile: string | null;
  nicotine_range: string | null;
  vg_pg_ratio: string | null;
  volume: string | null;
  price_range: string | null;
  description: string | null;
  image_urls: string[];
  status: string;
  avg_rating: number;
  review_count: number;
  tags: TagItem[];
  created_at: string;
}

export interface JuiceListData {
  items: JuiceItem[];
  total: number;
  page: number;
  size: number;
}

export const getJuices = (params: {
  page?: number;
  size?: number;
  brand_id?: number;
  flavor_profile?: string;
  sort?: string;
}) => client.get<{ code: number; data: JuiceListData }>('/juices', { params });

export const getJuice = (id: number) =>
  client.get<{ code: number; data: JuiceItem }>(`/juices/${id}`);

export const searchJuices = (q: string, page = 1, size = 20) =>
  client.get<{ code: number; data: JuiceListData }>('/juices/search', { params: { q, page, size } });

export const getTopRated = (limit = 20) =>
  client.get<{ code: number; data: JuiceItem[] }>('/juices/top-rated', { params: { limit } });
