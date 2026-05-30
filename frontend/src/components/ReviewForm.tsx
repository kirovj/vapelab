import { useState } from 'react';
import { Form, Rate, Input, Button, message } from 'antd';
import { createReview, updateReview } from '../api/review';
import type { ReviewItem } from '../api/review';

interface ReviewFormProps {
  juiceId: number;
  review?: ReviewItem | null;
  onSuccess: () => void;
  onCancel?: () => void;
}

export default function ReviewForm({ juiceId, review, onSuccess, onCancel }: ReviewFormProps) {
  const [loading, setLoading] = useState(false);
  const [form] = Form.useForm();

  const handleSubmit = async (values: { rating: number; comment?: string }) => {
    setLoading(true);
    try {
      if (review) {
        await updateReview(review.id, values);
        message.success('评论已更新');
      } else {
        await createReview({ juice_id: juiceId, ...values });
        message.success('评论已发表');
      }
      form.resetFields();
      onSuccess();
    } catch (err: unknown) {
      const msg = (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail || '操作失败';
      message.error(msg);
    } finally { setLoading(false); }
  };

  return (
    <div className="mb-4 p-4 bg-gray-50 rounded-lg">
      <Form form={form} onFinish={handleSubmit} initialValues={review ? { rating: review.rating, comment: review.comment } : { rating: 5 }}>
        <Form.Item name="rating" label="评分" rules={[{ required: true }]}>
          <Rate count={10} />
        </Form.Item>
        <Form.Item name="comment" label="评论">
          <Input.TextArea rows={3} placeholder="分享你的使用体验..." />
        </Form.Item>
        <Form.Item>
          <Button type="primary" htmlType="submit" loading={loading}>
            {review ? '更新评论' : '发表评论'}
          </Button>
          {onCancel && <Button className="ml-2" onClick={onCancel}>取消</Button>}
        </Form.Item>
      </Form>
    </div>
  );
}
