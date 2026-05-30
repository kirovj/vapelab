import client from './client';

export interface ReviewItem {
  id: number;
  juice_id: number;
  user_id: number;
  username: string;
  rating: number;
  comment: string | null;
  created_at: string;
}

export interface ReviewListData {
  items: ReviewItem[];
  total: number;
  page: number;
  size: number;
}

export const getReviews = (juiceId: number, page = 1, size = 20) =>
  client.get<{ code: number; data: ReviewListData }>(`/juices/${juiceId}/reviews`, { params: { page, size } });

export const createReview = (data: { juice_id: number; rating: number; comment?: string }) =>
  client.post('/reviews/create', data);

export const updateReview = (id: number, data: { rating?: number; comment?: string }) =>
  client.post(`/reviews/${id}/update`, data);

export const deleteReview = (id: number) =>
  client.post(`/reviews/${id}/delete`);
