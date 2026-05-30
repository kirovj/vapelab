import { useEffect, useState } from 'react';
import { List, Rate, Button, Popconfirm, message, Empty, Spin } from 'antd';
import { DeleteOutlined, EditOutlined } from '@ant-design/icons';
import { getReviews, deleteReview } from '../api/review';
import type { ReviewItem } from '../api/review';
import ReviewForm from './ReviewForm';
import { useAuthStore } from '../stores/authStore';

interface ReviewListProps {
  juiceId: number;
}

export default function ReviewList({ juiceId }: ReviewListProps) {
  const [reviews, setReviews] = useState<ReviewItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [total, setTotal] = useState(0);
  const [editing, setEditing] = useState<ReviewItem | null>(null);
  const { user } = useAuthStore();

  const fetchReviews = async () => {
    setLoading(true);
    try {
      const res = await getReviews(juiceId);
      setReviews(res.data.data.items);
      setTotal(res.data.data.total);
    } finally { setLoading(false); }
  };

  useEffect(() => { fetchReviews(); }, [juiceId]);

  const handleDelete = async (id: number) => {
    try {
      await deleteReview(id);
      message.success('删除成功');
      fetchReviews();
    } catch { message.error('删除失败'); }
  };

  if (loading) return <Spin className="block text-center py-4" />;

  return (
    <div className="mt-8">
      <h3 className="text-lg font-bold mb-4">用户评论 ({total})</h3>
      {user && !editing && (
        <ReviewForm juiceId={juiceId} onSuccess={fetchReviews} />
      )}
      {editing && (
        <ReviewForm juiceId={juiceId} review={editing} onSuccess={() => { setEditing(null); fetchReviews(); }} onCancel={() => setEditing(null)} />
      )}
      {reviews.length === 0 ? <Empty description="暂无评论，来第一个评价吧" /> : (
        <List
          dataSource={reviews}
          renderItem={(item) => (
            <List.Item actions={user && user.id === item.user_id ? [
              <Button size="small" icon={<EditOutlined />} onClick={() => setEditing(item)}>编辑</Button>,
              <Popconfirm title="确定删除？" onConfirm={() => handleDelete(item.id)}>
                <Button size="small" danger icon={<DeleteOutlined />}>删除</Button>
              </Popconfirm>,
            ] : undefined}>
              <List.Item.Meta
                title={<div className="flex items-center gap-2"><span>{item.username}</span><Rate disabled value={item.rating / 2} allowHalf style={{ fontSize: 14 }} /><span className="text-xs text-gray-400">{item.rating}/10</span></div>}
                description={<div><p>{item.comment || '(无文字评论)'}</p><span className="text-xs text-gray-400">{new Date(item.created_at).toLocaleDateString('zh-CN')}</span></div>}
              />
            </List.Item>
          )}
        />
      )}
    </div>
  );
}
